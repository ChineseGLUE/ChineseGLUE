#!/usr/bin/env bash
# @Author: bo.shi
# @Date:   2019-11-04 09:56:36
# @Last Modified by:   bo.shi
# @Last Modified time: 2019-11-09 22:38:52

TASK_NAME="lcqmc"
MODEL_NAME="roeberta_zh_L-24_H-1024_A-16"
CURRENT_DIR=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
export CUDA_VISIBLE_DEVICES="0"
export PRETRAINED_MODELS_DIR=$CURRENT_DIR/prev_trained_model
export ROBERTA_LARGE_DIR=$PRETRAINED_MODELS_DIR/$MODEL_NAME
export GLUE_DATA_DIR=$CURRENT_DIR/../../glue/chineseGLUEdatasets

# download and unzip dataset
if [ ! -d $GLUE_DATA_DIR ]; then
  mkdir -p $GLUE_DATA_DIR
  echo "makedir $GLUE_DATA_DIR"
fi
cd $GLUE_DATA_DIR
if [ ! -d $TASK_NAME ]; then
  mkdir $TASK_NAME
  echo "makedir $GLUE_DATA_DIR/$TASK_NAME"
fi
cd $TASK_NAME
echo "Please try again if the data is not downloaded successfully."
wget -c https://raw.githubusercontent.com/pengming617/text_matching/master/data/train.txt
wget -c https://raw.githubusercontent.com/pengming617/text_matching/master/data/dev.txt
wget -c https://raw.githubusercontent.com/pengming617/text_matching/master/data/test.txt
echo "Finish download dataset."

# download model
if [ ! -d $ROBERTA_LARGE_DIR ]; then
  mkdir -p $ROBERTA_LARGE_DIR
  echo "makedir $ROBERTA_LARGE_DIR"
fi
cd $ROBERTA_LARGE_DIR
if [ ! -f "bert_config_large.json" ] || [ ! -f "vocab.txt" ] || [ ! -f "checkpoint" ] || [ ! -f "roberta_zh_large_model.ckpt.index" ] || [ ! -f "roberta_zh_large_model.ckpt.meta" ] || [ ! -f "roberta_zh_large_model.ckpt.data-00000-of-00001" ]; then
  rm *
  wget --header="Host: doc-10-88-docs.googleusercontent.com" --header="User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36" --header="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3" --header="Accept-Language: zh-CN,zh;q=0.9" --header="Referer: https://drive.google.com/uc?id=1W3WgPJWGVKlU9wpUYsdZuurAIFKvrl_Y&export=download" "https://doc-10-88-docs.googleusercontent.com/docs/securesc/ha0ro937gcuc7l7deffksulhg5h7mbp1/m1g3b3c8lrgrpf3bm0a14ga6ndvsnhmk/1573308000000/01257927096926394597/*/1W3WgPJWGVKlU9wpUYsdZuurAIFKvrl_Y?e=download" -O "roeberta_zh_L-24_H-1024_A-16.zip" -c
  unzip roeberta_zh_L-24_H-1024_A-16.zip
  rm roeberta_zh_L-24_H-1024_A-16.zip
else
  echo "model exists"
fi
echo "Finish download model."

# run task
cd $CURRENT_DIR
echo "Start running..."
python run_classifier.py \
  --task_name=$TASK_NAME \
  --do_train=true \
  --do_eval=true \
  --data_dir=$GLUE_DATA_DIR/$TASK_NAME \
  --vocab_file=$ROBERTA_LARGE_DIR/vocab.txt \
  --bert_config_file=$ROBERTA_LARGE_DIR/bert_config_large.json \
  --init_checkpoint=$ROBERTA_LARGE_DIR/roberta_zh_large_model.ckpt \
  --max_seq_length=128 \
  --train_batch_size=32 \
  --learning_rate=2e-5 \
  --num_train_epochs=3.0 \
  --output_dir=$CURRENT_DIR/${TASK_NAME}_output/
