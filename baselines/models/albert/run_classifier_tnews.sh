#!/usr/bin/env bash
# @Author: bo.shi
# @Date:   2019-11-04 09:56:36
# @Last Modified by:   bo.shi
# @Last Modified time: 2019-11-04 22:33:31

TASK_NAME="tnews"
MODEL_NAME="albert_xlarge_zh"
CURRENT_DIR=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
export CUDA_VISIBLE_DEVICES="0"
export ALBERT_CONFIG_DIR=$CURRENT_DIR/albert_config
export ALBERT_PRETRAINED_MODELS_DIR=$CURRENT_DIR/prev_trained_model
export ALBERT_XLARGE_DIR=$ALBERT_PRETRAINED_MODELS_DIR/$MODEL_NAME
export GLUE_DIR=$CURRENT_DIR/../../glue

# download and unzip dataset
if [[ -d $GLUE_DIR ]]; then
  cd $GLUE_DIR
  if [[ -d $TASK_NAME ]]; then
    echo "data exists, dir=$GLUE_DIR/$TASK_NAME"
  else
    mkdir $TASK_NAME
    cd $TASK_NAME
    wget https://storage.googleapis.com/chineseglue/tasks/tnews.zip
    tar zxvf tnews.zip
    rm tnews.zip
  fi
else
  echo "$GLUE_DIR not exist"
fi
echo "Finish download dataset."

# download model
if [[ -d $ALBERT_PRETRAINED_MODELS_DIR ]]; then
  cd $ALBERT_PRETRAINED_MODELS_DIR
  if [[ -d $MODEL_NAME ]]; then
    echo "model exist, dir=$ALBERT_PRETRAINED_MODELS_DIR/$MODEL_NAME"
  else
    mkdir $MODEL_NAME
    cd $MODEL_NAME
    wget https://storage.googleapis.com/albert_zh/albert_xlarge_zh_177k.zip
    tar zxvf albert_xlarge_zh_177k.zip
    rm albert_xlarge_zh_177k.zip
  fi
else
  echo "$ALBERT_PRETRAINED_MODELS_DIR not exist"
fi
echo "Finish download model."

# run task
cd $CURRENT_DIR
echo "Start running..."
python run_classifier.py \
  --task_name=$TASK_NAME \
  --do_train=true \
  --do_eval=true \
  --data_dir=$GLUE_DIR/$TASK_NAME \
  --vocab_file=$ALBERT_CONFIG_DIR/vocab.txt \
  --bert_config_file=$ALBERT_CONFIG_DIR/albert_config_xlarge.json \
  --init_checkpoint=$ALBERT_XLARGE_DIR/albert_model.ckpt \
  --max_seq_length=128 \
  --train_batch_size=32 \
  --learning_rate=2e-5 \
  --num_train_epochs=3.0 \
  --output_dir=$CURRENT_DIR/${TASK_NAME}_output/
