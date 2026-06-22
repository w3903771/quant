# 四框架对标覆盖映射 COVERAGE

> 用户要求：综述/指南需**完整覆盖** `reference/` 下 abu / QuantsPlaybook / stock / vnpy 的方法技术，做到**学完能自行读懂这 4 个项目**。本文件是完整性**验收清单**——写每章前查它，写完把对应行从 📋 翻成 ✅。
>
> 状态：📋 已入大纲(待写) ｜ ✅ 已写且覆盖 ｜ ⬜ 仍缺口
> 注：技术点的"原始方法出处"按 PLAN §2 动态检索原则，在写对应章时核验补入 references。

## 验收规则
- 每个框架的"技术点"必须能在指南某章学到其**原理 + 可运行实现思路**，或在综述某章读到其**原理与脉络**。
- 框架特有工程（如 vnpy 事件引擎、stock 数据管道）以指南 ch15/ch16 + 附录E 源码导读承接。
- 全部 📋 翻 ✅ 即视为"完整覆盖"达成。

---

## 1) abu（阿布量化）
| 技术点 | 承接章节 | 状态 |
|---|---|---|
| 择时买卖因子体系（解耦、事件驱动、基类/装饰器） | guide ch13.7(框架设计)、ch00/ch04；survey 11 | 📋 |
| ATR 止盈止损（移动/保护止盈） | guide ch04、ch13；survey 12 | 📋 |
| 选股因子（回归角度/极值/相似度Top-N） | guide ch03；survey 04 | 📋 |
| **头寸管理：Kelly / ATR 波动率仓位 / 最大仓位** | guide **ch13.5**；survey **12.2b** | 📋 |
| **滑点模型族** | guide **ch04.1b**；survey **11.1a** | 📋 |
| 手续费/成本（A股/美股/期货差异） | guide ch04.1；survey 11.1 | 📋 |
| 撮合/账户/资金曲线/benchmark | guide ch04；survey 11.1 | 📋 |
| 绩效度量（empyrical：Sharpe/IR/alpha-beta/回撤…） | guide ch04.2；survey 11.2 | 📋 |
| **UMP 机器学习交易拦截（主裁/边裁/KNN 非均衡）** | guide **ch05.5**；survey **5.6b** | 📋 |
| 特征/样本/分箱/ML 封装/交叉验证 | guide ch05；survey 05 | 📋 |
| **GA 遗传/进化参数寻优** | guide **ch04.5**；survey 04.4 | 📋 |
| 相似性/相关性选股 | guide ch08.2；survey 06.6 | 📋 |
| 技术指标/技术线（MA/MACD/RSI/BOLL/ATR/黄金分割/波浪/VWAP） | guide ch01.3；survey 02.4 | 📋 |
| 多市场数据（A股/美股/港股/期货/币） | guide ch0F/ch01；survey 02.2 | 📋 |
| K线图像 CNN 形态（DLBu 雏形） | guide ch07/ch08；survey 06 | 📋 |

## 2) QuantsPlaybook（研报复现集）
| 技术点 | 承接章节 | 状态 |
|---|---|---|
| 基本面：Piotroski F-Score、现金流选股 | guide ch03；survey 04 | 📋 |
| **行为/微观因子：STR凸显、聪明钱、APM、振幅、处置效应CGO、筹码CYQ、特质波动率、高频价量** | guide **ch03.5**；survey **4.1b** | 📋 |
| **网络因子：中心度、lead-lag 滞后网络** | guide **ch08.2**；survey 4.1b/06.6 | 📋 |
| **IPCA 工具化主成分** | guide **ch05.6**；survey **4.1c** | 📋 |
| **因子合成：等权/IC/半衰期IC/ICIR-协方差/ICIR-Ledoit** | guide **ch03.3**；survey **4.3** | 📋 |
| **规则/统计择时：RSRS/QRS、低延迟趋势、扩散、鳄鱼线、价量共振、牛熊线、形态** | guide ch01+复现；survey **3.6** | 📋 |
| **信号分解：小波、HHT(EMD/VMD)、高阶矩、时变夏普** | survey **7.2b**；guide ch07(选做) | 📋 |
| ML 择时（Trader-Company、SVM、HHT+分类） | guide ch05–06；survey 05 | 📋 |
| 排序学习 LGBMRanker（球队硬币因子） | guide **ch03.6**；survey 05.1 | 📋 |
| **PBO/CSCV 回测过拟合概率** | guide **ch04.4**；survey 11.3 | 📋 |
| **组合优化：DE 差分进化、HRP** | guide **ch13.6**；survey 03.4/12 | 📋 |
| 指数增强（自适应风控） | guide ch13；survey 12 | 📋 |
| 工具库（backtrader 模板/tear 绩效/vectorbt 绘图） | guide ch04；survey 13 | 📋 |
| MLT-TSMOM 多任务时序动量 | survey 06；guide ch07 | 📋 |

## 3) stock（A股多源工具集）
| 技术点 | 承接章节 | 状态 |
|---|---|---|
| 多源数据接入（tushare/akshare/掘金/futu/优矿） | guide **ch15.1**、ch0F/ch01；survey 02.2 | 📋 |
| **龙虎榜席位（游资/机构资金行为）** | guide **ch15.2**；survey 02.1 | 📋 |
| **大单/主力资金流、北向资金、股东户数、解禁** | guide **ch15.2**；survey 02.1 | 📋 |
| **打新（新股/科创板/打新基金/港股IPO）** | guide **ch15.3**；survey 02.1 | 📋 |
| **可转债（集思录、转债打新、折溢价、双低、LOF/ETF套利）** | guide **ch15.4**；survey 02.1 | 📋 |
| **涨跌停/封单/连板/一字板开板情绪** | guide **ch15.5**；survey 01.5/02.1 | 📋 |
| **股权质押风险因子** | guide **ch15.6**；survey 02.1 | 📋 |
| **数据管道：爬虫(requests/parsel/selenium)+MySQL/Mongo/ES+监控告警** | guide **ch15.7**、ch16；survey 13.3b | 📋 |
| **券商API实盘下单（ptrade/easytrader/逆回购）** | guide ch15.1/**ch16.3**；survey 13.3 | 📋 |
| K线技术形态（talib CDL）、多因子筛选 | guide ch01.3/ch03；survey 02.4/04 | 📋 |
| backtrader 回测、朴素贝叶斯滚动选股 | guide ch04.3/ch05；survey 11/05 | 📋 |
| 雪球策略验证（样本外复检） | guide ch04.4；survey 11.3 | 📋 |
| 实时监控告警（价格/转债阈值→邮件/微信/短信） | guide **ch15.7**；survey 13.3b | 📋 |

## 4) vnpy（事件驱动实盘平台）
| 技术点 | 承接章节 | 状态 |
|---|---|---|
| **事件驱动引擎（EventEngine/注册分发/定时器）** | guide **ch16.1**；survey 11.1/13.3b | 📋 |
| **交易对象模型 + OMS（Tick/Order/Trade/Position、vt_symbol）** | guide **ch16.2**；survey 13.3b | 📋 |
| **Gateway 抽象 + CTP/SimNow 接入 + 回调** | guide **ch16.3**；survey 13.3 | 📋 |
| **开平昨平今/净持仓制度（OffsetConverter）** | guide **ch04.1/ch16.2**；survey 11.1 | 📋 |
| CTA/组合/价差套利策略模板、回测↔实盘一致 | guide **ch16.4**、ch14；survey 11 | 📋 |
| 回测引擎（限价/停止单成交、盯市盈亏、绩效） | guide ch04；survey 11.1–11.2 | 📋 |
| 参数优化（穷举+遗传 DEAP、多进程） | guide ch04.5；survey 04.4 | 📋 |
| **算法交易 TWAP/Iceberg/Sniper/BestLimit** | guide **ch16.5**；survey 08.3/11.1b | 📋 |
| 期权交易（定价/IV曲面/希腊值） | guide ch16.7(了解)；survey 07/03 | 📋 |
| 风控 risk_manager（流控/前端限制） | guide **ch16.6**、ch13.3；survey 12.2 | 📋 |
| 数据库/datafeed（SQL/时序库/RQData/TuShare）、数据记录 | guide ch15.1/ch16；survey 02.2 | 📋 |
| vnpy.alpha（Alpha158/表达式引擎/ML 流水线，Qlib 启发） | guide ch03/ch06；survey 04.4/13 | 📋 |
| RPC 分布式 / K线图表 | guide ch16(延伸)；survey 13 | 📋 |

---

## 新增章节/小节汇总（因四框架对标而增）
- **guide 新增章**：`ch0F 金融地基`、`ch15 A股特色实务`(stock)、`ch16 事件驱动实盘`(vnpy)、`附录D 金融词典`、`附录E 框架源码导读`。
- **guide 新增小节**：ch03.3/3.5/3.6、ch04.1b/4.4/4.5、ch05.5/5.6、ch08.2、ch13.5/13.6/13.7。
- **survey 新增小节**：1.5(A股制度)、2.0(微观结构)、3.6(规则择时)、4.1b/4.1c/4.3、5.6b、7.2b、11.1a、12.2b、13.1b/13.3b。
