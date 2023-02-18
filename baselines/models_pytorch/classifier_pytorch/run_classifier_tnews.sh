CURRENT_DIR=`pwd`
export BERT_BASE_DIR=$CURRENT_DIR/prev_trained_model/bert-base-chinese
export GLUE_DIR=$CURRENT_DIR/chineseGLUEdatasets
export OUTPUR_DIR=$CURRENT_DIR/outputs
TASK_NAME="tnews"
horovodrun -np 4 python run_classifier.py

