#!/usr/bin/env bash
# @Author: bo.shi
# @Date:   2019-11-04 09:56:36
# @Last Modified by:   bo.shi
# @Last Modified time: 2019-11-09 21:44:44

TASK_NAME="bq"
MODEL_NAME="chinese_wwm_ext_L-12_H-768_A-12"
CURRENT_DIR=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
export CUDA_VISIBLE_DEVICES="0"
export BERT_PRETRAINED_MODELS_DIR=$CURRENT_DIR/prev_trained_model
export BERT_WWM_BASE_DIR=$BERT_PRETRAINED_MODELS_DIR/$MODEL_NAME
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
if [ ! -f "train.txt" ] || [ ! -f "dev.txt" ] || [ ! -f "test.txt" ]; then
  rm *
  wget https://storage.googleapis.com/chineseglue/tasks/bq.zip
  unzip bq.zip
  rm bq.zip
else
  echo "data exists"
fi
echo "Finish download dataset."

# download model
if [ ! -d $BERT_WWM_BASE_DIR ]; then
  mkdir -p $BERT_WWM_BASE_DIR
  echo "makedir $BERT_WWM_BASE_DIR"
fi
cd $BERT_WWM_BASE_DIR
if [ ! -f "bert_config.json" ] || [ ! -f "vocab.txt" ] || [ ! -f "bert_model.ckpt.index" ] || [ ! -f "bert_model.ckpt.meta" ] || [ ! -f "bert_model.ckpt.data-00000-of-00001" ]; then
  rm *
  wget --header="Host: doc-08-c4-docs.googleusercontent.com" --header="User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36" --header="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3" --header="Accept-Language: zh-CN,zh;q=0.9" --header="Referer: https://drive.google.com/uc?id=1buMLEjdtrXE2c4G1rpsNGWEx7lUQ0RHi&export=download" "https://doc-08-c4-docs.googleusercontent.com/docs/securesc/ha0ro937gcuc7l7deffksulhg5h7mbp1/9d35m9vsmme32tvu8cbi3spp8kreicvs/1573300800000/05961793937965181111/*/1buMLEjdtrXE2c4G1rpsNGWEx7lUQ0RHi?e=download" -O "chinese_wwm_ext_L-12_H-768_A-12.zip" -c
  unzip chinese_wwm_ext_L-12_H-768_A-12.zip
  rm chinese_wwm_ext_L-12_H-768_A-12.zip
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
  --vocab_file=$BERT_WWM_BASE_DIR/vocab.txt \
  --bert_config_file=$BERT_WWM_BASE_DIR/bert_config.json \
  --init_checkpoint=$BERT_WWM_BASE_DIR/bert_model.ckpt \
  --max_seq_length=128 \
  --train_batch_size=32 \
  --learning_rate=2e-5 \
  --num_train_epochs=3.0 \
  --output_dir=$CURRENT_DIR/${TASK_NAME}_output/
