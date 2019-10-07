1. 数据集整体下载，解压到glue文件夹里
  ```cd glue ```  
  ```wget https://storage.googleapis.com/chineseglue/chineseGLUEdatasets.v0.0.1.zip```
  
2. 训练模型
  将预训练模型下载解压到对应的模型中prev_trained_model文件夹里  
  a. albert_xlarge  
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
  运行各个模型文件夹下不同任务对应的run_classifier_*.sh即可  
  ```sh run_classifier_xnli.sh```

3. 测试效果

    1. TNEWS
    
    | 模型 | 开发集（dev) | 测试集（test) | 训练参数 |
    | :----:| :----: | :----: | :----: |
    | ALBERT-xlarge |	 |	|batch_size=32, length=128, epoch=3 |
    | BERT-base	| 89.80	| 89.78	| batch_size=32, length=128, epoch=3 |
    | BERT-wwm-ext-base | 89.88 | 89.81 |	batch_size=32, length=128, epoch=3 |
    | ERNIE-base	| 89.77	|89.83 | batch_size=32, length=128, epoch=3 |
    | RoBERTa-large	|90.00 | 89.91 |	batch_size=16, length=128, epoch=3 |
    | XLNet-mid	|86.14 | 86.26 |	batch_size=32, length=128, epoch=3 | 

    2. XNLI
    
    | 模型 | 开发集（dev) | 测试集（test) | 训练参数 |
    | :----:| :----: | :----: | :----: |
    | ALBERT-xlarge |	 |	|batch_size=64, length=128, epoch=2 |
    | BERT-base	| 77.80	| 77.8	| batch_size=64, length=128, epoch=2 |
    | BERT-wwm-ext-base | 79.4 | 78.7 |	batch_size=64, length=128, epoch=2 |
    | ERNIE-base	| 79.7	|78.6 | batch_size=64, length=128, epoch=2 |
    | RoBERTa-large	|80.2 |79.9 |	batch_size=64, length=128, epoch=2 |
    | XLNet-mid	|79.2 | 78.7 |	batch_size=64, length=128, epoch=2 | 
    
    3. LCQMC
    
    | 模型 | 开发集（dev) | 测试集（test) | 训练参数 |
    | :----:| :----: | :----: | :----: |
    | ALBERT-xlarge |	 |	|batch_size=64, length=128, epoch=3 |
    | BERT-base	| 89.4 	| 86.9 	| batch_size=64, length=128, epoch=3 |
    | BERT-wwm-ext-base |89.1   | ***87.3*** |	batch_size=64, length=128, epoch=3 |
    | ERNIE-base	| 89.8 	| 87.2 | batch_size=64, length=128, epoch=3|
    | RoBERTa-large	|***89.9***  | 87.2|	batch_size=64, length=128, epoch=3 |
    | XLNet-mid	| |  |	batch_size=64, length=128, epoch=3 | 


