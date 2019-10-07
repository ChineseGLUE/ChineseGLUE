1. 数据集整体下载，解压到glue文件夹里  
  cd glue  
  wget https://storage.googleapis.com/chineseglue/chineseGLUEdatasets.v0.0.1.zip
  
2. 训练模型  
  将预训练模型下载解压到对应的模型中prev_trained_model文件夹里  
  a. albert  
  https://github.com/brightmart/albert_zh  
  b. bert  
  https://github.com/google-research/bert  
  c. bert-wwm-ext  
  https://github.com/ymcui/Chinese-BERT-wwm  
  d. ernie  
  https://github.com/ArthurRizar/tensorflow_ernie  
  e. roberta    
  https://github.com/brightmart/roberta_zh  
  f. xlnet  
  https://github.com/ymcui/Chinese-PreTrained-XLNet  
  修改run_classifier.sh指定模型路径  
  运行各个模型文件夹下的run_classifier.sh即可
 
