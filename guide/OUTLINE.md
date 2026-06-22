# 教学指南大纲 · d2l 风格的 Python 量化实战手册

> 对齐 https://d2l.ai/ ：每节"动机 → 直觉 → 数学 → 从零实现 → 框架实现 → 实验/可视化 → 小结 → 练习"。
> **双份代码**：**内嵌脚本**（md 内 teaching snippet，跟讲解走、不单独运行） + **完整脚本** `code/chXX/<slug>.py`（自身端到端可独立运行；"完整"≠"一个脚本产出整章结果"，一章常含多个完整脚本，按 `code/chXX/` 子目录归集；**随站点发布**，正文以链接指向，不在章末整体内嵌）。
> 运行环境：本目录独立 uv 环境（PLAN §4.2）。重依赖按章 `uv sync --group ...`。

约定：每章顶部含「本章你将学到 / 前置 / 本章新增依赖+安装命令 / 数据来源 / 对应综述章节 / **运行状态三态**(已实跑✅·仅静态检查🟦·环境受阻⬜)」。

> **金融知识约定（PLAN §4.3，用户重点）**：①每个技术章设**完整的「💡金融前置知识」一节**（不是便签），通俗类比 + 专业定义/公式/边界并重，**详尽、宁详勿略、0 基础可读**；②**技术与金融深度融合**——任何 ML/DL/RL/LLM 都按"解决什么金融问题→原理→每个量的金融含义→如何金融解读决策"来讲，严禁写成与金融无关的通用算法教程；③金融概念词典见 `附录D`，系统金融地基见 `ch0F`。
> **四框架对标（PLAN §8）**：本指南需完整覆盖 `reference/` 下 abu / QuantsPlaybook / stock / vnpy 的方法技术，验收清单见 `../COVERAGE_frameworks.md`，源码导读见 `附录E`。

## 🚩 全书贯穿红线清单（每个回测/评估都自查，前置到 ch00）
1. **下一bar成交**：信号用 t 收盘，成交记 t+1 开盘（杜绝未来函数）。
2. **成本占位**：任何回测含手续费+滑点（A股另加印花税/过户费），ch00 起即留占位参数。
3. **A股制度**：T+1、涨跌停不可成交、停牌跳过、ST 处理——在 ch04 做进引擎，前面章遇到先标注"ch04 修正"。
4. **防泄漏 CV**：截面/时序评估用 Purged/Embargo/CPCV（ch05 讲，ch03 先标注"此处未 purge"）。
5. **数据快照**：默认读 `data/snapshots/` 快照 + 记 as_of 日（PLAN §4.2），保可复现。

## 篇幅规划（轻/中/重）
| 章 | 篇幅 | 章 | 篇幅 |
|---|---|---|---|
| ch0F 金融地基(0基础·详尽) | **重** | ch08 Transformer/GNN | 中偏轻 |
| ch00 第一个策略 | 中 | ch09 强化学习 | **重** |
| ch01 数据处理 | **重** | ch10 时序基础模型 | **重(前沿)** |
| ch02 组合(瘦身) | 中 | ch11 大模型/另类 | **重(前沿)** |
| ch03 因子 | **重** | ch12 LLM Agent | **重(前沿)** |
| ch04 回测引擎 | **重** | ch13 组合风险实战 | **重** |
| ch05 ML预测 | **重** | ch14 端到端pipeline | **重** |
| ch06 GBDT/Qlib | **重** | ch15 A股特色实务〔stock〕 | **重** |
| ch07 DL时序 | 中 | ch16 事件驱动实盘〔vnpy〕 | **重** |
| 附录A-C | 中 | 附录D 金融词典 / E 框架导读 | **重/中** |
> **MVP 主线**（最先打通、全力实跑）：ch0F→ch00→ch01→ch03→ch04→ch06。**前沿(ch09–ch12)按用户指示为重点深入**：原理与方案讲透，能跑就实跑、跑不通诚实标 🟦/⬜，深度不打折。**ch15/ch16/附录D 为四框架对标的硬性覆盖项。**

---

## Part 0 · 预备与基石

### ch0F 金融市场与工具基础（0 基础地基章 · 详尽 · 通俗+专业）　【重】
> 全书金融地基，先于技术。**详尽**讲清"市场怎么运作、有哪些工具、钱怎么赚怎么亏"，通俗类比 + 专业定义/公式并重，不简略。
- 0F.1 一级/二级市场、交易所与撮合、连续竞价与集合竞价、做市与流动性
- 0F.2 账户与委托：限价/市价单、做多/做空、融资融券、T+0/T+1、订单生命周期
- 0F.3 价格与收益：开高低收、成交量、复权(前/后复权)、分红送转、算术vs几何/对数收益、年化与复利
- 0F.4 风险与收益的金融含义：波动率/方差/下行风险、回撤、风险溢价、无风险利率与折现、风险厌恶
- 0F.5 公司与估值：财报三表与关键科目、市值、PE/PB/PEG/EV、ROE 杜邦分解、成长vs价值
- 0F.6 工具谱系：股票/指数/ETF/LOF、可转债、期货(保证金/杠杆/展期)、期权(权利金/行权/希腊值直觉)
- 0F.7 参与者与生态：散户/公募/私募/外资/做市商；买方卖方；A股制度速览(承接综述1.5)
- 0F.8 从"金融问题"到"可计算问题"：本书后续技术如何回答这些金融问题（与各章呼应索引）
- 代码：`code/ch0F/finance_basics.py`（取数演示估值/复权/收益口径差异，可视化）
- 对应综述：01、附录D 详解词典

### ch00 环境、数据与你的第一个策略
- 0.1 量化全景与本书地图；收益率、对数收益、复利
- 0.2 uv 环境与运行方式；akshare/yfinance 取数第一课（A股+美股）
- 0.3 价格→收益→净值曲线；可视化
- 0.4 第一个可回测策略：均线交叉（从零实现最小回测；**用日频、不触发 T+1 的玩具形式**，含手续费占位+下一bar成交；完整版回测/绩效留 ch04，制度坑 ch04 讲透）
- 代码：`code/ch00/first_strategy.py`
- 对应综述：01

### ch01 金融数据处理与可视化
- 1.1 pandas 处理行情：索引、重采样、对齐、缺失/停牌
- 1.2 复权原理与实现；幸存者偏差与 point-in-time 直观演示
- 1.3 技术指标从零实现（MA/EMA/RSI/MACD/布林带）与向量化
- 1.4 横截面数据结构（多股票面板）、去极值/标准化/行业中性化
- 代码：`code/ch01/data_pipeline.py`、`code/ch01/indicators.py`
- 对应综述：02

### ch02 收益、风险与组合理论（瘦身版，避免早段过载）
- 2.1 期望收益、协方差、风险；多资产组合数学
- 2.2 均值-方差优化：解析解 + scipy 数值优化，画有效前沿（**从零，必做**）
- 2.3 最小方差 / 最大 Sharpe（从零）
- 〔风险平价、Ledoit-Wolf 收缩、Black-Litterman **上移到 ch13 实战**，消除与 ch13 重叠、降低本章坡度〕
- 代码：`code/ch02/meanvar.py`
- 对应综述：03（**ch02=组合理论基础**）

### ch03 因子与多因子模型
- 3.1 单因子：构造、分层回测、IC/RankIC/IR 从零计算（**标注"此处尚未 purge，ch05 修正"**；分层回测复用 ch00 玩具回测件，绩效全集留 ch04）
- 3.2 CAPM/Fama-French 回归（statsmodels）；因子暴露
- 3.3 多因子合成（**等权/IC加权/半衰期IC/最大化ICIR-协方差/最大化ICIR-Ledoit收缩**）、行业市值中性化〔QuantsPlaybook composition_factor〕
- 3.4 用 alphalens 做规范因子分析（框架实现）
- 3.5 **行为金融与微观结构因子**〔QuantsPlaybook〕：APM(隔夜/日间分离反转)、聪明钱、振幅隐藏结构、处置效应 CGO、筹码分布 CYQ——每个先讲行为金融成因再实现
- 3.6 **排序学习选股(Learning-to-Rank)**：用 LightGBM `lambdarank` 做截面排序（对照 QuantsPlaybook 球队硬币因子用 LGBMRanker）
- 代码：`code/ch03/single_factor.py`、`code/ch03/multifactor.py`、`code/ch03/behavioral_factors.py`
- 对应综述：04

### ch04 回测引擎与绩效评估
- 4.1 从零写事件驱动回测器：撮合、手续费、T+1/涨跌停约束；**期货开平昨平今/净持仓制度**注记〔vnpy OffsetConverter〕
- 4.1b **滑点模型族**〔abu SlippageBu〕：固定/比例/均价/冲击成本模型，从零实现并对比对绩效的影响
- 4.2 绩效指标全集实现：年化/波动/Sharpe/最大回撤/换手/胜率（基于 empyrical 思路从零）
- 4.3 框架实现：vectorbt 向量化回测 与 backtrader 事件驱动对照〔QuantsPlaybook hugos_toolkit / stock backtest〕
- 4.4 过拟合治理实验（**可跑**）：参数寻优"虚假最优"、walk-forward、**PBO/CSCV 回测过拟合概率 + Deflated Sharpe 从零实现**〔QuantsPlaybook CSCV/PBO〕、雪球策略验证式样本外复检
- 4.5 **参数寻优方法对比**：网格 vs **遗传/进化搜索(GA)**〔abu GridSearch、vnpy DEAP、QuantsPlaybook DE〕
- 代码：`code/ch04/backtester.py`、`code/ch04/metrics.py`、`code/ch04/slippage.py`、`code/ch04/pbo_dsr.py`
- 新增依赖：`uv sync --group backtest`（注意 numpy2/pandas3 兼容，必要时固定版本）
- 对应综述：11

## Part 1 · 机器学习量化

### ch05 用机器学习预测收益
- 5.1 把选股变监督学习：特征矩阵、标签(未来收益/分类)、横截面 vs 时序
- 5.2 时序交叉验证陷阱：Purged K-Fold / Embargo / CPCV 从零实现
- 5.3 线性/正则(Ridge/Lasso/ElasticNet)基线，IC 评估
- 5.4 防泄漏 pipeline 与特征重要性
- 5.5 **元标签与交易级信号拦截器(UMP 式)**〔abu UmpBu〕：在历史交易记录上训练分类器二次过滤信号（主裁=对订单特征学分类、边裁=KNN/距离的相似裁决）；López de Prado meta-labeling 落地
- 5.6 **IPCA（工具化主成分/条件因子模型）**简介〔QuantsPlaybook〕：让因子载荷随特征变化，承接综述 05.5
- 代码：`code/ch05/ml_pipeline.py`、`code/ch05/purged_cv.py`、`code/ch05/meta_labeling.py`
- 对应综述：05

### ch06 树模型、梯度提升与 Qlib 工作流
- 6.1 随机森林 → GBDT → XGBoost/LightGBM 原理与调参
- 6.2 截面选股实战：训练、滚动预测、构建多空组合并回测
- 6.3 Microsoft Qlib 工作流：数据、Alpha158/Alpha360、模型、回测一体化
- 6.4 Qlib 在 Windows/uv 的安装注记与最小可跑例
- 代码：`code/ch06/lgbm_stock.py`、`code/ch06/qlib_workflow.py`
- 新增依赖：`uv sync --group qlib`（版本兼容见章内注记）
- 对应综述：05、13

### ch07 深度学习时序模型（MLP/LSTM/GRU/TCN）
- 7.1 PyTorch 速通：张量、Dataset/DataLoader、训练循环（金融数据版）
- 7.2 滑窗样本构造；MLP 基线
- 7.3 LSTM/GRU 预测收益；TCN(时序卷积)
- 7.4 IC loss / 排序损失；过拟合治理；与 LightGBM 对比
- 代码：`code/ch07/torch_basics.py`、`code/ch07/lstm_tcn.py`
- 新增依赖：`uv sync --group dl`
- 对应综述：06、07

### ch08 Transformer 与图神经网络
- 8.1 注意力机制；PatchTST/iTransformer 思路与简化实现
- 8.2 股票关系图构建（相关性/行业/供应链）；**网络/图因子**〔QuantsPlaybook〕：股票网络中心度因子、隔夜-日间 lead-lag 滞后相关网络 + 聚类
- 8.3 GCN/GAT 截面关系建模最小实现
- 8.4 何时值得上 Transformer/GNN：与基线的诚实对比
- 代码：`code/ch08/transformer_ts.py`、`code/ch08/stock_gnn.py`
- 新增依赖：`uv sync --group dl`（GNN 视情况用 torch 自实现，避免 PyG 安装负担）
- 对应综述：06

## Part 2 · 进阶与前沿

### ch09 强化学习交易（FinRL）
- 9.1 交易作为 MDP：自定义 Gymnasium 环境（状态/动作/奖励/成本）
- 9.2 从零 DQN 直觉 → 用 stable-baselines3 跑 PPO
- 9.3 单标的择时 与 组合配置两类任务
- 9.4 FinRL 概览与最小例；奖励设计与过拟合陷阱
- 代码：`code/ch09/trading_env.py`、`code/ch09/ppo_trade.py`
- 新增依赖：`uv sync --group rl`
- 对应综述：08

### ch10 时序基础模型（zero-shot 预测）
> 写作前 WebSearch 核验模型现状与可用权重/接口。
- 10.1 基础模型范式：预训练 + zero/few-shot 时序预测
- 10.2 实操：Chronos / TimesFM / Lag-Llama 之一做 zero-shot 预测对比经典基线
- 10.3 局限：金融低信噪比下的现实表现、泄漏与评测
- 代码：`code/ch10/ts_foundation.py`
- 新增依赖：`uv sync --group dl nlp`（按所选模型）
- 对应综述：07、09

### ch11 大模型与另类数据（情绪 / 财报 NLP / LLM 因子）
> 写作前核验库与模型。
- 11.1 金融文本情绪：词典法 → FinBERT → LLM 抽取
- 11.2 用情绪/事件构造因子并回测其增量
- 11.3 用 LLM(API 或本地小模型)生成可解释信号的流程与防泄漏
- 代码：`code/ch11/sentiment_factor.py`
- 新增依赖：`uv sync --group nlp`
- 对应综述：09

### ch12 LLM Agent 量化系统
> 写作前核验编排框架与代表系统。
- 12.1 Agent 循环：工具(取数/回测/计算)、记忆、规划、反思
- 12.2 从零搭一个"研究助理"Agent：给定假设→取数→回测→产出报告
- 12.3 多 Agent 协作范式(分析/交易/风控/辩论)概念与最小演示
- 12.4 成本/延迟/幻觉/越权与人在回路；清醒的能力边界
- 代码：`code/ch12/research_agent.py`
- 对应综述：10

## Part 3 · 工程与实战

### ch13 组合优化与风险管理实战
- 13.1 从预测信号到目标持仓：带约束的组合优化(换手/行业/个股上限)
- 13.2 风险模型与协方差估计落地：**Ledoit-Wolf 收缩、风险平价、Black-Litterman（从 ch02 上移至此）**；风险预算
- 13.3 风控规则、回撤控制、业绩归因实战
- 13.4 模型监控与再训练节奏（衰减检测、walk-forward 上线）
- 13.5 **头寸规模(position sizing)**〔abu BetaBu〕：Kelly 公式、ATR/波动率目标仓位、配对仓位、最大仓位约束——逐笔头寸与组合权重的关系
- 13.6 **启发式组合优化**〔QuantsPlaybook〕：DE 差分进化(回撤最小目标)、HRP 层次风险平价——非凸/稳健优化
- 13.7 **因子/策略工程化框架设计模式**〔abu 买卖因子基类+装饰器、vnpy App 架构〕：可扩展、可注册、优化与策略解耦
- 代码：`code/ch13/portfolio_construction.py`、`code/ch13/position_sizing.py`
- 对应综述：12（**ch13=带约束实战**）

### ch14 完整 pipeline 与实盘工程
- 14.1 串起来：数据→因子/预测→组合→回测→归因 的端到端流水线
- 14.2 实盘鸿沟：实现差、容量、监控、再训练节奏
- 14.3 工程化：配置管理、复现、定时任务、纸上交易；走向实盘的清单
- 代码：`code/ch14/end_to_end.py`
- 对应综述：11、13、14

## Part 4 · A股实务与实盘工程（四框架对标，PLAN §8）

### ch15 A股特色数据与实务玩法　【重】〔对标 stock〕
> A股相对英文教材的"灵魂"，缺它读不懂 stock 仓库。每个玩法先讲金融/制度成因，再讲如何变信号/因子及其坑。
- 15.1 多源数据接入工程：tushare/akshare/baostock + 掘金/futu/优矿；API vs 爬虫双轨
- 15.2 事件/资金流另类数据：**龙虎榜**席位(游资/机构)、**大单/主力资金流**、**北向资金**、股东户数、解禁
- 15.3 **打新**：新股/科创板中签、打新基金筛选、开板时机
- 15.4 **可转债**：集思录数据、转债打新与折溢价、双低/下修博弈、LOF/ETF 折溢价套利
- 15.5 **涨跌停与情绪**：封单金额、连板强度、一字板开板、情绪周期
- 15.6 **股权质押**风险因子；事件驱动选股
- 15.7 数据管道工程：爬虫(requests/parsel/selenium)+ MySQL/MongoDB/ES 存储 + 实时监控告警(邮件/微信/钉钉)
- 代码：`code/ch15/longhubang_factor.py`、`code/ch15/kzz_arbitrage.py`、`code/ch15/data_pipeline.py`
- 对应综述：01.5、02.1、13

### ch16 事件驱动实盘交易系统　【重】〔对标 vnpy〕
> 从"回测脚本"跨到"实盘系统"。以 vnpy 为范本讲透事件驱动架构与实盘工程。
- 16.1 事件驱动架构：从零实现最小 EventEngine（事件队列+注册分发+定时器），再读 vnpy 对照
- 16.2 交易对象模型与 OMS：Tick/Bar/Order/Trade/Position、vt_symbol、订单生命周期、开平转换(today/yesterday)
- 16.3 Gateway 抽象与实盘接入：connect/subscribe/send_order/cancel + on_tick/on_order 回调；**CTP/SimNow 仿真**最小可跑例
- 16.4 策略模板：CTA(单标的)、portfolio(多标的)、spread(价差套利)；同代码回测↔仿真↔实盘一致
- 16.5 **订单执行算法**：TWAP/Iceberg/Sniper/BestLimit 拆单（呼应综述 08.3/11.1b 最优执行）
- 16.6 实盘风控：交易流控、下单量/撤单数前端限制；断线重连、对账
- 16.7 期权/价差延伸：IV 曲面与希腊值跟踪（option_master，了解级）
- 代码：`code/ch16/event_engine.py`、`code/ch16/ctp_demo.py`（🟦 仿真环境受限时标注）
- 对应综述：11、13

## 附录
- A. 数学预备：线性代数 / 概率统计 / 最优化 / 随机过程（按需点查）
- B. 资源清单：书 / 课 / 框架 / 数据 / 社区（与 survey/references.md 互链）
- C. 常见报错与环境兼容（numpy2/pandas3、Qlib、torch on Windows）
- **D. 金融概念详解词典**（0 基础前置，通俗+专业并重、详尽）：承接 ch0F，逐条详解账户/委托/撮合/做多做空/融资融券/复权/分红/估值PE-PB/财报三表/指数ETF/可转债/期货期权/保证金/无风险利率/A股制度等，各章「金融前置框」回链此处
- **E. 四框架源码导读对照**：把书中知识点反向链接到 abu / QuantsPlaybook / stock / vnpy 的关键源文件，给"读这个知识点→去看哪个框架哪段代码"的对照表（与 `../COVERAGE_frameworks.md` 互补）

---
## Kaggle 取材对照（代码范式来源，详见 references.md K 类）
| Kaggle 竞赛 | ✅迁移什么(与数据解耦的可学范式) | ❌不迁移什么(弃用) | 用于章节 |
|---|---|---|---|
| Jane Street Market Prediction / Real-Time | 防泄漏时序 CV、三重门/元标签思路、GBDT+NN 集成框架 | 匿名特征逆向、私榜专用效用目标、魔法常数 | ch05、ch06、ch07 |
| Two Sigma Financial Modeling | 截面建模流程、稳健回归、特征中性化 | 该赛特有的匿名因子定义 | ch03、ch05 |
| Optiver Realized Volatility Prediction | 已实现波动率/订单簿特征构造思路 | 依赖其专有高频数据的具体管线 | ch07（+综述07波动率） |
| Optiver - Trading at the Close | 集合竞价/撮合与标签设计思想 | 该赛盘口数据格式的硬编码 | ch04、ch06 |
| Two Sigma: Using News to Predict | 新闻情绪→收益的另类数据流水线骨架 | 其专有新闻数据 schema | ch11 |
> **改编规则（PLAN §4.1/§2）**：①注明来源竞赛+notebook；②用 A股/通用数据重写为可独立运行；③可检查准则——**魔法常数须有数据驱动来源否则删；禁止用全样本统计量做特征**；④脚本注释标注"剔除了什么"。

---
### 写作顺序（MVP 主线优先，与 PLAN §6 一致）
里程碑1（MVP核心闭环，先冒烟测试）：**ch0F**→ch00→ch01→ch03→ch04→ch06（+ch05 防泄漏）｜ 里程碑2（组合/风控+A股实务）：ch02、ch13、ch14、**ch15** ｜ 里程碑3（DL/时序）：ch07、ch08 ｜ **里程碑4（强化学习与前沿·重点深入）：ch09、ch10、ch11、ch12** ｜ 里程碑5（实盘系统+前瞻+收尾）：**ch16**、附录A–E(含金融词典D/框架导读E/前沿趋势)
> 注：ch0F 金融地基随里程碑1 先行；ch15(A股实务)、ch16(实盘系统) 为四框架对标新增；附录D 金融词典与正文金融前置框同步增补。
