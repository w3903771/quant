# 量化投资 · 教学指南

[← 量化首页](/) ｜ [技术综述](/survey/)

> 一份**可运行的 Python 量化教学指南**：动手实现、跑得通，强调「原理 + 公式 + 可运行代码」三位一体。所有代码在本地运行（PyTorch + 真实数据），结果图表作为静态图嵌入正文，无需在线执行。

本指南是配套技术综述的「怎么做」之书；想先建立全局认知、理解「为什么」，请看 [量化技术综述 ↗](/survey/)。

## 怎么用这本书

- 每章先讲清**金融含义**，再讲**数学与代码**；技术一律「结合金融」来讲。
- 代码有两份形态：正文里的**讲解片段** + 每章独立子目录 `guide/code/chXX/` 下的**可独立运行完整脚本**（随站点发布，可在线查看/下载）。
- 数据采用「**快照优先**」范式（首次拉取落盘，默认读快照），保证可复现。

## 完整目录

> **图例**：✅ **蓝色链接** = 已发布（可点击）；⬜ <span style="color:#9aa0a6">灰色 = 计划中，陆续发布</span>。

**Part 0 · 预备与基石**

- ✅ [ch0F 金融市场与工具基础](ch0F_金融市场与工具基础.md) —— 零基础金融地基：市场与撮合、账户与委托、复权与收益口径、风险与估值、工具谱系、A股现行制度（含可运行演示）。
- ⬜ <span style="color:#9aa0a6">ch00 环境、数据与你的第一个策略</span>
- ⬜ <span style="color:#9aa0a6">ch01 金融数据处理与可视化</span>
- ⬜ <span style="color:#9aa0a6">ch02 收益、风险与组合理论</span>
- ⬜ <span style="color:#9aa0a6">ch03 因子与多因子模型</span>
- ⬜ <span style="color:#9aa0a6">ch04 回测引擎与绩效评估</span>

**Part 1 · 机器学习量化**

- ⬜ <span style="color:#9aa0a6">ch05 用机器学习预测收益（特征/标签/时序CV）</span>
- ⬜ <span style="color:#9aa0a6">ch06 树模型、梯度提升与 Qlib 工作流</span>
- ⬜ <span style="color:#9aa0a6">ch07 深度学习时序模型（MLP/LSTM/GRU/TCN）</span>
- ⬜ <span style="color:#9aa0a6">ch08 Transformer 与图神经网络</span>

**Part 2 · 进阶与前沿**

- ⬜ <span style="color:#9aa0a6">ch09 强化学习交易（FinRL）</span>
- ⬜ <span style="color:#9aa0a6">ch10 时序基础模型（zero-shot 预测）</span>
- ⬜ <span style="color:#9aa0a6">ch11 大模型与另类数据（情绪 / 财报 NLP / LLM 因子）</span>
- ⬜ <span style="color:#9aa0a6">ch12 LLM Agent 量化系统</span>

**Part 3 · 工程与实战**

- ⬜ <span style="color:#9aa0a6">ch13 组合优化与风险管理实战</span>
- ⬜ <span style="color:#9aa0a6">ch14 完整 pipeline 与实盘工程</span>

**Part 4 · A股实务与实盘工程**

- ⬜ <span style="color:#9aa0a6">ch15 A股特色数据与实务玩法〔对标 stock〕</span>
- ⬜ <span style="color:#9aa0a6">ch16 事件驱动实盘交易系统〔对标 vnpy〕</span>

**附录**

- ⬜ <span style="color:#9aa0a6">A 数学预备 ／ B 资源清单 ／ C 常见报错与环境兼容 ／ D 金融概念详解词典 ／ E 四框架源码导读对照</span>

!!! warning "免责声明"
    本书为个人学习笔记，内容仅供学习研究，**不构成任何投资建议**。市场是对抗性的，任何回测曲线默认假设其过拟合，直到被严格证伪。
