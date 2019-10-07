CURRENT_DIR=`pwd`
export CUDA_VISIBLE_DEVICES="0"
export ALBERT_XLARGE_DIR=$CURRENT_DIR/prev_trained_model/albert_xlarge
export GLUE_DIR=$CURRENT_DIR/../../glue/chineseGLUEdatasets/

python run_classifier.py \
  --task_name=TNEWS \
  --do_train=true \
  --do_eval=true \
  --data_dir=$GLUE_DIR/tnews \
  --vocab_file=$ALBERT_XLARGE_DIR/vocab.txt \
  --bert_config_file=$ALBERT_XLARGE_DIR/albert_config_xlarge.json \
  --init_checkpoint=$ALBERT_XLARGE_DIR/model.ckpt-174000 \
  --max_seq_length=128 \
  --train_batch_size=32 \
  --learning_rate=2e-5 \
  --num_train_epochs=3.0 \
  --output_dir=$CURRENT_DIR/tnews_output/
