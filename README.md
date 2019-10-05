# ChineseGLUE
Language Understanding Evaluation benchmark for Chinese: datasets, baselines, corpus and leaderboard

中文语言理解测评基准，包括代表性的数据集、基准模型、语料库、排行榜。  

我们会选择一系列有一定代表性的任务对应的数据集，做为我们测试基准的数据集。这些数据集会覆盖不同的任务、数据量、任务难度。

ChineseGLUE的定位
---------------------------------------------------------------------
为更好的服务中文语言理解、任务和产业界，做为通用语音模型测评的补充，通过完善中文语言理解基础设施的方式来促进中文语言模型的发展

Why do we need a benchmark for Chinese lanague understand evaluation?

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

resources for training, evaluating, and analyzing natural language understanding systems. SuperGLUE consists of: 

##### 1）中文任务的基准测试，覆盖多个不同程度的语言任务 
  
  A benchmark of several sentence or sentence pair language understanding tasks. 

 Currently the datasets used in these tasks are come from public. We will include datasets with private test set before
 
 the end of 2019.

##### 2）公开的排行榜 
  
  A public leaderboard for tracking performance. You will able to submit your prediction files on these tasks,

each task will be evaluated and scored, a final score will also be available.

##### 3）基线模型，包含开始的代码、预训练模型 
  
  baselines for ChineseGLUE tasks. baselines will be available in TensorFlow,PyTorch,Keras and PaddlePaddle.

##### 4）语料库，用于语言建模、预训练或生成型任务 

   A huge amount of raw corpus for pre-train or language modeling research purpose. It will contains around 10G raw corpus in 2019; 
   
   In the first half year of 2020, it will include at least 30G raw corpus; By the end of 2020, we will include enough
   
   raw corpus, such as 100G, so big enough that you will need no more raw corpus for general purpose language modeling.

   You can use it for general purpose or domain adaption, or even for text generating. when you use for domain adaption, 
   you will able to select corpus you are interested in.

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
         1.从 概念 上 看 , 奶油 收入 有 两 个 基本 方面 产品 和 地理 . [分隔符]	产品 和 地理 是 什么 使 奶油 抹 霜 工作 . [分隔符]	neutral
         2.我们 的 一个 号码 会 非常 详细 地 执行 你 的 指示  [分隔符]	我 团队 的 一个 成员 将 非常 精确 地 执行 你 的 命令	[分隔符] entailment
        
        原始的XNLI覆盖15种语言（含低资源语言）。我们选取其中的中文，并将做格式转换，使得非常容易进入训练和测试阶段。


##### 3. ADDING SOON

更多数据集添加中，至少会包含5个数据集，目标是8个覆盖不同任务的有代表性的数据集；如果你有定义良好的数据集，请与我们取得联系。

数据集打包<a href="#">下载</a>地址，添加中。。。

Timeline 时间计划:
---------------------------------------------------------------------
2019-10-20 to 2019-12-31: beta version of ChineseGLUE

2020.1.1 to 2020-12-31: official version of ChineseGLUE

2021.1.1 to 2021-12-31: super version of ChineseGLUE

Contribution 贡献你的力量，从今天开始
---------------------------------------------------------------------

Share your data set with community or make a contribution today! Just send email to chineseGLUE@163.com, 

or join QQ group: 836811304

Reference:
---------------------------------------------------------------------
1、<a href="https://openreview.net/pdf?id=rJ4km2R5t7">GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding</a>

2、<a href="https://w4ngatang.github.io/static/papers/superglue.pdf">SuperGLUE: A Stickier Benchmark for General-Purpose Language Understanding Systems</a>

3、<a href="https://www.aclweb.org/anthology/C18-1166.pdf">LCQMC: A Large-scale Chinese Question Matching Corpus</a>

4、<a href="https://arxiv.org/pdf/1809.05053.pdf">XNLI: Evaluating Cross-lingual Sentence Representations</a>