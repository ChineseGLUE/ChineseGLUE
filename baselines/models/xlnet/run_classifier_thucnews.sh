export CUDA_VISIBLE_DEVICES="0"
CURRENT_DIR=`pwd`

export XLNET_DIR=$CURRENT_DIR/prev_trained_model/chinese_xlnet_mid_L-24_H-768_A-12
export RAW_DIR=$CURRENT_DIR/../../glue/chineseGLUEdatasets/
OUTPUT_DIR=$CURRENT_DIR/xlnet_output
TASK_NAME="thucnews"

python run_classifier_thucnews.py \
    --spiece_model_file=${XLNET_DIR}/spiece.model \
    --model_config_path=${XLNET_DIR}/xlnet_config.json \
    --init_checkpoint=${XLNET_DIR}/xlnet_model.ckpt \
    --task_name=$TASK_NAME \
    --do_train=True \
    --do_eval=True \
    --do_predict=True \
    --eval_all_ckpt=False \
    --uncased=False \
    --data_dir=${RAW_DIR}/${TASK_NAME} \
    --output_dir=${OUTPUT_DIR} \
    --model_dir=${OUTPUT_DIR} \
    --train_batch_size=16 \
    --eval_batch_size=16 \
    --num_hosts=1 \
    --num_core_per_host=1 \
    --num_train_epochs=3 \
    --max_seq_length=128 \
    --learning_rate=2e-5 \
    --save_steps=1000 \
    --use_tpu=False \
    --predict_dir=${OUTPUT_DIR}/predict
