1. 数据集整体下载，解压到glue文件夹里  
  ```cd glue ```  
  ```wget https://storage.googleapis.com/chineseglue/chineseGLUEdatasets.v0.0.1.zip```

    注：lcqmc数据集，请从<a href="http://icrc.hitsz.edu.cn/info/1037/1146.htm">这里</a>申请或搜索网络

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
  运行各个模型文件夹下不同任务对应的run_classifier_*.sh即可。如跑xnl运行： 
  ```sh run_classifier_xnli.sh```

3. 测试效果

    1. TNEWS 文本分类
    
    | 模型 | 开发集（dev) | 测试集（test) | 训练参数 |
    | :----:| :----: | :----: | :----: |
    | ALBERT-xlarge |	88.30 | 88.30	|batch_size=32, length=128, epoch=3 |
    | BERT-base	| 89.80	| 89.78	| batch_size=32, length=128, epoch=3 |
    | BERT-wwm-ext-base | 89.88 | 89.81 |	batch_size=32, length=128, epoch=3 |
    | ERNIE-base	| 89.77	|89.83 | batch_size=32, length=128, epoch=3 |
    | RoBERTa-large	|***90.00*** | ***89.91*** |	batch_size=16, length=128, epoch=3 |
    | XLNet-mid	|86.14 | 86.26 |	batch_size=32, length=128, epoch=3 | 
    | RoBERTa-wwm-ext |89.75 | 89.64 |	batch_size=32, length=128, epoch=3 | 

    2. XNLI 自然语言推理
    
    | 模型 | 开发集（dev) | 测试集（test) | 训练参数 |
    | :----:| :----: | :----: | :----: |
    | ALBERT-xlarge |74.0？ |74.0？	|batch_size=64, length=128, epoch=2 |
    | ALBERT-base | 77.0 |	77.1 |batch_size=64, length=128, epoch=2 |
    | ALBERT-large | 78.0 | 77.5	|batch_size=64, length=128, epoch=2 |
    | BERT-base	| 77.80	| 77.8	| batch_size=64, length=128, epoch=2 |
    | BERT-wwm-ext-base | 79.4 | 78.7 |	batch_size=64, length=128, epoch=2 |
    | ERNIE-base	| 79.7	|78.6 | batch_size=64, length=128, epoch=2 |
    | RoBERTa-large	|***80.2*** |***79.9*** |	batch_size=64, length=128, epoch=2 |
    | XLNet-mid	|79.2 | 78.7 |	batch_size=64, length=128, epoch=2 | 
    | RoBERTa-wwm-ext	|78.9 | 78.3 |	batch_size=64, length=128, epoch=2 | 
    
    3. LCQMC  语义相似度匹配
    
    | 模型 | 开发集（dev) | 测试集（test) | 训练参数 |
    | :----:| :----: | :----: | :----: |
    | ALBERT-xlarge | 89.00 | 86.76	|batch_size=64, length=128, epoch=3 |
    | BERT-base	| 89.4 	| 86.9 	| batch_size=64, length=128, epoch=3 |
    | BERT-wwm-ext-base |89.1   | ***87.3*** |	batch_size=64, length=128, epoch=3 |
    | ERNIE-base	| 89.8 	| 87.2 | batch_size=64, length=128, epoch=3|
    | RoBERTa-large	|***89.9***  | 87.2|	batch_size=64, length=128, epoch=3 |
    | XLNet-mid	| 86.14 | 85.98 |	batch_size=32, length=128, epoch=3 | 
    | RoBERTa-wwm-ext	| 88.85 | 86.65 |	batch_size=64, length=128, epoch=3 | 

    4. INEWS 互联网情感分析
    
    | 模型 | 开发集（dev) | 测试集（test) | 训练参数 |
    | :----:| :----: | :----: | :----: |
    | ALBERT-xlarge |83.70	 | 81.90	|batch_size=32, length=512, epoch=8 |
    | BERT-base	| 81.29	| 82.70	| batch_size=16, length=512, epoch=3 |
    | BERT-wwm-ext-base | 81.93 | 83.46 |	batch_size=16, length=512, epoch=3 |
    | ERNIE-base	| ***84.50***	|***85.14*** | batch_size=16, length=512, epoch=3 |
    | RoBERTa-large	|81.90 | 84.00 |	batch_size=4, length=512, epoch=3 |
    | XLNet-mid	|82.00 | 84.00 |	batch_size=8, length=512, epoch=3 | 
    | RoBERTa-wwm-ext	|81.97 | 81.58 |	batch_size=16, length=512, epoch=3 | 
