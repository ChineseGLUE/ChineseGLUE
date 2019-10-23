export CUDA_VISIBLE_DEVICES="1"
pip install sentencepiece --user
CURRENT_DIR=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
XLNET_DIR=$CURRENT_DIR/prev_trained_model/chinese_xlnet_mid_L-24_H-768_A-12
OUTPUT_DIR=$CURRENT_DIR/lcqmc_output
RAW_DIR=$CURRENT_DIR/../../glue/chineseGLUEdatasets/

python run_classifier.py \
    --spiece_model_file=${XLNET_DIR}/spiece.model \
    --model_config_path=${XLNET_DIR}/xlnet_config.json \
    --init_checkpoint=${XLNET_DIR}/xlnet_model.ckpt \
    --task_name=lcqmc \
    --do_train=False \
    --do_eval=True \
    --eval_all_ckpt=False \
    --uncased=False \
    --data_dir=${RAW_DIR}/lcqmc \
    --output_dir=${OUTPUT_DIR} \
    --model_dir=${OUTPUT_DIR} \
    --train_batch_size=32 \
    --eval_batch_size=8 \
    --num_hosts=1 \
    --num_core_per_host=1 \
    --num_train_epochs=3 \
    --max_seq_length=128 \
    --learning_rate=2e-5 \
    --save_steps=1000 \
    --use_tpu=False 
