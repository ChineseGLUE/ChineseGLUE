#!/usr/bin/env bash
CURRENT_DIR=`pwd`
export CUDA_VISIBLE_DEVICES="0"
export BERT_BASE_DIR=$CURRENT_DIR/prev_trained_model/chinese_wwm_ext_L-12_H-768_A-12
export GLUE_DIR=$CURRENT_DIR/../../glue/chineseGLUEdatasets/

python run_classifier.py \
  --task_name=lcqmc \
  --do_train=true \
  --do_eval=true \
  --data_dir=$GLUE_DIR/lcqmc \
  --vocab_file=$BERT_BASE_DIR/vocab.txt \
  --bert_config_file=$BERT_BASE_DIR/bert_config.json \
  --init_checkpoint=$BERT_BASE_DIR/bert_model.ckpt \
  --max_seq_length=128 \
  --train_batch_size=32 \
  --learning_rate=2e-5 \
  --num_train_epochs=3.0 \
  --output_dir=$CURRENT_DIR/lcqmc_output/
