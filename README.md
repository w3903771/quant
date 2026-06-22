# 量化投资 · 综述与教学指南

> 个人学习用工程。两份互补产物：一份**详尽中文技术综述**（看脉络、看原理、看全局地图），一份**可运行的 Python 教学指南**（动手实现、跑得通，强调"原理 + 公式 + 可运行代码"三位一体）。

## 范围与定位（已确认）

| 维度 | 选择 |
|---|---|
| 市场/数据 | **A 股为主 + 通用原理**（akshare / tushare / baostock / Microsoft Qlib 生态；同时讲清不依赖市场的通用原理） |
| 代码形态 | **可运行 + 真实数据框架**（Qlib、akshare、yfinance、vectorbt/backtrader、PyTorch、FinRL 等；对齐 d2l 的可执行风格） |
| 综述深度 | **详尽深度综述**（覆盖完整技术脉络：传统 ML → 深度学习 → 时序/概率 → 强化学习 → 大模型 → Agent） |
| 语言 | 中文（保留必要英文术语与库名） |
| 目的 | 给自己看 / 自学，不投稿；引用不限于论文，可含书籍、框架文档、博客、开源仓库 |

## 目录结构

```
E:\Programming\Python\project\other\quantification\   # 项目根（2026-06-21 由 ai-paper/study/quantification 迁来）
├── README.md            # 本文件：总索引 + 进度追踪
├── PLAN.md              # 主规划：路线图、引用策略、写作约定、协作流程、发布工具链(§9)
├── DEPLOY.md            # 发布与部署手册（MkDocs+GitHub Pages：域名/DNS/HTTPS/多学科）
├── pyproject.toml       # 独立 uv 量化环境依赖（核心 + 分组重依赖 + docs 组）
├── mkdocs.guide.yml     # 指南站 MkDocs 配置（构建 /guide/）
├── mkdocs.survey.yml    # 综述站 MkDocs 配置（构建 /survey/）
├── home/index.html      # 学科首页（quant.ebook.ttzg.site 根，列出两本书）
├── .github/workflows/   # deploy.yml：构建两书→合并→GitHub Pages
├── .gitignore           # 忽略 .venv / 数据缓存 / _site 构建产物
├── .venv/               # uv 虚拟环境（不提交）
├── COVERAGE_frameworks.md     # 四框架对标覆盖验收清单（学完能读懂它们）
├── REVIEW_panel_2026-06-21.md # 5 人面板评审纪要
├── reference/           # 你引入的 4 个量化框架源码：abu / QuantsPlaybook / stock / vnpy
├── survey/              # 【产物一】中文技术综述  → 发布为 /survey/
│   ├── index.md         # 站点首页（封面）
│   ├── OUTLINE.md       # 综述详细大纲（内部规划，不发布）
│   ├── 00_导读.md
│   ├── 01_*.md ...      # 逐章
│   ├── js/mathjax.js    # 数学渲染配置
│   └── references.md    # 参考资料库（论文/书籍/框架/网络资料，含核验状态）
└── guide/               # 【产物二】可运行的 Python 教学指南  → 发布为 /guide/
    ├── index.md         # 站点首页（封面）
    ├── OUTLINE.md       # 指南详细大纲（内部规划，不发布）
    ├── ch00_*.md ...    # 逐章（md 内含片段代码 + 指向 code/ 的完整脚本）
    ├── js/mathjax.js    # 数学渲染配置
    ├── code/            # 每节的可独立运行完整脚本/notebook（chXX_<slug>.py，不发布）
    └── data/            # 示例缓存数据（gitignore）
```

**运行环境**：独立 uv 项目，已实测可用（Python 3.11.11 / pandas 3.0 / numpy 2.4 / sklearn 1.9 / xgboost / lightgbm / akshare / yfinance）。在本目录下用 `uv run python guide/code/chXX_xxx.py` 运行；重依赖按里程碑 `uv sync --group dl|rl|nlp|backtest|qlib` 安装。详见 PLAN §4.2。

## 进度追踪（Progress Tracker）

> 每完成一个单元就在此打勾；跨会话续作时先读此表。状态：⬜ 未开始 / 🟨 进行中 / ✅ 完成

### 规划层（里程碑 0 ✅ 完成）
- ✅ 范围确认（市场/代码/深度/uv环境/双份代码）
- ✅ 独立 uv 量化环境搭建并实测核心依赖
- ✅ README + PLAN + survey/OUTLINE + guide/OUTLINE + references 骨架
- ✅ Kaggle 纳入一等代码/引用来源（PLAN §2/§4.1、references K 类、guide 对照表）
- ✅ **5 人面板评审 + 落实 P0+P1 修订**（见 `REVIEW_panel_2026-06-21.md`）
- ✅ **执行策略=MVP 主线优先**（先打通 ch00→ch01→ch03→ch04→ch06 + 综述 01/02/04/11）
- ✅ **修正：强化学习与前沿(综述08-10/14、指南ch09-12)仍为"重点·深入"，含前瞻技术与趋势**（不降级，运行风险用三态纪律处理）
- ✅ **金融知识=通俗+专业、详尽、与技术深度融合**（新增 `ch0F 金融地基章` + `附录D 金融词典`，每章设完整「金融前置」节；技术一律"结合金融"讲，PLAN §4.3）
- ✅ **动态检索贯穿全程**：每章写作时现做检索，不限 outline 阶段文献（PLAN §2）
- ✅ **四框架对标覆盖**（abu / QuantsPlaybook / stock / vnpy）：新增 guide `ch0F/ch15(A股实务)/ch16(实盘系统)/附录D-E` + 综述/指南多处小节；验收清单见 `COVERAGE_frameworks.md`（PLAN §8）
- ✅ **发布工具链定型（2026-06-22）**：MkDocs+Material；学科进子域名、一学科一仓库、指南/综述为同站 `/guide/`·`/survey/` 路径区（`quant.ebook.ttzg.site`）；配置与手册已落地（`mkdocs.*.yml` / `home/` / `DEPLOY.md` / `.github/workflows/deploy.yml`）。**正式产物不提 "d2l"**（仅编写期内部参照）

> **里程碑 1 进行中**：①✅ **地基库联调冒烟测试完成**（vectorbt/pyqlib/quantstats/polars 主栈可用；alphalens 系与 pandas3 不兼容 → ch03 走「从零 + qlib 评估」；详见 PLAN §4.2）；② 下一步：写 `ch0F 金融地基` + 指南 ch00 + 综述 01。

### 综述（survey/）
- ✅ 00 导读与全书地图
- ⬜ 01 量化投资全景与简史
- ⬜ 02 数据与特征工程（A股数据生态 / 三大偏差）
- ⬜ 03 经典金融工程基石（EMH/CAPM/APT/组合优化）
- ⬜ 04 因子投资与 Alpha 挖掘
- ⬜ 05 传统机器学习方法
- ⬜ 06 深度学习方法
- ⬜ 07 时间序列与概率建模
- ⬜ 08 强化学习与量化
- ⬜ 09 大语言模型与量化
- ⬜ 10 LLM Agent 与自主量化
- ⬜ 11 回测、评估与过拟合治理
- ⬜ 12 风险管理与组合构建
- ⬜ 13 行业生态与平台
- ⬜ 14 挑战、局限与前沿展望
- ⬜ references.md 充实与核验

### 指南（guide/）
- ⬜ ch0F 金融市场与工具基础（0基础地基·详尽）
- ⬜ ch00 环境、数据与第一个策略
- ⬜ ch01 金融数据处理与可视化
- ⬜ ch02 收益、风险与组合理论
- ⬜ ch03 因子与多因子模型
- ⬜ ch04 回测引擎与绩效评估
- ⬜ ch05 机器学习预测收益（特征/标签/时序CV）
- ⬜ ch06 树模型与梯度提升（Qlib 工作流）
- ⬜ ch07 深度学习时序模型（LSTM/GRU/TCN）
- ⬜ ch08 Transformer 与图神经网络
- ⬜ ch09 强化学习交易（FinRL）
- ⬜ ch10 时序基础模型（TimesFM/Chronos/PatchTST）
- ⬜ ch11 大模型与另类数据（情绪/财报 NLP/LLM 因子）
- ⬜ ch12 LLM Agent 量化系统
- ⬜ ch13 组合优化与风险管理实战
- ⬜ ch14 完整 pipeline 与实盘工程
- ⬜ ch15 A股特色数据与实务玩法〔对标 stock〕
- ⬜ ch16 事件驱动实盘交易系统〔对标 vnpy〕
- ⬜ 附录 A-C / D 金融词典 / E 四框架源码导读

## 使用方式建议
- **想建立全局认知、理解"为什么"** → 读 `survey/`
- **想动手实现、跑代码、掌握"怎么做"** → 读 `guide/`
- 两者章节大致一一呼应（见 PLAN.md 的对照表），可对照阅读。
