export CUDA_VISIBLE_DEVICES="0"
CURRENT_DIR=`pwd`

XLNET_DIR=$CURRENT_DIR/prev_trained_model/chinese_xlnet_mid_L-24_H-768_A-12
OUTPUT_DIR=$CURRENT_DIR/xnli_output
RAW_DIR=$CURRENT_DIR/../../glue/chineseGLUEdatasets/

python run_classifier.py \
    --spiece_model_file=${XLNET_DIR}/spiece.model \
    --model_config_path=${XLNET_DIR}/xlnet_config.json \
    --init_checkpoint=${XLNET_DIR}/xlnet_model.ckpt \
    --task_name=xnli \
    --do_train=True \
    --do_eval=True \
    --eval_all_ckpt=False \
    --uncased=False \
    --data_dir=${RAW_DIR}/xnli \
    --output_dir=${OUTPUT_DIR} \
    --model_dir=${OUTPUT_DIR} \
    --train_batch_size=64 \
    --eval_batch_size=64 \
    --num_hosts=1 \
    --num_core_per_host=1 \
    --num_train_epochs=2 \
    --max_seq_length=128 \
    --learning_rate=3e-5 \
    --save_steps=5000 \
    --use_tpu=False 
