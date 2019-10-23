# ChineseGLUE
Language Understanding Evaluation benchmark for Chinese: datasets, baselines, pre-trained models, corpus and leaderboard

中文语言理解测评基准，包括代表性的数据集、基准(预训练)模型、语料库、排行榜。  

我们会选择一系列有一定代表性的任务对应的数据集，做为我们测试基准的数据集。这些数据集会覆盖不同的任务、数据量、任务难度。

中文任务基准测评(chineseGLUE)-排行榜
---------------------------------------------------------------------
#####  排行榜会定期更新                     数据来源: https://github.com/chineseGLUE/chineseGLUE

| 模型 | Score | 参数 | TNEWS | LCQMC | XNLI | INEWS | DRCD | CMRC2018 | BQ | MSRANER
| :----:| :----: | :----: | :----: |:----: |:----: |:----: |:----: |:----: |:----: |:----: |
| <a href="https://github.com/google-research/bert">BERT-base</a>	| 85.60 | 108M | 89.78 	| 86.9 	|77.8 | 82.7 | 91.46 | 85.48 | 85.08 | 95.38 |
| <a href="https://github.com/ymcui/Chinese-BERT-wwm">BERT-wwm-ext</a> | 86.26  | 108M |89.81   | ***87.3***  | 78.7	| 83.46 | 92.63 | 86.68 | ***85.21*** | 95.26 | 
| <a href="https://github.com/PaddlePaddle/ERNIE">ERNIE-base</a>	|86.36  | 108M |89.83  	|87.2 | 78.6| ***85.14*** | 92.01 | 87.30 | 84.47 | 95.17 | 
| <a href="https://github.com/brightmart/roberta_zh">RoBERTa-large</a> | 87.01 | 334M 	|89.91  | 87.2  | 79.9 | 84.0 | 94.25 | 88.60 | 85.20 | ***96.07*** | 
| <a href="https://github.com/ymcui/Chinese-PreTrained-XLNet">XLNet-mid</a>	| 82.56 | 209M | 86.26 | 85.98  |78.7 |84.0| - | - | 77.85 | - | 
| <a href="https://github.com/brightmart/albert_zh">ALBERT-xlarge</a> | 85.58 | 59M |	88.3 |	86.76 | 74.0? |82.4 | 94.70 | 88.66 | 84.21 | - | 
| <a href="https://github.com/brightmart/albert_zh">ALBERT-tiny</a> | 79.61 | 1.8M |	87.10 |	85.4 | 68.0 |81.4 | 80.67 | 73.95 | 80.76 | - | 
| <a href="https://github.com/ymcui/Chinese-BERT-wwm">RoBERTa-wwm-ext</a>  | 86.07 | 108M  |	89.79 |	86.33 | 79.28 | 82.28 | 93.53 | 87.28 | 84.02 | 95.06 | 
| <a href="https://github.com/ymcui/Chinese-BERT-wwm">RoBERTa-wwm-large</a> | ***87.02*** | 330M |	***90.11*** |	86.82 | ***80.04*** | 82.78 | ***95.06*** | ***89.42*** | 84.90 | 95.32 | 


注：TNEWS:文本分类；LCQMC:语义相似度；XNLI:自然语言推理；INEWS:情感分析；DRCD & CMRC2018:阅读理解；

BQ:智能客服问句匹配；MSRANER:命名实体识别；cmrc2018仅开发集结果；Score是计算平均值获得；



ChineseGLUE的定位
---------------------------------------------------------------------
为更好的服务中文语言理解、任务和产业界，做为通用语音模型测评的补充，通过完善中文语言理解基础设施的方式来促进中文语言模型的发展

Why do we need a benchmark for Chinese lanague understand evaluation?

*** 2019-10-13: 新增评测官网入口; INEWS基线模型 ***

  <a href="https://chineseglue.github.io"> 评测入口</a>

为什么我们需要一个中文任务的基准测试？ 
---------------------------------------------------------------------
首先，中文是一个大语种，有其自身的特定、大量的应用。

    如中文使用人数近14亿，是联合国官方语言之一，产业界有大量的的朋友在做中文的任务。
    中文是象形文字，有文字图形；字与字之间没有分隔符，不同的分词(分字或词)会影响下游任务。

其次，相对于英文的数据集，中文的公开可用的数据集还比较少。
     
     很多数据集是非公开的或缺失基准测评的；多数的论文描述的模型是在英文数据集上做的测试和评估，那么对于中文效果如何？不得而知。

再次，语言理解发展到当前阶段，预训练模型极大的促进了自然语言理解。

     不同的预训练模型相继产生，但不少最先进(state of the art)的模型，并没有官方的中文的版本，也没有对这些预训练模型在不同任务上的公开测试，
     导致技术的发展和应用还有不少距离，或者说技术应用上的滞后。

那么，如果有一个中文任务的基准测试，包含一批大众能广泛使用和测评的数据集、适用中文任务的特点、能紧跟当前世界技术的发展，
     
     能缓解当前中文任务的一些问题，并促进相关应用的发展。

中文任务的基准测试-内容体系 Contents
--------------------------------------------------------------------
Language Understanding Evaluation benchmark for Chinese(ChineseGLUE) got ideas from GLUE, which is a collection of 

resources for training, evaluating, and analyzing natural language understanding systems. ChineseGLUE consists of: 

##### 1）中文任务的基准测试，覆盖多个不同程度的语言任务 
  
A benchmark of several sentence or sentence pair language understanding tasks. 

Currently the datasets used in these tasks are come from public. We will include datasets with private test set before the end of 2019.

##### 2）公开的排行榜 
  
A public leaderboard for tracking performance. You will able to submit your prediction files on these tasks, each task will be evaluated and scored, a final score will also be available.

##### 3）基线模型，包含开始的代码、预训练模型 
  
baselines for ChineseGLUE tasks. baselines will be available in TensorFlow,PyTorch,Keras and PaddlePaddle.

##### 4）语料库，用于语言建模、预训练或生成型任务 

A huge amount of raw corpus for pre-train or language modeling research purpose. It will contains around 10G raw corpus in 2019; 
   
In the first half year of 2020, it will include at least 30G raw corpus; By the end of 2020, we will include enough raw corpus, such as 100G, so big enough that you will need no more raw corpus for general purpose language modeling.

You can use it for general purpose or domain adaption, or even for text generating. when you use for domain adaption, you will able to select corpus you are interested in.

数据集介绍与下载
--------------------------------------------------------------------
##### 1. LCQMC 口语化描述的语义相似度任务
输入是两个句子，输出是0或1。其中0代表语义不相似，1代表语义相似。

        数据量：训练集(238,766)，验证集(8,802)，测试集(12,500)
        例子： 
         1.聊天室都有哪些好的 [分隔符] 聊天室哪个好 [分隔符] 1
         2.飞行员没钱买房怎么办？ [分隔符] 父母没钱买房子 [分隔符] 0

##### 2. XNLI 语言推断任务
跨语言理解的数据集，给定一个前提和假设，判断这个假设与前提是否具有蕴涵、对立、中性关系。
                
        数据量：训练集(392,703)，验证集(？)，测试集(？)
        例子： 
         1.从 概念 上 看 , 奶油 收入 有 两 个 基本 方面 产品 和 地理 .[分隔符] 产品 和 地理 是 什么 使 奶油 抹 霜 工作 . [分隔符]	neutral
         2.我们 的 一个 号码 会 非常 详细 地 执行 你 的 指示 [分隔符] 我 团队 的 一个 成员 将 非常 精确 地 执行 你 的 命令	[分隔符] entailment
        
        原始的XNLI覆盖15种语言（含低资源语言）。我们选取其中的中文，并将做格式转换，使得非常容易进入训练和测试阶段。


##### 3.TNEWS 今日头条中文新闻（短文本）分类
        
        数据量：训练集(266,000)，验证集(57,000)，测试集(57,000)
        例子：
        6552431613437805063_!_102_!_news_entertainment_!_谢娜为李浩菲澄清网络谣言，之后她的两个行为给自己加分_!_佟丽娅,网络谣言,快乐大本营,李浩菲,谢娜,观众们
        每行为一条数据，以_!_分割的个字段，从前往后分别是 新闻ID，分类code，分类名称，新闻字符串（仅含标题），新闻关键词
       
##### 4.INEWS 互联网情感分析任务
        
        数据量：训练集(5,356)，验证集(1,000)，测试集(1,000)     
        例子：
        1_!_00005a3efe934a19adc0b69b05faeae7_!_九江办好人民满意教育_!_近3年来，九江市紧紧围绕“人本教育、公平教育、优质教育、幸福教育”的目标，努力办好人民满意教育，促进了义务教育均衡发展，农村贫困地区办学条件改善。目前，该市特色教育学校有70所 ......
        每行为一条数据，以_!_分割的个字段，从前往后分别是情感类别，数据id，新闻标题，新闻内容
        
##### 5.DRCD 繁体阅读理解任务
台達閱讀理解資料集 Delta Reading Comprehension Dataset (DRCD)(https://github.com/DRCKnowledgeTeam/DRCD) 屬於通用領域繁體中文機器閱讀理解資料集。 本資料集期望成為適用於遷移學習之標準中文閱讀理解資料集。  

```
数据量：训练集(8,016个段落，26,936个问题)，验证集(1,000个段落，3,524个问题)，测试集(1,000个段落，3,493个问题)  
例子：
{
  "version": "1.3",
  "data": [
    {
      "title": "基督新教",
      "id": "2128",
      "paragraphs": [
        {
          "context": "基督新教與天主教均繼承普世教會歷史上許多傳統教義，如三位一體、聖經作為上帝的啟示、原罪、認罪、最後審判等等，但有別於天主教和東正教，新教在行政上沒有單一組織架構或領導，而且在教義上強調因信稱義、信徒皆祭司， 以聖經作為最高權威，亦因此否定以教宗為首的聖統制、拒絕天主教教條中關於聖傳與聖經具同等地位的教導。新教各宗派間教義不盡相同，但一致認同五個唯獨：唯獨恩典：人的靈魂得拯救唯獨是神的恩典，是上帝送給人的禮物。唯獨信心：人唯獨藉信心接受神的赦罪、拯救。唯獨基督：作為人類的代罪羔羊，耶穌基督是人與上帝之間唯一的調解者。唯獨聖經：唯有聖經是信仰的終極權威。唯獨上帝的榮耀：唯獨上帝配得讚美、榮耀",
          "id": "2128-2",
          "qas": [
            {
              "id": "2128-2-1",
              "question": "新教在教義上強調信徒皆祭司以及什麼樣的理念?",
              "answers": [
                {
                  "id": "1",
                  "text": "因信稱義",
                  "answer_start": 92
                }
              ]
            },
            {
              "id": "2128-2-2",
              "question": "哪本經典為新教的最高權威?",
              "answers": [
                {
                  "id": "1",
                  "text": "聖經",
                  "answer_start": 105
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```  
数据格式和squad相同，如果使用简体中文模型进行评测的时候可以将其繁转简(本项目已提供)
        
##### 6.CMRC2018 简体中文阅读理解任务

https://hfl-rc.github.io/cmrc2018/

```
数据量：训练集(短文数2,403，问题数10,142)，试验集(短文数256，问题数1,002)，开发集(短文数848，问题数3,219)  
例子：
{
  "version": "1.0",
  "data": [
    {
        "title": "傻钱策略",
        "context_id": "TRIAL_0",
        "context_text": "工商协进会报告，12月消费者信心上升到78.1，明显高于11月的72。另据《华尔街日报》报道，2013年是1995年以来美国股市表现最好的一年。这一年里，投资美国股市的明智做法是追着“傻钱”跑。所谓的“傻钱”策略，其实就是买入并持有美国股票这样的普通组合。这个策略要比对冲基金和其它专业投资者使用的更为复杂的投资方法效果好得多。",
        "qas":[
                {
                "query_id": "TRIAL_0_QUERY_0",
                "query_text": "什么是傻钱策略？",
                "answers": [
                     "所谓的“傻钱”策略，其实就是买入并持有美国股票这样的普通组合",
                     "其实就是买入并持有美国股票这样的普通组合",
                     "买入并持有美国股票这样的普通组合"
                    ]
                },
                {
                "query_id": "TRIAL_0_QUERY_1",
                "query_text": "12月的消费者信心指数是多少？",
                "answers": [
                    "78.1",
                    "78.1",
                    "78.1"
                    ]
                },
                {
                "query_id": "TRIAL_0_QUERY_2",
                "query_text": "消费者信心指数由什么机构发布？",
                "answers": [
                    "工商协进会",
                    "工商协进会",
                    "工商协进会"
                    ]
                }
            ]
        }
    ]
}
```  
数据格式和squad相同

##### 7. BQ 智能客服问句匹配
该数据集是自动问答系统语料，共有120,000对句子对，并标注了句子对相似度值，取值为0或1（0表示不相似，1表示相似）。数据中存在错别字、语法不规范等问题，但更加贴近工业场景。

        数据量：训练集(100,000)，验证集(10,000)，测试集(10,000)
        例子： 
         1.我存钱还不扣的 [分隔符] 借了每天都要还利息吗 [分隔符] 0
         2.为什么我的还没有额度 [分隔符] 为啥没有额度！！ [分隔符] 1

##### 8. MSRANER 命名实体识别
该数据集共有5万多条中文命名实体识别标注数据（包括人名、地名、组织名），分别用nr、ns、nt表示，其他实体用o表示。

        数据量：训练集(46,364)，测试集(4,365)
        例子： 
         1.据说/o 应/o 老友/o 之/o 邀/o ，/o 梁实秋/nr 还/o 坐/o 着/o 滑竿/o 来/o 此/o 品/o 过/o 玉峰/ns 茶/o 。/o
         2.他/o 每年/o 还/o 为/o 河北农业大学/nt 扶助/o 多/o 名/o 贫困/o 学生/o 。/o

##### 9. 更多数据集添加中，Comming soon!

更多数据集添加中，如果你有定义良好的数据集，请与我们取得联系。

##### 数据集下载 <a href="https://storage.googleapis.com/chineseglue/chineseGLUEdatasets.v0.0.1.zip">整体下载</a>

或使用命令：

    wget https://storage.googleapis.com/chineseglue/chineseGLUEdatasets.v0.0.1.zip

中文任务基准测评(chineseGLUE)-排行榜-各任务对比
---------------------------------------------------------------------

#### TNEWS 短文本分类：

| 模型 | 开发集（dev) | 测试集（test) | 训练参数 |
| :----:| :----: | :----: | :----: |
| ALBERT-xlarge | 88.30	 | 88.30	|batch_size=32, length=128, epoch=3 |
| BERT-base	| 89.80	| 89.78	| batch_size=32, length=128, epoch=3 |
| BERT-wwm-ext-base | 89.88 | 89.81 |	batch_size=32, length=128, epoch=3 |
| ERNIE-base	| 89.77	|89.83 | batch_size=32, length=128, epoch=3 |
| RoBERTa-large	| 90.00 | 89.91 |	batch_size=16, length=128, epoch=3 |
| XLNet-mid	|86.14 | 86.26 |	batch_size=32, length=128, epoch=3 | 
| RoBERTa-wwm-ext | 89.82 | 89.79 |	batch_size=32, length=128, epoch=3 | 
| RoBERTa-wwm-large-ext | ***90.05*** | ***90.11*** |	batch_size=16, length=128, epoch=3 | 

#### XNLI 自然语言推理：
    
| 模型 | 开发集（dev) | 测试集（test) | 训练参数 |
| :----:| :----: | :----: | :----: |
| ALBERT-xlarge |	74.0? |	74.0? |batch_size=64, length=128, epoch=2 |
| BERT-base	| 77.80	| 77.80	| batch_size=64, length=128, epoch=2 |
| BERT-wwm-ext-base | 79.4 | 78.7 |	batch_size=64, length=128, epoch=2 |
| ERNIE-base	| 79.7	|78.6 | batch_size=64, length=128, epoch=2 |
| RoBERTa-large	|***80.2*** |79.9 |	batch_size=64, length=128, epoch=2 |
| XLNet-mid	| 79.2 | 78.7 |	batch_size=64, length=128, epoch=2 | 
| RoBERTa-wwm-ext	| 79.56 | 79.28 |	batch_size=64, length=128, epoch=2 | 
| RoBERTa-wwm-large-ext	| ***80.20*** | ***80.04*** |	batch_size=16, length=128, epoch=2 | 

注：ALBERT-xlarge，在XNLI任务上训练暂时还存在有问题

#### LCQMC 口语化描述的语义相似度匹配：
    
| 模型 | 开发集（dev) | 测试集（test) | 训练参数 |
| :----:| :----: | :----: | :----: |
| ALBERT-xlarge | 89.00	 | 86.76	|batch_size=64, length=128, epoch=3 |
| BERT-base	| 89.4 	| 86.9 	| batch_size=64, length=128, epoch=3 |
| BERT-wwm-ext-base |89.1   | ***87.3*** |	batch_size=64, length=128, epoch=3 |
| ERNIE-base	| 89.8 	| 87.2 | batch_size=64, length=128, epoch=3|
| RoBERTa-large	|***89.9***  | 87.2|	batch_size=64, length=128, epoch=3 |
| XLNet-mid	| 86.14 | 85.98 |	batch_size=64, length=128, epoch=3 | 
| RoBERTa-wwm-ext	| 89.08 | 86.33 |	batch_size=64, length=128, epoch=3 | 
| RoBERTa-wwm-large-ext	| 89.79 | 86.82 |	batch_size=16, length=128, epoch=3 | 
    
    
#### INEWS 互联网情感分析：
    
| 模型 | 开发集（dev) | 测试集（test) | 训练参数 |
| :----:| :----: | :----: | :----: |
| ALBERT-xlarge |	81.80 | 82.40	|batch_size=32, length=512, epoch=8 |
| BERT-base	| 81.29	| 82.70	| batch_size=16, length=512, epoch=3 |
| BERT-wwm-ext-base | 81.93 | 83.46 |	batch_size=16, length=512, epoch=3 |
| ERNIE-base	| ***84.50***	|***85.14*** | batch_size=16, length=512, epoch=3 |
| RoBERTa-large	| 81.90 | 84.00 |	batch_size=4, length=512, epoch=3 |
| XLNet-mid	| 82.00 | 84.00 |	batch_size=8, length=512, epoch=3 | 
| RoBERTa-wwm-ext	| 82.98 | 82.28 |	batch_size=16, length=512, epoch=3 | 
| RoBERTa-wwm-large-ext	| 83.73 | 82.78 |	batch_size=4, length=512, epoch=3 | 

#### DRCD 繁体阅读理解：
    
| 模型 | 开发集（dev) | 测试集（test) | 训练参数 |
| :----:| :----: | :----: | :----: |
| BERT-base	|F1:92.296(92.565) EM:86.600(87.089) | F1:91.46 EM:85.49 |	batch=32, length=512, epoch=2 lr=3e-5 warmup=0.1 |
| BERT-wwm-ext-base	|F1:93.265(93.393) EM:88.002(88.28) | F1:92.633 EM:87.145 |	batch=32, length=512, epoch=2 lr=3e-5 warmup=0.1 |
| ERNIE-base	|F1:92.779(93.021) EM:86.845(87.259) | F1:92.011 EM:86.029 |	batch=32, length=512, epoch=2 lr=3e-5 warmup=0.1 |
| ALBERT-large	|F1:93.90(94.03) EM:88.88(89.13) | F1:93.06 EM:87.52 |	batch=32, length=512, epoch=3 lr=2e-5 warmup=0.05 |
| ALBERT-xlarge	|F1:94.626(95.101) EM:89.682(90.125) | F1:94.697 EM:89.780 |	batch_size=32, length=512, epoch=3 lr=2.5e-5 warmup=0.06 |
| ALBERT-tiny	|F1:81.507(81.818) EM:71.606(72.247) | F1:80.672 EM:70.083 |	batch=32, length=512, epoch=3 lr=2e-4 warmup=0.1 |
| RoBERTa-large	|F1:94.93(95.06) EM:90.11(90.24) | F1:94.25 EM:89.35 |	batch=32, length=256, epoch=2 lr=3e-5 warmup=0.1|
| RoBERTa-wwm-ext	|F1:94.26(94.48) EM:89.29(89.64) | F1:93.53 EM:88.12 |	batch=32, length=512, epoch=2 lr=3e-5 warmup=0.1|
| RoBERTa-wwm-large-ext	|***F1:95.3228(95.54) EM:90.539(90.692)*** | ***F1:95.06 EM:90.70*** | batch=32, length=512, epoch=2 lr=2.5e-5 warmup=0.1 |  

#### CMRC2018 阅读理解(暂时只有开发集结果)：
    
| 模型 | 开发集（dev) | 训练参数 |
| :----:| :----: | :----: |
| BERT-base	|F1:85.476(85.682) EM:64.765(65.921) |	batch=32, length=512, epoch=2 lr=3e-5 warmup=0.1 |
| BERT-wwm-ext-base	|F1:86.679(87.473) EM:66.959(69.09) |	batch=32, length=512, epoch=2 lr=3e-5 warmup=0.1 |
| ERNIE-base	|F1:87.300(87.733) EM:66.890(68.251) |	batch=32, length=512, epoch=2 lr=3e-5 warmup=0.1 |
| ALBERT-large	| F1:87.8596(88.43) EM:67.754(69.028) | epoch3, batch=32, length=512, lr=2e-5, warmup=0.05 |
| ALBERT-xlarge	| F1:88.657(89.426) EM:68.897(70.643) | epoch3, batch=32, length=512, lr=2e-5, warmup=0.1 |
| ALBERT-tiny	| F1:73.949(74.664) EM:48.307(50.233) | epoch3, batch=32, length=512, lr=2e-4, warmup=0.1 |
| RoBERTa-middle	| F1:86.841(87.242) EM:67.195(68.313) | epoch2, batch=32, length=512, lr=3e-5, warmup=0.1 |
| RoBERTa-large	| F1:88.608(89.431) EM:69.935(72.538) | epoch2, batch=32, length=256, lr=3e-5, warmup=0.1 |
| RoBERTa-wwm-ext	|F1:87.277(88.052) EM:67.891(69.369) | epoch2, batch=32, length=512, lr=3e-5, warmup=0.1 | 
| RoBERTa-wwm-large-ext	|***F1:89.415(89.724) EM:70.593(71.358)*** | epoch2, batch=32, length=512, lr=2.5e-5, warmup=0.1 | 

#### BQ 智能客服问句匹配：

| 模型 | 开发集（dev） | 测试集（test） | 训练参数 |
| :----:| :----: | :----: | :----: |
| BERT-base | 85.86 | 85.08 | batch_size=64, length=128, epoch=3 |
| BERT-wwm-ext-base | 86.05 | ***85.21*** |batch_size=64, length=128, epoch=3 |
| ERNIE-base | 85.92 | 84.47 | batch_size=64, length=128, epoch=3 |
| RoBERTa-large	| 85.68 | 85.20 | batch_size=8, length=128, epoch=3 |
| XLNet-mid	| 79.81 | 77.85 | batch_size=32, length=128, epoch=3 |
| ALBERT-xlarge |	85.21 | 84.21 | batch_size=16, length=128, epoch=3 |
| ALBERT-tiny | 82.04 | 80.76 | batch_size=64, length=128, epoch=5 |
| RoBERTa-wwm-ext | 85.31 | 84.02 | batch_size=64, length=128, epoch=3 |
| RoBERTa-wwm-large-ext | ***86.34*** | 84.90 | batch_size=16, length=128, epoch=3 |

#### MSRANER 命名实体识别:

| 模型 | 测试集（test） | 训练参数 |
| :----: | :----: | :----: |
| BERT-base	| 95.38	| batch_size=16, length=256, epoch=5, lr=2e-5 |
| BERT-wwm-ext-base	| 95.26	| batch_size=16, length=256, epoch=5, lr=2e-5 |
| ERNIE-base | 95.17 | batch_size=16, length=256, epoch=5, lr=2e-5 |
| RoBERTa-large | ***96.07***	| batch_size=8, length=256, epoch=5, lr=2e-5 |
| XLNet-mid | - | - |
| ALBERT-xlarge | - | - |
| ALBERT-tiny | - | - |
| RoBERTa-wwm-ext | 95.06	| batch_size=16, length=256, epoch=5, lr=2e-5 |
| RoBERTa-wwm-large-ext | 95.32	| batch_size=8, length=256, epoch=5, lr=2e-5 |


基线模型-代码 start codes for baselines 
---------------------------------------------------------------------

1. 数据集整体下载，解压到glue文件夹里  
  ```cd glue ```  
  ```wget https://storage.googleapis.com/chineseglue/chineseGLUEdatasets.v0.0.1.zip```

   注：lcqmc数据集，请从<a href="http://icrc.hitsz.edu.cn/info/1037/1146.htm">这里</a>申请或搜索网络

2. 训练模型  
    
    ```a.将预训练模型下载解压到对应的模型中prev_trained_model文件夹里。``` 
         ```以bert和albert为例子：```
            
         ``` a1. albert  ``` 
         ```https://github.com/brightmart/albert_zh ```  
         ```a1. bert  ``` 
         ```https://github.com/google-research/bert ```    
        
     ```b.修改run_classifier.sh指定模型路径  ``` 
    
     ```c.运行各个模型文件夹下的run_classifier.sh即可 ```  
       ```sh run_classifier.sh```

3. 详见：<a href="https://github.com/chineseGLUE/chineseGLUE/tree/master/baselines">基准模型-模型训练</a>

#### 开放测评提交入口（建设中）：<a href="https://chineseglue.github.io">我要提交</a>

<img src="https://github.com/chineseGLUE/chineseGLUE/blob/master/resources/img/chineseGLUE_landing.jpeg"  width="80%" height="40%" />


语料库：语言建模、预训练或生成型任务
---------------------------------------------------------------------
可用于语言建模、预训练或生成型任务等，数据量超过10G，主要部分来自于<a href="https://github.com/brightmart/nlp_chinese_corpus">nlp_chinese_corpus项目</a>

当前语料库按照【预训练格式】处理，内含有多个文件夹；每个文件夹有许多不超过4M大小的小文件，文件格式符合预训练格式：每句话一行，文档间空行隔开。

包含如下子语料库（总共14G语料）：

1、新闻语料: 8G语料，分成两个上下两部分，总共有2000个小文件。

2、社区互动语料：3G语料，包含3G文本，总共有900多个小文件。

3、维基百科：1.1G左右文本，包含300左右小文件。

4、评论数据：2.3G左右文本，含有811个小文件，合并<a href="https://github.com/InsaneLife/ChineseNLPCorpus">ChineseNLPCorpus</a>的多个评论数据，清洗、格式转换、拆分成小文件。

这些语料，你可以通过上面这两个项目，清洗数据并做格式转换获得；

你也可以通过邮件申请（chineseGLUE#163.com）获得单个项目的语料，告知单位或学校、姓名、语料用途；

如需获得ChineseGLUE项目下的所有语料，需成为ChineseGLUE组织成员，并完成一个（小）任务。

成为ChineseGLUE组织的创始成员
---------------------------------------------------------------------
##### 你将可以：

1、成功中国第一个中文任务基准测评的创始会员

2、能与其他专业人士共同贡献力量，促进中文自然语言处理事业的发展

3、参与部分工作后，获得已经清洗并预训练的后的、与英文wiki & bookCorpus同等量级、大规模的预训练语料，用于研究目的。

4、优先使用state of the art的中文预训练模型，包括各种体验版或未公开版本

##### 如何参与：

发送邮件 chineseGLUE#163.com，简要介绍你自己、背景、工作或研究方向、你的组织、在哪方面可以为社区贡献力量，我们评估后会与你取得联系你。

任务清单 TODO LIST
---------------------------------------------------------------------
1、搜集、挖掘1个有代表性的数据集，一般为分类或句子对任务 (需要额外5个数据集)

2、阅读理解任务转化成句子对任务（如线索与问题或答案），并做测评，数据应拆分成训练、验证和测试集。

3、基线模型baselises在特定任务模型的训练、预测的方法和脚本(支持PyTorch、Keras)；

4、对当前主流模型（如bert/bert_wwm_ext/roberta/albert/ernie/ernie2.0等），结合ChineseGLUE的数据集，做准确率测试。
   
   如： XLNet-mid在LCQMC数据集上做测试

5、是否还有没有参与测评的模型？

##### 其他
6、排行榜landing页

7、介绍中文语言理解测评基准(ChineseGLUE)

8、测评系统主要功能开发

Timeline 时间计划:
---------------------------------------------------------------------
2019-10-20 to 2019-12-31: beta version of ChineseGLUE

2020.1.1 to 2020-12-31: official version of ChineseGLUE

2021.1.1 to 2021-12-31: super version of ChineseGLUE

Contribution 贡献你的力量，从今天开始
---------------------------------------------------------------------

Share your data set with community or make a contribution today! Just send email to chineseGLUE#163.com, 

or join QQ group: 836811304

Reference:
---------------------------------------------------------------------
1、<a href="https://openreview.net/pdf?id=rJ4km2R5t7">GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding</a>

2、<a href="https://w4ngatang.github.io/static/papers/superglue.pdf">SuperGLUE: A Stickier Benchmark for General-Purpose Language Understanding Systems</a>

3、<a href="https://www.aclweb.org/anthology/C18-1166.pdf">LCQMC: A Large-scale Chinese Question Matching Corpus</a>

4、<a href="https://arxiv.org/pdf/1809.05053.pdf">XNLI: Evaluating Cross-lingual Sentence Representations</a>

5、<a href="https://github.com/fate233/toutiao-text-classfication-dataset">TNES: toutiao-text-classfication-dataset</a>

6、<a href="https://github.com/brightmart/nlp_chinese_corpus">nlp_chinese_corpus: 大规模中文自然语言处理语料 Large Scale Chinese Corpus for NLP</a>

7、<a href="https://github.com/InsaneLife/ChineseNLPCorpus">ChineseNLPCorpus</a>
