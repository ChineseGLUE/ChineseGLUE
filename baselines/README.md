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
    | RoBERTa-wwm-ext | 89.82 | 89.79 |	batch_size=32, length=128, epoch=3 | 
    | RoBERTa-wwm-large-ext | ***90.05*** | ***90.11*** |	batch_size=16, length=128, epoch=3 | 

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
    | RoBERTa-wwm-ext	| 79.56 | 79.28 |	batch_size=64, length=128, epoch=2 | 
    | RoBERTa-wwm-large-ext	| ***80.20*** | ***80.04*** |	batch_size=16, length=128, epoch=2 | 
    
    3. LCQMC  语义相似度匹配
    
    | 模型 | 开发集（dev) | 测试集（test) | 训练参数 |
    | :----:| :----: | :----: | :----: |
    | ALBERT-xlarge | 89.00 | 86.76	|batch_size=64, length=128, epoch=3 |
    | BERT-base	| 89.4 	| 86.9 	| batch_size=64, length=128, epoch=3 |
    | BERT-wwm-ext-base |89.1   | ***87.3*** |	batch_size=64, length=128, epoch=3 |
    | ERNIE-base	| 89.8 	| 87.2 | batch_size=64, length=128, epoch=3|
    | RoBERTa-large	|***89.9***  | 87.2|	batch_size=64, length=128, epoch=3 |
    | XLNet-mid	| 86.14 | 85.98 |	batch_size=32, length=128, epoch=3 | 
    | RoBERTa-wwm-ext	| 89.08 | 86.33 |	batch_size=64, length=128, epoch=3 | 
    | RoBERTa-wwm-large-ext	| 89.79 | 86.82 |	batch_size=16, length=128, epoch=3 | 

    4. INEWS 互联网情感分析
    
    | 模型 | 开发集（dev) | 测试集（test) | 训练参数 |
    | :----:| :----: | :----: | :----: |
    | ALBERT-xlarge |83.70	 | 81.90	|batch_size=32, length=512, epoch=8 |
    | BERT-base	| 81.29	| 82.70	| batch_size=16, length=512, epoch=3 |
    | BERT-wwm-ext-base | 81.93 | 83.46 |	batch_size=16, length=512, epoch=3 |
    | ERNIE-base	| ***84.50***	|***85.14*** | batch_size=16, length=512, epoch=3 |
    | RoBERTa-large	|81.90 | 84.00 |	batch_size=4, length=512, epoch=3 |
    | XLNet-mid	|82.00 | 84.00 |	batch_size=8, length=512, epoch=3 | 
    | RoBERTa-wwm-ext	| 82.98 | 82.28 |	batch_size=16, length=512, epoch=3 | 
    | RoBERTa-wwm-large-ext	|83.73 | 82.78 |	batch_size=4, length=512, epoch=3 | 
    
    5. DRCD 繁体阅读理解
    
    | 模型 | 开发集（dev) | 测试集（test) | 训练参数 |
    | :----:| :----: | :----: | :----: |
    | ALBERT-large	|F1:93.90(94.03) EM:88.88(89.13) | F1:93.06 EM:87.52 |	batch_size=32, length=512, epoch=3 lr=2e-5 warmup=0.05 |
    | ALBERT-xlarge	|F1:94.626(95.101) EM:89.682(90.125) | F1:94.697 EM:89.780 |	batch_size=32, length=512, epoch=3 lr=2.5e-5 warmup=0.06 |
    | ALBERT-tiny	|F1:81.507(81.818) EM:71.606(72.247) | F1:80.672 EM:70.083 |	batch_size=32, length=512, epoch=3 lr=2e-4 warmup=0.1 |
    | RoBERTa-large	|F1:94.93(95.06) EM:90.11(90.24) | F1:94.25 EM:89.35 |	batch_size=32, length=256, epoch=2 lr=3e-5 warmup=0.1|
    | RoBERTa-wwm-ext	|F1:94.26(94.48) EM:89.29(89.64) | F1:93.53 EM:88.12 |	batch_size=32, length=512, epoch=2 lr=3e-5 warmup=0.1| 
    | RoBERTa-wwm-large-ext	|***F1:95.3228(95.54) EM:90.539(90.692)*** | ***F1:95.06 EM:90.70*** | batch_size=32, length=512, epoch=2 lr=2.5e-5 warmup=0.1 |
    
    6. CMRC2018 阅读理解
    
    | 模型 | 开发集（dev) | 训练参数 |
    | :----:| :----: | :----: |
    | ALBERT-large	| F1:87.8596(88.43) EM:67.754(69.028) | epoch3, batch=32, length=512, lr=2e-5, warmup=0.05 |
    | ALBERT-xlarge	| F1:88.657(89.426) EM:68.897(70.643) | epoch3, batch=32, length=512, lr=2e-5, warmup=0.1 |
    | ALBERT-tiny	| F1:73.949(74.664) EM:48.307(50.233) | epoch3, batch=32, length=512, lr=2e-4, warmup=0.1 |
    | RoBERTa-middle	| F1:86.841(87.242) EM:67.195(68.313) | epoch2, batch=32, length=512, lr=3e-5, warmup=0.1 |
    | RoBERTa-large	| F1:88.608(89.431) EM:69.935(72.538) | epoch2, batch=32, length=256, lr=3e-5, warmup=0.1 |
    | RoBERTa-wwm-ext	|F1:87.277(88.052) EM:67.891(69.369) | epoch2, batch=32, length=512, lr=3e-5, warmup=0.1 |  
    | RoBERTa-wwm-large-ext	|***F1:89.415(89.724) EM:70.593(71.358)*** | epoch2, batch=32, length=512, lr=2.5e-5, warmup=0.1 | 

    7. CCKS2018 task3 语义相似度匹配

    | 模型 | 开发集（dev） | 测试集（test） | 训练参数 |
    | :----:| :----: | :----: | :----: |
    | BERT-base | 92.69 | 92.53 | batch_size=64, length=128, epoch=3 |
    | BERT-wwm-ext-base | 93.00 | 92.79 |batch_size=64, length=128, epoch=3 |
    | ERNIE-base | 90.78 | 90.48 | batch_size=64, length=128, epoch=3 |
    | RoBERTa-large	| 93.34 | 92.81 | batch_size=8, length=128, epoch=3 |
    | XLNet-mid	| - | - | - |
    | ALBERT-xlarge |	92.49 | 92.59 | batch_size=16, length=128, epoch=3 |
    | ALBERT-tiny | 88.22 | 87.62 | batch_size=64, length=128, epoch=5 |
    | RoBERTa-wwm-large-ext | **93.62** | **93.61** | batch_size=8, length=128, epoch=3 |

    8. MSRANER 命名实体识别

    | 模型 | 测试集（test） | 训练参数 |
    | :----: | :----: | :----: |
    | BERT-base	| 95.38	| batch_size=16, length=256, epoch=5, lr=2e-5 |
    | BERT-wwm-ext-base	| 95.26	| batch_size=16, length=256, epoch=5, lr=2e-5 |
    | ERNIE-base | 95.17 | batch_size=16, length=256, epoch=5, lr=2e-5 |
    | RoBERTa-large | 96.07	| batch_size=8, length=256, epoch=5, lr=2e-5 |
    | XLNet-mid | - | - |
    | ALBERT-xlarge | - | - |
    | ALBERT-tiny | - | - |
    | RoBERTa-wwm-ext | 95.06	| batch_size=16, length=256, epoch=5, lr=2e-5 |
    | RoBERTa-wwm-large-ext | 95.32	| batch_size=8, length=256, epoch=5, lr=2e-5 |


