# coding=utf-8
# Copyright 2018 The Google AI Language Team Authors and The HuggingFace Inc. team.
# Copyright (c) 2018, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" Finetuning the library models for sequence classification on chineseGLUE (Bert, XLM, XLNet, RoBERTa)."""

from __future__ import absolute_import, division, print_function

import argparse
import glob
import logging
import os
import numpy as np
import torch
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler,TensorDataset
from torch.utils.data.distributed import DistributedSampler

from transformers import (WEIGHTS_NAME, BertConfig,
                          BertForSequenceClassification, BertTokenizer,
                          RobertaConfig, XLNetConfig,
                          XLNetForSequenceClassification,
                          XLNetTokenizer,
                          AlbertForSequenceClassification)

from transformers import AdamW, WarmupLinearSchedule

from metrics.glue_compute_metrics import compute_metrics
from processors import glue_output_modes as output_modes

from processors import glue_processors as processors
from processors import glue_convert_examples_to_features as convert_examples_to_features
from processors import collate_fn,xlnet_collate_fn
from tools.common import seed_everything
from tools.common import init_logger,logger
from tools.progressbar import ProgressBar
import horovod.torch as hvd


ALL_MODELS = sum((tuple(conf.pretrained_config_archive_map.keys()) for conf in (BertConfig, XLNetConfig,
                                                                                RobertaConfig)), ())
MODEL_CLASSES = {
    ## bert ernie bert_wwm bert_wwwm_ext
    'bert': (BertConfig, BertForSequenceClassification, BertTokenizer),
    'xlnet': (XLNetConfig, XLNetForSequenceClassification, XLNetTokenizer),
    'roberta': (BertConfig, BertForSequenceClassification, BertTokenizer),
    'albert': (BertConfig, AlbertForSequenceClassification, BertTokenizer)
}

def train(args, train_dataset, model, tokenizer):
    """ Train the model """
    args.train_batch_size = args.per_gpu_train_batch_size * max(1, args.n_gpu)
    #train_sampler = RandomSampler(train_dataset) if args.local_rank == -1 else DistributedSampler(train_dataset)
    train_sampler = DistributedSampler(train_dataset, num_replicas=hvd.size(), rank=hvd.rank(), shuffle=True)
    train_dataloader = DataLoader(train_dataset, sampler=train_sampler, batch_size=args.per_gpu_train_batch_size, collate_fn=xlnet_collate_fn if args.model_type in ['xlnet'] else collate_fn)

    if args.max_steps > 0:
        t_total = args.max_steps
        args.num_train_epochs = args.max_steps // (len(train_dataloader) // args.gradient_accumulation_steps) + 1
    else:
        t_total = len(train_dataloader) // args.gradient_accumulation_steps * args.num_train_epochs
    args.warmup_steps = int(t_total * args.warmup_proportion)
    # Prepare optimizer and schedule (linear warmup and decay)
    no_decay = ['bias', 'LayerNorm.weight']
    optimizer_grouped_parameters = [
        {'params': [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)], 'weight_decay': args.weight_decay},
        {'params': [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
        ]
    optimizer = AdamW(optimizer_grouped_parameters, lr=args.learning_rate, eps=args.adam_epsilon)
    optimizer = hvd.DistributedOptimizer(optimizer, named_parameters=model.named_parameters())
    scheduler = WarmupLinearSchedule(optimizer, warmup_steps=args.warmup_steps, t_total=t_total)
    #if args.fp16:
    #    try:
    #        from apex import amp
    #    except ImportError:
    #        raise ImportError("Please install apex from https://www.github.com/nvidia/apex to use fp16 training.")
    #    model, optimizer = amp.initialize(model, optimizer, opt_level=args.fp16_opt_level)

    ## multi-gpu training (should be after apex fp16 initialization)
    #if args.n_gpu > 1:
    #    model = torch.nn.DataParallel(model)

    ## Distributed training (should be after apex fp16 initialization)
    #if args.local_rank != -1:
    #    model = torch.nn.parallel.DistributedDataParallel(model, device_ids=[args.local_rank],
    #                                                      output_device=args.local_rank,
    #                                                      find_unused_parameters=True)

    # Train!
    if hvd.rank() == 0:
        logger.info("***** Running training *****")
        logger.info("  Num examples = %d", len(train_dataset))
        logger.info("  Num GPUs = %d", hvd.size())
        logger.info("  Num Epochs = %d", args.num_train_epochs)
        logger.info("  Instantaneous batch size per GPU = %d", args.per_gpu_train_batch_size)
        logger.info("  Total train batch size (w. parallel, distributed & accumulation) = %d",
                       args.train_batch_size * args.gradient_accumulation_steps * (torch.distributed.get_world_size() if args.local_rank != -1 else 1))
        logger.info("  Gradient Accumulation steps = %d", args.gradient_accumulation_steps)
        logger.info("  Total optimization steps = %d", t_total)

    model_without_ddp = model
    global_step = 0
    tr_loss, logging_loss = 0.0, 0.0
    model.zero_grad()
    seed_everything(args.seed)  # Added here for reproductibility (even between python 2 and 3)
    hvd.broadcast_parameters(model.state_dict(), root_rank=0)
    hvd.broadcast_optimizer_state(optimizer, root_rank=0)
    for epoch_idx in range(int(args.num_train_epochs)):
        print("Training Epoch: ", epoch_idx + 1)
        train_dataloader.sampler.set_epoch(epoch_idx)
        pbar = ProgressBar(n_total=len(train_dataloader),desc='Training')
        for step, batch in enumerate(train_dataloader):
            model.train()
            batch = tuple(t.to(args.device) for t in batch)
            inputs = {'input_ids':      batch[0],
                      'attention_mask': batch[1],
                      'labels':         batch[3]}
            if args.model_type != 'distilbert':
                inputs['token_type_ids'] = batch[2] if args.model_type in ['bert','xlnet','albert','roberta'] else None  # XLM, DistilBERT don't use segment_ids
            outputs = model(**inputs)
            loss = outputs[0]  # model outputs are always tuple in transformers (see doc)

            #if args.n_gpu > 1:
            #    loss = loss.mean() # mean() to average on multi-gpu parallel training
            #if args.gradient_accumulation_steps > 1:
            #    loss = loss / args.gradient_accumulation_steps

            if args.fp16:
                with amp.scale_loss(loss, optimizer) as scaled_loss:
                    scaled_loss.backward()
                    optimizer.synchronize()
                torch.nn.utils.clip_grad_norm_(amp.master_params(optimizer), args.max_grad_norm)
            else:
                loss.backward()
                optimizer.synchronize()
                torch.nn.utils.clip_grad_norm_(model.parameters(), args.max_grad_norm)

            has_nan = False
            for n, p in model.named_parameters():
                if p.grad is not None:
                    if torch.any(torch.isnan(p.grad)):
                        has_nan = True
                        break
                    if torch.any(p.grad > 50):
                        has_nan = True
                        break
                    if has_nan:
                        optimizer.zero_grad()
            tr_loss += loss.item()
            if (step + 1) % args.gradient_accumulation_steps == 0:
                with optimizer.skip_synchronize():
                    if not has_nan:
                        optimizer.step()
                scheduler.step()  # Update learning rate schedule
                model.zero_grad()
                global_step += 1

                if  args.logging_steps > 0 and global_step % args.logging_steps == 0:
                    # Log metrics
                    results = evaluate(args, model, tokenizer)

                if hvd.rank() == 0 and args.save_steps > 0 and global_step % args.save_steps == 0:
                    # Save model checkpoint
                    output_dir = os.path.join(args.output_dir, 'checkpoint-{}'.format(global_step))
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                    model_to_save = model.module if hasattr(model, 'module') else model  # Take care of distributed/parallel training
                    model_to_save.save_pretrained(output_dir)
                    torch.save(args, os.path.join(output_dir, 'training_args.bin'))
                    logger.info("Saving model checkpoint to %s", output_dir)
                    tokenizer.save_vocabulary(vocab_path=output_dir)
            pbar(step,{'loss':loss.item()})
        print(" ")
        #results = evaluate(args, model, tokenizer)
        #if 'cuda' in str(args.device):
        #    torch.cuda.empty_cache()
    return global_step, tr_loss / global_step

##### Validation
def reduce_tensor_hvd(tensor):
    rt = tensor.clone()
    avg_rt = hvd.allreduce(rt)
    return avg_rt

def evaluate(args, model, tokenizer, prefix=""):
    # Loop to handle MNLI double evaluation (matched, mis-matched)
    eval_task_names = ("mnli", "mnli-mm") if args.task_name == "mnli" else (args.task_name,)
    eval_outputs_dirs = (args.output_dir, args.output_dir + '-MM') if args.task_name == "mnli" else (args.output_dir,)

    results = {}
    for eval_task, eval_output_dir in zip(eval_task_names, eval_outputs_dirs):
        eval_dataset = load_and_cache_examples(args, eval_task, tokenizer, data_type='dev')
        if hvd.rank() == 0:
            if not os.path.exists(eval_output_dir):
                os.makedirs(eval_output_dir)

        args.eval_batch_size = args.per_gpu_eval_batch_size * max(1, args.n_gpu)
        # Note that DistributedSampler samples randomly
        eval_sampler = DistributedSampler(eval_dataset, num_replicas=hvd.size(), rank=hvd.rank(), shuffle=False)
        eval_dataloader = DataLoader(eval_dataset, sampler=eval_sampler, batch_size=args.per_gpu_eval_batch_size,collate_fn=xlnet_collate_fn if args.model_type in ['xlnet'] else collate_fn)

        # Eval!
        if hvd.rank() == 0:
            logger.info("***** Running evaluation {} *****".format(prefix))
            logger.info("  Num examples = %d", len(eval_dataset))
            logger.info("  Batch size = %d", args.eval_batch_size)
        eval_loss = 0.0
        nb_eval_steps = 0
        preds = None
        out_label_ids = None
        pbar = ProgressBar(n_total=len(eval_dataloader),desc = "Evaluating")
        for step,batch in enumerate(eval_dataloader):
            model.eval()
            batch = tuple(t.to(args.device) for t in batch)
            with torch.no_grad():
                inputs = {'input_ids':      batch[0],
                          'attention_mask': batch[1],
                          'labels':         batch[3]}
                if args.model_type != 'distilbert':
                    inputs['token_type_ids'] = batch[2] if args.model_type in ['bert','xlnet','albert','roberta'] else None  # XLM, DistilBERT and RoBERTa don't use segment_ids
                outputs = model(**inputs)
                tmp_eval_loss, logits = outputs[:2]
                eval_loss += tmp_eval_loss.mean().item()
            nb_eval_steps += 1
            if preds is None:
                preds = logits.detach().cpu().numpy()
                out_label_ids = inputs['labels'].detach().cpu().numpy()
            else:
                preds = np.append(preds, logits.detach().cpu().numpy(), axis=0)
                out_label_ids = np.append(out_label_ids, inputs['labels'].detach().cpu().numpy(), axis=0)
            pbar(step)
        print(' ')
        if 'cuda' in str(args.device):
            torch.cuda.empty_cache()
        eval_loss = eval_loss / nb_eval_steps
        if args.output_mode == "classification":
            preds = np.argmax(preds, axis=1)
        elif args.output_mode == "regression":
            preds = np.squeeze(preds)
        result = compute_metrics(eval_task, preds, out_label_ids)
        results.update(result)
        if hvd.rank() == 0:
            logger.info("***** Eval results {} *****".format(prefix))
        for key in sorted(result.keys()):
            acc = torch.tensor(result[key])
            acc = reduce_tensor_hvd(acc)
            results["acc"] = acc.cpu().numpy()
            if hvd.rank() == 0:
                logger.info("  %s = %s", key, acc.cpu())
    return results

def predict(args, model, tokenizer, prefix=""):
    # Loop to handle MNLI double evaluation (matched, mis-matched)
    pred_task_names = ("mnli", "mnli-mm") if args.task_name == "mnli" else (args.task_name,)
    pred_outputs_dirs = (args.output_dir, args.output_dir + '-MM') if args.task_name == "mnli" else (args.output_dir,)

    results = {}
    for pred_task, pred_output_dir in zip(pred_task_names, pred_outputs_dirs):
        pred_dataset = load_and_cache_examples(args, pred_task, tokenizer, data_type='test')
        if not os.path.exists(pred_output_dir) and args.local_rank in [-1, 0]:
            os.makedirs(pred_output_dir)

        args.pred_batch_size = args.per_gpu_eval_batch_size * max(1, args.n_gpu)
        # Note that DistributedSampler samples randomly
        pred_sampler = SequentialSampler(pred_dataset) if args.local_rank == -1 else DistributedSampler(pred_dataset)
        pred_dataloader = DataLoader(pred_dataset, sampler=pred_sampler, batch_size=args.pred_batch_size,collate_fn=xlnet_collate_fn if args.model_type in ['xlnet'] else collate_fn)

        logger.info("***** Running prediction {} *****".format(prefix))
        logger.info("  Num examples = %d", len(pred_dataset))
        logger.info("  Batch size = %d", args.pred_batch_size)
        nb_pred_steps = 0
        preds = None
        pbar = ProgressBar(n_total=len(pred_dataloader),desc = "Predicting")
        for step,batch in enumerate(pred_dataloader):
            model.eval()
            batch = tuple(t.to(args.device) for t in batch)
            with torch.no_grad():
                inputs = {'input_ids':      batch[0],
                          'attention_mask': batch[1],
                          'labels':         batch[3]}
                if args.model_type != 'distilbert':
                    inputs['token_type_ids'] = batch[2] if ('bert' in args.model_type or 'xlnet' in args.model_type) else None  # XLM, DistilBERT and RoBERTa don't use segment_ids
                outputs = model(**inputs)
                _, logits = outputs[:2]
            nb_pred_steps += 1
            if preds is None:
                preds = logits.detach().cpu().numpy()
            else:
                preds = np.append(preds, logits.detach().cpu().numpy(), axis=0)
            pbar(step)
        print(' ')
        if args.output_mode == "classification":
            preds = np.argmax(preds, axis=1)
        elif args.output_mode == "regression":
            preds = np.squeeze(preds)
        output_pred_file = os.path.join(pred_output_dir, prefix, "test_prediction.txt")
        with open(output_pred_file, "w") as writer:
            for pred in preds:
                writer.write(str(pred)+'\n')
    return results

def load_and_cache_examples(args, task, tokenizer, data_type='train'):
    if args.local_rank not in [-1, 0] and not evaluate:
        torch.distributed.barrier()  # Make sure only the first process in distributed training process the dataset, and the others will use the cache

    processor = processors[task]()
    output_mode = output_modes[task]
    # Load data features from cache or dataset file
    cached_features_file = os.path.join(args.data_dir, 'cached_{}_{}_{}_{}'.format(
        data_type,
        list(filter(None, args.model_name_or_path.split('/'))).pop(),
        str(args.max_seq_length),
        str(task)))
    if os.path.exists(cached_features_file):
        logger.info("Loading features from cached file %s", cached_features_file)
        features = torch.load(cached_features_file)
    else:
        logger.info("Creating features from dataset file at %s", args.data_dir)
        label_list = processor.get_labels()
        if task in ['mnli', 'mnli-mm'] and 'roberta' in args.model_type:
            # HACK(label indices are swapped in RoBERTa pretrained model)
            label_list[1], label_list[2] = label_list[2], label_list[1]

        if data_type == 'train':
            examples = processor.get_train_examples(args.data_dir)
        elif data_type == 'dev':
            examples = processor.get_dev_examples(args.data_dir)
        else:
            examples = processor.get_test_examples(args.data_dir)

        features = convert_examples_to_features(examples,
                                                tokenizer,
                                                label_list=label_list,
                                                max_length=args.max_seq_length,
                                                output_mode=output_mode,
                                                pad_on_left=bool(args.model_type in ['xlnet']),                 # pad on the left for xlnet
                                                pad_token=tokenizer.convert_tokens_to_ids([tokenizer.pad_token])[0],
                                                pad_token_segment_id=4 if args.model_type in ['xlnet'] else 0,
        )
        if hvd.rank() == 0:
            logger.info("Saving features into cached file %s", cached_features_file)
            torch.save(features, cached_features_file)

    if hvd.rank() == 0 and not evaluate:
        torch.distributed.barrier()  # Make sure only the first process in distributed training process the dataset, and the others will use the cache

    # Convert to Tensors and build dataset
    all_input_ids = torch.tensor([f.input_ids for f in features], dtype=torch.long)
    all_attention_mask = torch.tensor([f.attention_mask for f in features], dtype=torch.long)
    all_token_type_ids = torch.tensor([f.token_type_ids for f in features], dtype=torch.long)
    all_lens = torch.tensor([f.input_len for f in features],dtype=torch.long)
    if output_mode == "classification":
        all_labels = torch.tensor([f.label for f in features], dtype=torch.long)
    elif output_mode == "regression":
        all_labels = torch.tensor([f.label for f in features], dtype=torch.float)
    dataset = TensorDataset(all_input_ids, all_attention_mask, all_token_type_ids, all_lens,all_labels)
    return dataset


def main():
    parser = argparse.ArgumentParser()

    ## Required parameters
    parser.add_argument("--data_dir", default="./chineseGLUEdatasets/tnews/", type=str,
                        help="The input data dir. Should contain the .tsv files (or other data files) for the task.")
    parser.add_argument("--model_type", default="bert", type=str, 
                        help="Model type selected in the list: " + ", ".join(MODEL_CLASSES.keys()))
    parser.add_argument("--model_name_or_path", default="bert-base-chinese", type=str, 
                        help="Path to pre-trained model or shortcut name selected in the list: " + ", ".join(ALL_MODELS))
    parser.add_argument("--task_name", default="tnews", type=str,
                        help="The name of the task to train selected in the list: " + ", ".join(processors.keys()))
    parser.add_argument("--device", default="mtgpu", type=str,
                        help="device")
    parser.add_argument("--output_dir", default="./outputs/tnews_output", type=str,
                        help="The output directory where the model predictions and checkpoints will be written.")

    ## Other parameters
    parser.add_argument("--config_name", default="", type=str,
                        help="Pretrained config name or path if not the same as model_name")
    parser.add_argument("--tokenizer_name", default="", type=str,
                        help="Pretrained tokenizer name or path if not the same as model_name")
    parser.add_argument("--cache_dir", default="", type=str,
                        help="Where do you want to store the pre-trained models downloaded from s3")
    parser.add_argument("--max_seq_length", default=128, type=int,
                        help="The maximum total input sequence length after tokenization. Sequences longer "
                             "than this will be truncated, sequences shorter will be padded.")
    parser.add_argument("--do_train", default=True,
                        help="Whether to run training.")
    parser.add_argument("--do_eval", default=True,
                        help="Whether to run eval on the dev set.")
    parser.add_argument("--do_predict", action='store_true',
                        help="Whether to run the model in inference mode on the test set.")
    parser.add_argument("--do_lower_case", default=True,
                        help="Set this flag if you are using an uncased model.")

    parser.add_argument("--per_gpu_train_batch_size", default=32, type=int,
                        help="Batch size per GPU/CPU for training.")
    parser.add_argument("--per_gpu_eval_batch_size", default=32, type=int,
                        help="Batch size per GPU/CPU for evaluation.")
    parser.add_argument('--gradient_accumulation_steps', type=int, default=1,
                        help="Number of updates steps to accumulate before performing a backward/update pass.")
    parser.add_argument("--learning_rate", default=2e-5, type=float,
                        help="The initial learning rate for Adam.")
    parser.add_argument("--weight_decay", default=0.01, type=float,
                        help="Weight deay if we apply some.")
    parser.add_argument("--adam_epsilon", default=1e-8, type=float,
                        help="Epsilon for Adam optimizer.")
    parser.add_argument("--max_grad_norm", default=1.0, type=float,
                        help="Max gradient norm.")
    parser.add_argument("--num_train_epochs", default=4.0, type=float,
                        help="Total number of training epochs to perform.")
    parser.add_argument("--max_steps", default=-1, type=int,
                        help="If > 0: set total number of training steps to perform. Override num_train_epochs.")
    parser.add_argument("--warmup_proportion", default=0.1, type=float,
                        help="Proportion of training to perform linear learning rate warmup for,E.g., 0.1 = 10% of training.")

    parser.add_argument('--logging_steps', type=int, default=2093,
                        help="Log every X updates steps.")
    parser.add_argument('--save_steps', type=int, default=2093,
                        help="Save checkpoint every X updates steps.")
    parser.add_argument("--eval_all_checkpoints", action='store_true',
                        help="Evaluate all checkpoints starting with the same prefix as model_name ending and ending with step number")
    parser.add_argument("--no_cuda", action='store_true',
                        help="Avoid using CUDA when available")
    parser.add_argument('--overwrite_output_dir', default=True,
                        help="Overwrite the content of the output directory")
    parser.add_argument('--overwrite_cache', action='store_true',
                        help="Overwrite the cached training and evaluation sets")
    parser.add_argument('--seed', type=int, default=42,
                        help="random seed for initialization")

    parser.add_argument('--fp16', action='store_true',
                        help="Whether to use 16-bit (mixed) precision (through NVIDIA apex) instead of 32-bit")
    parser.add_argument('--fp16_opt_level', type=str, default='O1',
                        help="For fp16: Apex AMP optimization level selected in ['O0', 'O1', 'O2', and 'O3']."
                             "See details at https://nvidia.github.io/apex/amp.html")
    parser.add_argument("--local_rank", type=int, default=-1,
                        help="For distributed training: local_rank")
    parser.add_argument('--server_ip', type=str, default='', help="For distant debugging.")
    parser.add_argument('--server_port', type=str, default='', help="For distant debugging.")
    args = parser.parse_args()

    hvd.init()
    args.output_dir = args.output_dir +'{}'.format(args.model_type)
    if hvd.rank() == 0:
        if not os.path.exists(args.output_dir):
            os.mkdir(args.output_dir)
    init_logger(log_file=args.output_dir+'/{}-{}.log'.format(args.model_type,args.task_name))
    if hvd.rank() == 0:
        if os.path.exists(args.output_dir) and os.listdir(args.output_dir) and args.do_train and not args.overwrite_output_dir:
            raise ValueError("Output directory ({}) already exists and is not empty. Use --overwrite_output_dir to overcome.".format(args.output_dir))

    # Setup distant debugging if needed
    if args.server_ip and args.server_port:
        # Distant debugging - see https://code.visualstudio.com/docs/python/debugging#_attach-to-a-local-script
        import ptvsd
        print("Waiting for debugger attach")
        ptvsd.enable_attach(address=(args.server_ip, args.server_port), redirect_output=True)
        ptvsd.wait_for_attach()

    ## Setup CUDA, GPU & distributed training
    #if args.local_rank == -1 or args.no_cuda:
    #    device = torch.device("cuda" if torch.cuda.is_available() and not args.no_cuda else "cpu")
    #    args.n_gpu = torch.cuda.device_count()
    #else:  # Initializes the distributed backend which will take care of sychronizing nodes/GPUs
    #    torch.cuda.set_device(args.local_rank)
    #    device = torch.device("cuda", args.local_rank)
    #    torch.distributed.init_process_group(backend='nccl')
    #    args.n_gpu = 1
    args.n_gpu = hvd.size()
    device=args.device
    if args.device == "mtgpu":
        os.environ["PVR_GPUIDX"] = str(hvd.local_rank())
        os.environ["MTGPU_MAX_MEM_USAGE_GB"] = "31"
        import musa_torch_extension


    # Setup logging
    logger.warning("Process rank: %s, device: %s, n_gpu: %s, distributed training: %s, 16-bits training: %s",
                    args.local_rank, device, args.n_gpu, bool(args.local_rank != -1), args.fp16)

    # Set seed
    seed_everything(args.seed)
    # Prepare GLUE task
    args.task_name = args.task_name.lower()
    if args.task_name not in processors:
        raise ValueError("Task not found: %s" % (args.task_name))
    processor = processors[args.task_name]()
    args.output_mode = output_modes[args.task_name]
    label_list = processor.get_labels()
    num_labels = len(label_list)

    # Load pretrained model and tokenizer
    if args.local_rank not in [-1, 0]:
        torch.distributed.barrier()  # Make sure only the first process in distributed training will download model & vocab

    args.model_type = args.model_type.lower()
    config_class, model_class, tokenizer_class = MODEL_CLASSES[args.model_type]
    config = config_class.from_pretrained(args.config_name if args.config_name else args.model_name_or_path, num_labels=num_labels, finetuning_task=args.task_name)
    tokenizer = tokenizer_class.from_pretrained(args.tokenizer_name if args.tokenizer_name else args.model_name_or_path, do_lower_case=args.do_lower_case)
    model = model_class.from_pretrained(args.model_name_or_path, from_tf=bool('.ckpt' in args.model_name_or_path), config=config)

    if args.local_rank == 0:
        torch.distributed.barrier()  # Make sure only the first process in distributed training will download model & vocab

    model.to(args.device)

    if args.local_rank == 0:
        logger.info("Training/evaluation parameters %s", args)

    # Training
    if args.do_train:
        train_dataset = load_and_cache_examples(args, args.task_name, tokenizer, data_type='train')
        global_step, tr_loss = train(args, train_dataset, model, tokenizer)
        logger.info(" global_step = %s, average loss = %s", global_step, tr_loss)


    # Saving best-practices: if you use defaults names for the model, you can reload it using from_pretrained()
    if args.do_train and hvd.rank() == 0:
        # Create output directory if needed
        if not os.path.exists(args.output_dir) and hvd.rank() == 0:
            os.makedirs(args.output_dir)

        logger.info("Saving model checkpoint to %s", args.output_dir)
        # Save a trained model, configuration and tokenizer using `save_pretrained()`.
        # They can then be reloaded using `from_pretrained()`
        model_to_save = model.module if hasattr(model, 'module') else model  # Take care of distributed/parallel training
        model_to_save.save_pretrained(args.output_dir)
        tokenizer.save_pretrained(args.output_dir)

        # Good practice: save your training arguments together with the trained model
        torch.save(args, os.path.join(args.output_dir, 'training_args.bin'))

        # Load a trained model and vocabulary that you have fine-tuned
        model = model_class.from_pretrained(args.output_dir)
        tokenizer = tokenizer_class.from_pretrained(args.output_dir, do_lower_case=args.do_lower_case)
        model.to(args.device)

    # Evaluation
    results = {}
    if args.do_eval and args.local_rank in [-1, 0]:
        tokenizer = tokenizer_class.from_pretrained(args.output_dir, do_lower_case=args.do_lower_case)
        checkpoints = [args.output_dir]
        if args.eval_all_checkpoints:
            checkpoints = list(os.path.dirname(c) for c in sorted(glob.glob(args.output_dir + '/**/' + WEIGHTS_NAME, recursive=True)))
            logging.getLogger("transformers.modeling_utils").setLevel(logging.WARN)  # Reduce logging
        logger.info("Evaluate the following checkpoints: %s", checkpoints)
        for checkpoint in checkpoints:
            global_step = checkpoint.split('-')[-1] if len(checkpoints) > 1 else ""
            prefix = checkpoint.split('/')[-1] if checkpoint.find('checkpoint') != -1 else ""
            model = model_class.from_pretrained(checkpoint)
            model.to(args.device)
            result = evaluate(args, model, tokenizer, prefix=prefix)
            result = dict((k + '_{}'.format(global_step), v) for k, v in result.items())
            results.update(result)
        output_eval_file = os.path.join(args.output_dir, "checkpoint_eval_results.txt")
        with open(output_eval_file, "w") as writer:
            for key in sorted(results.keys()):
                writer.write("%s = %s\n" % (key, str(results[key])))

if __name__ == "__main__":
    main()
