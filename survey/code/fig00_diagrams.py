"""survey 00 导读 —— 两张定调图（替代原 ASCII 图，扛窄屏）。

综述面向读者**不贴代码**：本脚本只是制图工具，经 mkdocs `exclude_docs: code/` 不发布，
仅把生成的 PNG（survey/img/00/）嵌入正文。

运行（仓库根目录）：
    uv run python survey/code/fig00_diagrams.py
依赖：matplotlib（环境已含）。无随机性、无网络，确定性可复现。
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


def _find_repo_root(start: Path) -> Path:
    for p in [start, *start.parents]:
        if (p / "pyproject.toml").exists():
            return p
    return start.parents[-1]


IMG_DIR = _find_repo_root(Path(__file__).resolve()) / "survey" / "img" / "00"
IMG_DIR.mkdir(parents=True, exist_ok=True)

TEAL = "#0f8b8d"  # 与综述站 primary(teal) 呼应


def fig_pipeline() -> None:
    """五环节流水线：数据→信号→组合→执行→风控 + 顶部贯穿'评估/回测/归因'。"""
    fig, ax = plt.subplots(figsize=(9.6, 4.2)); ax.axis("off")
    stages = [
        ("① 数据", "行情/基本面\n另类/文本", "#e8f3f3"),
        ("② 预测·信号", "因子、ML、DL\nRL、LLM", "#d6ebec"),
        ("③ 组合构建", "优化、风险\n预算、约束", "#c3e3e4"),
        ("④ 交易执行", "下单、滑点\n冲击、T+1", "#b0dbdc"),
        ("⑤ 风险控制", "回撤、敞口\n失效监控", "#9dd3d4"),
    ]
    n = len(stages); x0, w, gap = 0.0, 1.55, 0.45
    centers = []
    for i, (title, sub, color) in enumerate(stages):
        x = x0 + i * (w + gap)
        cx = x + w / 2; centers.append(cx)
        ax.add_patch(plt.Rectangle((x, 0.5), w, 1.25, fc=color, ec=TEAL, lw=1.4, zorder=2))
        ax.text(cx, 1.42, title, ha="center", va="center", fontsize=11, fontweight="bold", zorder=3)
        ax.text(cx, 0.92, sub, ha="center", va="center", fontsize=8.5, color="#333", zorder=3)
        if i < n - 1:
            ax.annotate("", xy=(x + w + gap, 1.1), xytext=(x + w, 1.1),
                        arrowprops=dict(arrowstyle="-|>", lw=1.6, color="#555"))
    # 顶部贯穿带 + 引导虚线
    left, right = centers[0] - w / 2, centers[-1] + w / 2
    ax.add_patch(plt.Rectangle((left, 2.25), right - left, 0.5, fc="#fff3cd", ec="#d4a017", lw=1.4, zorder=2))
    ax.text((left + right) / 2, 2.5, "评估 / 回测 / 归因（贯穿全程，防自欺的免疫系统）",
            ha="center", va="center", fontsize=10.5, fontweight="bold", zorder=3)
    for cx in centers:
        ax.plot([cx, cx], [1.75, 2.25], ls=":", color="#d4a017", lw=1.0, zorder=1)
    ax.text((left + right) / 2, 0.18, "方法在变，骨架不变——这是阅读全书的主线",
            ha="center", va="center", fontsize=9.5, color=TEAL, style="italic")
    ax.set_xlim(left - 0.3, right + 0.3); ax.set_ylim(0, 2.95)
    fig.tight_layout(); fig.savefig(IMG_DIR / "pipeline.png", dpi=130); plt.close(fig)
    print(f"  [图] {IMG_DIR / 'pipeline.png'}")


def fig_evolution() -> None:
    """技术脉络演化链：规则→…→Agent，强调'叠加而非替代'。"""
    nodes = [
        ("规则/技术分析", "人定规则"),
        ("统计套利", "协整/配对(典型)"),
        ("线性因子模型", "Fama-French"),
        ("传统机器学习", "GBDT/XGB"),
        ("深度学习", "LSTM/Tfm/GNN"),
        ("强化学习", "序贯决策(MDP)"),
        ("大模型 LLM", "文本/时序基模"),
        ("LLM Agent", "自主研究闭环"),
    ]
    fig, ax = plt.subplots(figsize=(13.5, 3.4)); ax.axis("off")
    n = len(nodes); w, gap = 1.4, 0.32
    for i, (name, sub) in enumerate(nodes):
        x = i * (w + gap); cx = x + w / 2
        shade = "#e8f3f3" if i % 2 == 0 else "#d0e8e9"
        ax.add_patch(plt.Rectangle((x, 0.7), w, 0.95, fc=shade, ec=TEAL, lw=1.3, zorder=2))
        ax.text(cx, 1.34, name, ha="center", va="center", fontsize=9.5, fontweight="bold", zorder=3)
        ax.text(cx, 0.95, sub, ha="center", va="center", fontsize=7.8, color="#444", zorder=3)
        if i < n - 1:
            ax.annotate("", xy=(x + w + gap, 1.175), xytext=(x + w, 1.175),
                        arrowprops=dict(arrowstyle="-|>", lw=1.5, color="#888"))
    total = n * (w + gap) - gap
    ax.text(total / 2, 0.28,
            "叠加而非替代：每一步为解决上一步的某个局限而出现，但前者并未消失——"
            "2026 实战里 GBDT 仍是 Alpha 预测主力，DL/LLM/Agent 是特定场景的增量",
            ha="center", va="center", fontsize=9, color="#b00", style="italic")
    ax.text(total / 2, 2.05, "环节② 预测/信号 的技术演化（事后整理的叙事，非唯一/必然路径）",
            ha="center", va="center", fontsize=10.5, fontweight="bold", color=TEAL)
    ax.set_xlim(-0.3, total + 0.3); ax.set_ylim(0, 2.3)
    fig.tight_layout(); fig.savefig(IMG_DIR / "evolution.png", dpi=130); plt.close(fig)
    print(f"  [图] {IMG_DIR / 'evolution.png'}")


def main() -> None:
    print("survey 00 导读 · 制图")
    fig_pipeline()
    fig_evolution()
    print("完成 →", IMG_DIR)


if __name__ == "__main__":
    main()
