---
layout: default
title: "Horizon Summary: 2026-06-22 (ZH)"
date: 2026-06-22
lang: zh
---

> 从 25 条内容中筛选出 16 条重要资讯。

---

1. [Claude 的身份验证要求](#item-1) ⭐️ 7.0/10
2. [宁可重复代码，也不要错误的抽象（2016）](#item-2) ⭐️ 7.0/10
3. [Cloudflare 推出无需注册账户的 60 分钟临时 Worker 部署功能](#item-3) ⭐️ 7.0/10
4. [我以前的工作是否只因欺诈而存在？](#item-4) ⭐️ 6.0/10
5. [万物皆对数](#item-5) ⭐️ 6.0/10
6. [AI 工具重塑软件「自建还是购买」的经济逻辑](#item-6) ⭐️ 6.0/10
7. [sqlite-utils 4.0rc1 新增数据库迁移与嵌套事务支持](#item-7) ⭐️ 6.0/10
8. [矩阵循环单元（MRU）更新：解决训练不稳定问题的注意力替代方案](#item-8) ⭐️ 6.0/10
9. [研究者发布无 Softmax 注意力模型，配备自定义 Triton 内核](#item-9) ⭐️ 6.0/10
10. [Apertus – 面向主权 AI 的开放基础模型](#item-10) ⭐️ 5.0/10
11. [个人网站的 JSON-LD 详解](#item-11) ⭐️ 5.0/10
12. [一个略有改进的 DVD-JEPA 演示 (P)](#item-12) ⭐️ 5.0/10
13. [WeightsLab：面向神经网络训练的开源数据中心调试工具](#item-13) ⭐️ 5.0/10
14. [超越理性（免费的全面毁灭风格即时战略游戏）](#item-14) ⭐️ 4.0/10
15. [针对西班牙语专业词汇微调 Whisper 模型的最佳实践探讨](#item-15) ⭐️ 4.0/10
16. [LoRA 上的 EMA 应用？(讨论)](#item-16) ⭐️ 4.0/10

---

<a id="item-1"></a>
## [Claude 的身份验证要求](https://support.claude.com/en/articles/14328960-identity-verification-on-claude) ⭐️ 7.0/10

Anthropic 正在对高级 Claude 模型的访问实施身份验证要求，此举引发了关于隐私保护、地缘政治背景下 AI 访问限制以及对美国 AI 行业竞争影响的广泛讨论。

hackernews · bathory · 6月21日 12:44 · [社区讨论](https://news.ycombinator.com/item?id=48618455)

**标签**: `#anthropic`, `#AI-policy`, `#identity-verification`, `#AI-access`, `#privacy`

---

<a id="item-2"></a>
## [宁可重复代码，也不要错误的抽象（2016）](https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction) ⭐️ 7.0/10

Sandi Metz 的这篇颇具影响力的文章认为，过早或错误的抽象比代码重复危害更大。该文在 Hacker News 上引发了大量讨论，再度引起广泛关注。

hackernews · rafaepta · 6月21日 16:08 · [社区讨论](https://news.ycombinator.com/item?id=48620090)

**标签**: `#software-design`, `#abstraction`, `#code-quality`, `#DRY`, `#refactoring`

---

<a id="item-3"></a>
## [Cloudflare 推出无需注册账户的 60 分钟临时 Worker 部署功能](https://simonwillison.net/2026/Jun/21/temporary-cloudflare-accounts/#atom-everything) ⭐️ 7.0/10

Cloudflare 现在允许开发者通过运行 `npx wrangler deploy --temporary` 命令，无需注册账户即可将 Workers 项目部署为有效期 60 分钟的临时应用。部署完成后，系统会提供一个认领链接，用户可在到期前选择将项目转为永久所有权。 该功能大幅降低了部署无服务器应用的门槛，非常适合快速原型开发、演示以及需要即时创建在线端点的 AI 智能体工作流。它彻底消除了注册账户的繁琐步骤，在自动化或 AI 驱动的开发流程中尤为实用。 Simon Willison 通过让 Codex Desktop 中的 GPT-4.5 构建一个 HTTP 重定向解析工具，亲测验证了该功能按预期正常运行。部署后会生成一个唯一子域名（例如 `cloudflare-redirect-resolver.educated-celery.workers.dev`）以及一个与 60 分钟有效期同步倒计时的账户认领页面。

rss · Simon Willison · 6月21日 22:01

**背景**: Cloudflare Workers 是一个无服务器平台，允许开发者在 Cloudflare 遍布全球 330 多个城市的边缘网络上运行 JavaScript 等语言编写的代码。Wrangler 是用于管理和部署 Cloudflare Workers 项目的官方命令行工具（CLI）。无服务器计算意味着开发者无需管理服务器即可部署代码，云服务商会自动处理底层基础设施。临时部署是指生命周期短暂的运行环境，常用于测试、预览或一次性任务。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://workers.cloudflare.com/">Cloudflare Workers - Global Serverless Functions Platform</a></li>
<li><a href="https://developers.cloudflare.com/workers/wrangler/">Wrangler · Cloudflare Workers docs</a></li>

</ul>
</details>

**标签**: `#Cloudflare`, `#serverless`, `#developer-tools`, `#AI-agents`, `#deployment`

---

<a id="item-4"></a>
## [我以前的工作是否只因欺诈而存在？](https://david.newgas.net/did-my-old-job-only-exist-because-of-fraud/) ⭐️ 6.0/10

作者反思自己的前一份工作是否依赖虚假账单行为得以维持，此话题引发了社区对企业欺诈、承包商虚报账单及科技职场财务违规现象的广泛讨论。

hackernews · advisedwang · 6月21日 21:40 · [社区讨论](https://news.ycombinator.com/item?id=48622867)

**标签**: `#corporate-culture`, `#fraud`, `#contracting`, `#career`, `#software-industry`

---

<a id="item-5"></a>
## [万物皆对数](https://alexkritchevsky.com/2026/05/25/everything-is-logarithms.html) ⭐️ 6.0/10

这是一篇数学随笔，论证对数是贯穿数学众多领域的统一核心概念。文章在 HN 社区引发讨论，网友们就其深度与新颖性展开了辩论。

hackernews · E-Reverance · 6月21日 21:10 · [社区讨论](https://news.ycombinator.com/item?id=48622626)

**标签**: `#mathematics`, `#logarithms`, `#mathematical-foundations`, `#education`, `#number-theory`

---

<a id="item-6"></a>
## [AI 工具重塑软件「自建还是购买」的经济逻辑](https://brandur.org/minimum-viable-unit) ⭐️ 6.0/10

Brandur Leach 发表了一篇文章，认为 AI 编程工具大幅降低了软件开发的最低可行成本，从根本上改变了个人和组织在「自建还是购买」上的传统权衡逻辑。文章提出了「可行区间」这一概念——指那些在过去不具备经济可行性、但如今已值得开发或销售的软件产品范围。 这一经济格局的转变可能催生新一波利基软件产品和微型 SaaS 业务，而这些产品此前要么开发成本过高，要么市场规模太小难以商业化。与此同时，这也带来了竞争层面的隐忧：如果所有人的开发成本都降低了，竞争对手的入场门槛也随之下降，可能压缩整个软件行业的利润空间。 文章承认软件开发成本并未降至零——实际经验表明，要把任何东西做好，仍然需要在初始原型之外投入大量时间和反复迭代。文章指出，可销售软件的「可行区间」确实存在，但正在收窄并向更低价格区间移动，因为开发成本的降低同时也让更多竞争者得以进入任何细分市场。

hackernews · brandur · 6月21日 16:41 · [社区讨论](https://news.ycombinator.com/item?id=48620342)

**背景**: 「自建还是购买」是软件工程和商业战略中的经典难题：企业应该自主开发工具或系统，还是向供应商购买现成解决方案？历史上，定制软件高昂的开发成本和时间投入，促使大多数组织在核心业务之外倾向于购买现成产品。以大语言模型（LLM）驱动的代码助手为代表的 AI 辅助编程工具的兴起，正在通过大幅提升开发效率来改变这一格局。微型 SaaS 是指通常由一人或极小团队构建和运营、面向细分市场的小型软件即服务产品。

**社区讨论**: 评论者普遍认同 AI 工具降低了启动项目的门槛，但也指出在最初的热情过后，持续维护和打磨软件所需的动力和精力仍是真实存在的障碍。一个关键的反驳观点是：开发成本的降低是双刃剑——它同样降低了竞争者的入场门槛，意味着「可行区间」可能是在收窄而非单纯扩大。还有人强调了成熟软件产品所具备的社区效应和长尾功能开发的价值，这些是独立开发者难以复制的。

**标签**: `#software-economics`, `#build-vs-buy`, `#AI-assisted-development`, `#entrepreneurship`, `#product-strategy`

---

<a id="item-7"></a>
## [sqlite-utils 4.0rc1 新增数据库迁移与嵌套事务支持](https://simonwillison.net/2026/Jun/21/sqlite-utils-40rc1/#atom-everything) ⭐️ 6.0/10

Simon Willison 于 2026 年 6 月 21 日发布了 sqlite-utils 4.0rc1，这是其广受欢迎的 Python SQLite 库主要版本 v4 的首个候选发布版本。此 RC 引入了两项重要新功能：内置数据库迁移（移植自独立的 sqlite-migrate 包）以及通过保存点实现的嵌套事务支持。 sqlite-utils 在 Python 和数据工程社区中被广泛使用，将迁移功能直接内置到库中省去了对独立依赖包的需求，使 LLM、Datasette 等项目的数据库结构演进更加简便。主版本号的升级也标志着基于 SQLite 的 Python 工具生态系统日趋成熟。 新的迁移系统设计上刻意保持精简——不支持反向（回滚）迁移，这意味着出现错误时需要编写新的正向迁移来修复，而非回滚。嵌套事务通过 SQLite 的保存点（savepoints）实现，因为 SQLite 原生不支持嵌套的 BEGIN 语句块。

rss · Simon Willison · 6月21日 23:35

**背景**: sqlite-utils 是由 Simon Willison（同时也是 Datasette 的创建者）开发的 Python 库和命令行工具，在 Python 内置 sqlite3 模块之上提供了高级操作，例如从 JSON 数据自动创建表格和复杂的表结构转换。数据库迁移是一系列版本化脚本，用于随时间推移逐步演进数据库结构，使团队能够以受控方式跟踪和应用结构变更。SQLite 保存点（savepoints）是事务内的命名检查点，允许在不中止整个事务的情况下进行部分回滚，从而在不原生支持嵌套事务的数据库引擎中模拟嵌套事务功能。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://coddy.tech/docs/sqlite/savepoints">Runnable SQLite Docs: Savepoints | Coddy</a></li>
<li><a href="https://www.slingacademy.com/article/using-nested-transactions-to-simplify-complex-workflows-in-sqlite/">Using Nested Transactions to Simplify Complex Workflows in SQLite</a></li>

</ul>
</details>

**标签**: `#sqlite`, `#python`, `#database`, `#open-source`, `#datasette`

---

<a id="item-8"></a>
## [矩阵循环单元（MRU）更新：解决训练不稳定问题的注意力替代方案](https://www.reddit.com/r/MachineLearning/comments/1ubz5o8/an_update_on_matrix_recurrent_units_an_attention/) ⭐️ 6.0/10

一位研究者发布了矩阵循环单元（MRU）项目的更新，MRU 是一种线性时间序列架构，通过在序列维度上进行累积矩阵乘法来替代注意力机制。此次更新引入了多种新的输入状态矩阵构造方法——包括 LDU 分解、带矩阵指数/Cayley 映射的斜对称矩阵以及 QR 分解——以解决此前在非玩具数据集上出现的训练不稳定问题。 由于 Transformer 自注意力机制的计算复杂度随序列长度呈二次方增长，MRU 等线性时间替代方案对深度学习社区具有广泛吸引力，有助于实现高效的长上下文建模。尽管这是未经同行评审的独立研究，但它丰富了循环网络和状态空间模型替代注意力机制的生态系统，其对矩阵构造策略的实证分析也为探索类似架构的研究者提供了有价值的参考。 在所测试的方法中，LDU 分解（用向量元素填充下三角、对角和上三角因子，并通过对 D 施加激活函数来强制行列式为 1）取得了最佳性能；而通过 Cayley 映射或矩阵指数强制输入状态为正交矩阵，出人意料地损害了序列学习能力——这表明剪切变换对于模型独立调整状态至关重要。在更大的 TinyStories 数据集上，提前终止的训练结果显示 MRU 的表现不如同等规模的 GPT-2 风格 Transformer 基线。

reddit · r/MachineLearning · /u/mikayahlevi · 6月21日 19:39

**背景**: Transformer 模型依赖自注意力机制，该机制计算序列中所有词元对之间的关系，导致时间和内存复杂度为 O(n²)，在处理长序列时代价极高。这推动了线性时间替代方案的研究，例如状态空间模型（如 Mamba）和线性循环网络（如 RWKV），它们通过固定大小的隐藏状态来处理序列。并行扫描（也称关联扫描或前缀扫描）是一种经典的并行计算技术，利用运算的结合律，以 O(log n)的并行步骤而非 O(n)的顺序步骤计算累积结果，从而使循环式计算在现代 GPU 硬件上变得可行。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/mikayahlevi/mru-lm">GitHub - mikayahlevi/mru-lm: An LM forked from my transformer ...</a></li>
<li><a href="https://medium.com/data-science-collective/mambas-secret-weapon-the-mathematical-elegance-of-the-parallel-associative-scan-e9617f2644fa">Mamba’s Secret Weapon: The Mathematical Elegance of the Parallel Associative Scan | by DrSwarnenduAI | Data Science Collective | Medium</a></li>
<li><a href="https://medium.com/@dr.teck/efficient-alternatives-to-transformer-self-attention-397851f324ab">Efficient Alternatives to Transformer Self-Attention</a></li>

</ul>
</details>

**社区讨论**: 此次更新直接源于此前社区的反馈：一位评论者曾询问矩阵状态的约束策略，另一位则发现在更全面的数据集上训练存在不稳定性，研究者在本次更新中对这两个问题进行了系统性解答。这种讨论体现了 Reddit 上业余机器学习研究典型的协作迭代模式。

**标签**: `#sequence-modeling`, `#recurrent-networks`, `#attention-alternative`, `#linear-time-complexity`, `#deep-learning-architecture`

---

<a id="item-9"></a>
## [研究者发布无 Softmax 注意力模型，配备自定义 Triton 内核](https://www.reddit.com/r/MachineLearning/comments/1ubmybr/i_released_a_softmaxfree_attention_model_at_gpt2/) ⭐️ 6.0/10

一位研究者开源了一个无 Softmax 注意力模型，规模相当于 GPT-2 Medium（约 3.54 亿参数，在 115 亿 token 上训练），采用结构化稀疏性和跳块内核以降低长上下文推理时的显存占用。该发布包含开放权重和实现新型注意力机制的自定义 Triton GPU 内核。 标准注意力机制中的 Softmax 计算开销大、显存占用高，尤其在长上下文场景下更为突出，因此可行的替代方案有望显著降低当前限制消费级硬件进行长上下文推理的显存需求。同时开放权重和自定义内核，使研究社区能够直接对该方法进行基准测试并在此基础上继续研究。 该模型结合了结构化稀疏性与跳块内核技术——将 token 分组为块（tile），每个查询块仅关注所选的部分键块，跳过其余部分以节省计算量和显存。以现代标准衡量，约 3.54 亿参数的规模相对较小，且发布帖中未附带与标准注意力基线进行比较的公开基准测试结果。

reddit · r/MachineLearning · /u/NonGameCatharsis · 6月21日 10:46

**背景**: 标准 Transformer 注意力机制对所有 token 对的交互计算 Softmax，导致随序列长度增加，显存和计算量呈二次方增长——这是长上下文模型的主要瓶颈。无 Softmax 注意力用替代归一化方案（如ℓ1 范数）取代该操作，以实现更高效的计算，SOFT 和 SimA 等先前工作已对此进行了探索。Triton 是 OpenAI 开发的开源 GPU 编程语言，允许研究者用 Python 编写高性能的类 CUDA 自定义内核，使在 GPU 上高效实现新型注意力模式变得更加容易。注意力机制中的结构化稀疏性是指强制规定哪些 token 对之间发生交互的预设、对硬件友好的模式，而非计算全对全注意力。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://proceedings.neurips.cc/paper/2021/file/b1d10e7bafa4421218a51b1e1f1b0ba2-Paper.pdf">SOFT: Softmax-free Transformer with Linear Complexity Jiachen Lu1 Jinghan Yao1</a></li>
<li><a href="https://arxiv.org/abs/2206.08898">[2206.08898] SimA: Simple Softmax-free Attention for Vision Transformers</a></li>
<li><a href="https://openai.com/index/triton/">Introducing Triton: Open-source GPU programming for neural networks | OpenAI</a></li>

</ul>
</details>

**标签**: `#attention-mechanisms`, `#transformers`, `#triton-kernels`, `#long-context`, `#open-source`

---

<a id="item-10"></a>
## [Apertus – 面向主权 AI 的开放基础模型](https://apertvs.ai/) ⭐️ 5.0/10

Apertus 是一个旨在实现 AI 主权的开放基础模型项目，但由于进展缓慢、基础模型陈旧以及多语言任务可靠性不足等问题，社区对其持怀疑态度。

hackernews · T-A · 6月21日 21:29 · [社区讨论](https://news.ycombinator.com/item?id=48622778)

**标签**: `#open-source-ai`, `#LLM`, `#AI-sovereignty`, `#multilingual-models`, `#foundation-models`

---

<a id="item-11"></a>
## [个人网站的 JSON-LD 详解](https://hawksley.dev/blog/json-ld-explained-for-personal-websites/) ⭐️ 5.0/10

本文以通俗易懂的方式介绍了个人网站中 JSON-LD 结构化数据的使用方法。社区讨论中，不少人对其在 AI 生成搜索摘要时代的实际 SEO 价值提出了质疑。

hackernews · ethanhawksley · 6月21日 18:51 · [社区讨论](https://news.ycombinator.com/item?id=48621517)

**标签**: `#JSON-LD`, `#SEO`, `#structured-data`, `#web-development`, `#schema.org`

---

<a id="item-12"></a>
## [一个略有改进的 DVD-JEPA 演示 (P)](https://www.reddit.com/r/MachineLearning/comments/1ubtf09/a_slightly_improved_dvdjepa_demo_p/) ⭐️ 5.0/10

一位社区成员改进了一个简洁的 DVD-JEPA 演示，通过添加环境噪声和公平的像素空间基线对比，更好地展示了 JEPA 忽略无关环境细节的能力。

reddit · r/MachineLearning · /u/Kirne · 6月21日 15:49

**标签**: `#JEPA`, `#self-supervised-learning`, `#representation-learning`, `#deep-learning`, `#demo`

---

<a id="item-13"></a>
## [WeightsLab：面向神经网络训练的开源数据中心调试工具](https://www.reddit.com/r/MachineLearning/comments/1ubwcat/datacentric_debugging_for_teams_training_neural/) ⭐️ 5.0/10

GrayboxTech 对 WeightsLab 进行了重大升级，这是一款开源的、原生支持 PyTorch 的调试工具，允许机器学习工程师在训练过程中暂停运行、检查实时损失信号，并识别错误标注、类别不平衡和异常值等数据质量问题。该工具专为处理图像、视频和 LiDAR 点云数据的计算机视觉工程师而设计。 数据质量问题是导致模型性能不佳最常见却也最难发现的原因之一，诊断这些问题通常需要中断训练并手动筛查数据集。一款能在训练过程中实时发现这些问题的工具，可以为团队节省大量调试时间和计算资源。 WeightsLab 是开源项目，托管在 GrayboxTech 的 GitHub 仓库中，原生集成 PyTorch，并支持图像、视频和 LiDAR 点云等多种数据模态，覆盖范围比大多数仅专注于图像数据的调试工具更广。然而，该公告缺乏基准对比或有效性的量化证据，目前也没有可见的社区验证。

reddit · r/MachineLearning · /u/taranpula39 · 6月21日 17:47

**背景**: 以数据为中心的 AI 是一种强调提升训练数据质量和一致性的方法，而非单纯调整模型架构。神经网络训练的调试以困难著称，因为失败往往是无声的——模型可能在没有报错的情况下完成训练，却因错误标注或类别分布不均而表现不佳。LiDAR（激光雷达）点云是一种三维数据表示形式，常用于自动驾驶和机器人领域，深度学习模型需要处理不规则的稀疏空间数据。PyTorch 是目前最主流的两大深度学习框架之一（另一个是 TensorFlow），在学术研究和生产级机器学习系统中均被广泛使用。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://karpathy.github.io/2019/04/25/recipe/">A Recipe for Training Neural Networks</a></li>
<li><a href="https://ieeexplore.ieee.org/document/9173706">Deep Learning for LiDAR Point Clouds in Autonomous Driving: A ...</a></li>

</ul>
</details>

**标签**: `#machine-learning`, `#data-quality`, `#debugging`, `#computer-vision`, `#pytorch`

---

<a id="item-14"></a>
## [超越理性（免费的全面毁灭风格即时战略游戏）](https://www.beyondallreason.info/) ⭐️ 4.0/10

《超越理性》是一款免费开源的即时战略游戏，灵感来源于经典游戏《全面毁灭》。该游戏在技术质量上广受好评，但其玩家社区的 toxic 氛围也饱受批评。

hackernews · mosiuerbarso · 6月21日 11:38 · [社区讨论](https://news.ycombinator.com/item?id=48617990)

**标签**: `#gaming`, `#open-source`, `#RTS`, `#community`, `#nostalgia`

---

<a id="item-15"></a>
## [针对西班牙语专业词汇微调 Whisper 模型的最佳实践探讨](https://www.reddit.com/r/MachineLearning/comments/1ubvmdx/best_current_methods_for_finetuning_whisper_on/) ⭐️ 4.0/10

一位 Reddit 用户在 r/MachineLearning 社区发帖，寻求将 OpenAI 的 Whisper 语音识别模型针对西班牙语专业技术词汇进行微调的最佳实践。该帖子询问了所需的标注音频数据量，以及是否存在比 LoRA、QLoRA 和 Spectrum 更新或更有效的方法。 将 Whisper 等通用语音识别模型针对特定专业领域进行微调是一个普遍的实际挑战，尤其是对于西班牙语这类语言，其技术术语在训练数据中可能代表性不足。从事医疗转录、法律音频或工业应用等类似项目的从业者，都可以从高效适配技术的系统性指导中获益。 该用户特别关注如何可靠地识别西班牙语中的技术术语和专业词汇，并询问模型收敛通常需要多少小时的标注音频数据。他们已熟悉 LoRA、QLoRA 和 Spectrum 等参数高效微调方法，并希望了解是否存在更新或更优的替代方案。

reddit · r/MachineLearning · /u/gothenjoyer_ · 6月21日 17:18

**背景**: Whisper 是 OpenAI 开源的自动语音识别（ASR）模型，基于大量多语言音频数据训练而成，但在处理罕见技术术语或专业领域行话时可能表现欠佳。微调（Fine-tuning）是指利用额外的标注数据将预训练模型适配到特定任务或领域，而无需从头训练。LoRA（低秩适配）和 QLoRA（量化低秩适配）等参数高效微调（PEFT）方法通过仅训练模型参数的一小部分来降低显存和计算开销。Spectrum 是一种较新的 PEFT 方法，根据各层的信噪比（SNR）选择性地训练特定层，在某些基准测试中已被证明与全量微调相当，并优于 QLoRA。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://arxiv.org/abs/2305.14314">[2305.14314] QLoRA: Efficient Finetuning of Quantized LLMs</a></li>
<li><a href="https://huggingface.co/blog/anakin87/spectrum">Selective fine-tuning of Language Models with Spectrum</a></li>
<li><a href="https://arxiv.org/html/2406.06623v1">Spectrum: Targeted Training on Signal to Noise Ratio - arXiv.org</a></li>

</ul>
</details>

**标签**: `#whisper`, `#fine-tuning`, `#speech-recognition`, `#LoRA`, `#NLP`

---

<a id="item-16"></a>
## [LoRA 上的 EMA 应用？(讨论)](https://www.reddit.com/r/MachineLearning/comments/1ubv0f5/ema_on_lora_r/) ⭐️ 4.0/10

一位研究者询问是否有人在参数高效微调场景中，将 EMA 应用于 LoRA 适配器以实现自蒸馏（即以 EMA 模型作为教师的师生框架）。

reddit · r/MachineLearning · /u/South-Conference-395 · 6月21日 16:54

**标签**: `#LoRA`, `#EMA`, `#self-distillation`, `#PEFT`, `#LLM fine-tuning`

---