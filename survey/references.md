# 参考资料库 references

统一编号，正文用 `[Rxx]` 引用。状态：🟦 经典可信（凭知识可直接引用）｜✅ 已 WebSearch 核验｜⬜ 待核验（2023+ 前沿，落笔前必须核验名称/年份/机构/主张）。

> 引用不限论文：含书籍、框架文档、开源仓库、课程、权威博客。

## A. 经典理论与因子（🟦 经典可信）
- [R01] 🟦 Markowitz, H. (1952). *Portfolio Selection*. Journal of Finance.
- [R02] 🟦 Sharpe, W. (1964). *Capital Asset Prices* (CAPM). Journal of Finance.
- [R03] 🟦 Ross, S. (1976). *Arbitrage Pricing Theory* (APT).
- [R04] 🟦 Fama, E. & French, K. (1993). *Common risk factors in stock and bond returns* (三因子).
- [R05] 🟦 Fama, E. & French, K. (2015). *A five-factor asset pricing model*.
- [R06] 🟦 Carhart, M. (1997). *On Persistence in Mutual Fund Performance* (四因子/动量).
- [R07] 🟦 Jegadeesh, N. & Titman, S. (1993). *Returns to Buying Winners and Selling Losers* (动量).
- [R08] 🟦 Black, F. & Litterman, R. (1992). *Global Portfolio Optimization*.
- [R09] 🟦 Ledoit, O. & Wolf, M. (2004). *Honey, I Shrunk the Sample Covariance Matrix* (协方差收缩).

## B. 时间序列与波动率（🟦）
- [R10] 🟦 Engle, R. (1982). *ARCH*.
- [R11] 🟦 Bollerslev, T. (1986). *GARCH*.
- [R12] 🟦 Tsay, R. *Analysis of Financial Time Series* (教材).
- [R56] 🟦 Almgren, R. & Chriss, N. (2000). *Optimal Execution of Portfolio Transactions*（最优执行闭式解，配 11.1b/08.3）。

## C. 机器学习/金融 ML（🟦/✅）
- [R13] 🟦 López de Prado, M. (2018). *Advances in Financial Machine Learning* (三重门/元标签/CPCV/PBO/DSR).
- [R14] 🟦 López de Prado, M. (2020). *Machine Learning for Asset Managers*.
- [R15] 🟦 Gu, S., Kelly, B. & Xiu, D. (2020). *Empirical Asset Pricing via Machine Learning*. RFS.
- [R16] 🟦 Grinold, R. & Kahn, R. *Active Portfolio Management* (IR/信息准则/Alpha).
- [R17] 🟦 Jansen, S. *Machine Learning for Algorithmic Trading* (2nd ed., 实战教材).
- [R18] 🟦 Chan, E. *Quantitative Trading* / *Algorithmic Trading* (实战).
- [R54] 🟦 Harvey, C., Liu, Y. & Zhu, H. (2016). *…and the Cross-Section of Expected Returns*. RFS（**多重检验**，因子"动物园"显著性通胀，配 04.2/11.3）。
- [R55] 🟦 Bailey, D. & López de Prado, M. (2014). *The Deflated Sharpe Ratio*；Bailey, Borwein, López de Prado & Zhu (2014/2017). *The Probability of Backtest Overfitting (PBO)*（11.3 过拟合治理原始来源）。

## D. 公式化 Alpha 与因子库（🟦/✅）
- [R19] 🟦 Kakushadze, Z. (2016). *101 Formulaic Alphas* (WorldQuant Alpha101).
- [R20] ⬜ 国泰君安 *GTJA191* 因子（来源/版本待核验）。
- [R57] ⬜ 石川等《因子投资：方法与实践》(2020) + 华泰/广发证券金工"多因子系列"研报（A股因子实证，落笔前核验具体篇目）。

## E. 框架与开源仓库（✅ 以官方仓库为准）
- [R21] ✅ Microsoft **Qlib** — github.com/microsoft/qlib （AI 量化平台，Alpha158/360）。
- [R22] ✅ **FinRL** / AI4Finance — github.com/AI4Finance-Foundation/FinRL （金融强化学习）。
- [R23] ✅ **alphalens(-reloaded)** — 因子绩效分析。
- [R24] ✅ **vectorbt** / **backtrader** / **zipline** / **Backtesting.py** — 回测框架。
- [R25] ✅ **akshare** / **tushare** / **baostock** — A股数据接口。
- [R26] ✅ **stable-baselines3** / **Gymnasium** — RL 库。

## F. 深度学习时序（🟦/⬜）
- [R27] ⬜ Informer / Autoformer / **PatchTST** / iTransformer（长序列预测，逐篇核验年份作者）。
- [R28] ⬜ 金融图神经网络代表工作（如关系建模 RSR/HATS 等，待核验）。
- [R29] 🟦 TabNet（Arik & Pfister, 2019/2021，表格深度学习）。

## G. 大模型 / 金融 LLM（⬜ 全部待核验：名称/年份/机构/主张）
- [R30] ⬜ **BloombergGPT** (2023, Bloomberg) — 金融领域 LLM。
- [R31] ⬜ **FinGPT** (AI4Finance) — 开源金融 LLM 框架。
- [R32] ⬜ **PIXIU / FinMA** — 金融 LLM 指令微调与基准。
- [R33] ⬜ **FinBERT** — 金融情绪预训练模型（核验版本/作者）。
- [R34] ⬜ 中文金融 LLM（如 XuanYuan 轩辕 等）— 待核验。

## H. 时序基础模型（⬜ 待核验）
- [R35] ⬜ **TimeGPT** (Nixtla)。
- [R36] ⬜ **Lag-Llama**。
- [R37] ⬜ **TimesFM** (Google)。
- [R38] ⬜ **Chronos** (Amazon)。
- [R39] ⬜ **Moirai** (Salesforce)。

## I. LLM Agent 量化（⬜ 待核验）
- [R40] ⬜ **TradingAgents** — 多 Agent 交易（辩论范式）。
- [R41] ⬜ **FinMem** — 带记忆的金融交易 Agent。
- [R42] ⬜ **FinAgent** — 多模态金融 Agent。
- [R43] ⬜ 自动化因子/策略挖掘 Agent（AlphaGPT 等）。
- [R44] ⬜ 编排框架：LangGraph / AutoGen / CrewAI（文档为准）。

## K. Kaggle 竞赛与公开 notebook（✅ 竞赛已核验，notebook 逐条补链接）
> 一等代码/工程范式来源。改编入指南时注明来源并用 A股/通用数据重写（PLAN §2、§4.1）。
- [R45] ✅ **Jane Street Market Prediction** (2020–2021) — 高频/中频信号、特征匿名化、效用最大化目标、严格防泄漏 CV。kaggle.com/competitions/jane-street-market-prediction
- [R46] ✅ **Jane Street Real-Time Market Data Forecasting** (2024) — 时序 responders 预测、在线评测。kaggle.com/competitions/jane-street-real-time-market-data-forecasting
- [R47] ✅ **Optiver Realized Volatility Prediction** (2021) — 高频订单簿/成交特征、已实现波动率建模。kaggle.com/competitions/optiver-realized-volatility-prediction
- [R48] ✅ **Optiver - Trading at the Close** (2023) — 收盘集合竞价预测、撮合与标签设计。kaggle.com/competitions/optiver-trading-at-the-close
- [R49] ✅ **Two Sigma: Using News to Predict Stock Movements** (2018) — 新闻情绪 → 收益，另类数据范式。kaggle.com/competitions/two-sigma-financial-news
- [R50] ✅ **Two Sigma Financial Modeling Challenge** (2016–2017) — 匿名因子截面建模。
- [R51] 🟦 **G-Research Crypto Forecasting** (2021–2022)、**Ubiquant Market Prediction** (2022)、**JPX Tokyo Stock Exchange Prediction** (2022) — 截面收益预测范式（落笔前可再核验细节）。

## J. 网络资料 / 课程 / 社区（✅ 逐条补链接）
- [R52] ✅ d2l.ai —《动手学深度学习》（本指南风格对齐对象）。
- [R53] ⬜ 量化社区/博客（聚宽、米筐、QuantStart、Quantopian 遗产文档等）逐条补。

## L. 对标框架（本工程 `reference/`，需完整覆盖，见 `COVERAGE_frameworks.md`）
- [R58] ✅ **abu(阿布量化 abupy)** — 择时买卖因子体系、Kelly/ATR 仓位管理、滑点模型、UMP 机器学习交易拦截(主裁/边裁)、GA 参数寻优、多市场。`reference/abu/`
- [R59] ✅ **QuantsPlaybook**(hugo2046) — 券商金工研报复现集：基本面/因子构建/择时/组合优化 + hugos_toolkit/SignalMaker。`reference/QuantsPlaybook/`
- [R60] ✅ **stock** — A股+港股+可转债+基金多源数据/分析/回测/ML 工具集，含龙虎榜/打新/可转债/质押/大单监控。`reference/stock/`
- [R61] ✅ **vnpy(vn.py)** — 事件驱动实盘交易平台：EventEngine/Gateway/OMS、CTA/组合/价差/算法/期权策略、CTP 接入、vnpy.alpha。`reference/vnpy/`

## M. 框架涉及的具名方法（⬜ 写到对应章时按"动态检索"核验原始出处再引用）
> 来自四框架盘点，落笔前 WebSearch 核验作者/年份/出处，勿凭印象。
- [R62] ⬜ **RSRS** 阻力支撑相对强度择时（光大证券金工研报，核验报告名/年份）。
- [R63] ⬜ **Piotroski F-Score**（Piotroski 2000, 财务质量打分）。
- [R64] ⬜ **HRP 层次风险平价**（López de Prado 2016）。
- [R65] ⬜ **IPCA 工具化主成分**（Kelly, Pruitt & Su 2019/2020）。
- [R66] ⬜ **Kelly 准则**（Kelly 1956）。
- [R67] ⬜ **凸显理论 STR / salience**（Bordalo, Gennaioli & Shleifer）、**APM/聪明钱/处置效应CGO/筹码CYQ** 等行为/微观因子（多为中文研报，逐一核验来源）。
- [R68] ⬜ **HHT(EMD)**（Huang et al. 1998）、**VMD**（Dragomiretskiy & Zosso 2014）。

---
> 维护规则：写每章时，新增引用追加到对应分类并给编号；2023+ 项必须先核验再从 ⬜ 升级到 ✅，核验失败则删除或明确标注存疑。
