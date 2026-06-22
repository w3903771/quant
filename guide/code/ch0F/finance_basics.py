"""ch0F 金融市场与工具基础 —— 配套可运行脚本。

本脚本把 ch0F 里"用一句话说不清、但一算就懂"的三件事做成可复现的演示：
  1) 复权（除权除息后如何还原真实收益）——为什么"不复权"会把分红/送股看成暴跌；
  2) 收益口径（简单 / 对数 / 算术平均 / 几何平均 / 年化 / 波动拖累）——它们差在哪、何时用哪个；
  3) 估值与风险的基本量（市值/EPS/BPS/PE/PB/ROE 杜邦分解，波动率/下行波动/最大回撤/夏普/索提诺）。

设计取向：
  - 核心演示用**自洽的合成数据**，保证**离线、可复现、永远跑通**（达「已实跑 ✅」不依赖联网）；
  - 末尾附一个**可选的 akshare 真实数据**小例（带快照兜底），无网络时友好跳过，正式范式留给 ch01。

运行环境：本仓库独立 uv 环境（Python 3.11 / numpy 2.4 / pandas 3.0 / matplotlib）。
运行命令（在仓库根目录）：
    uv run python guide/code/ch0F/finance_basics.py
依赖：numpy、pandas、matplotlib（核心演示）；akshare（仅可选真实数据小例，缺了不影响主流程）。
运行状态：已实跑 ✅（见 ch0F 正文「运行状态」与本文件末尾的实测输出摘要）。
"""
from __future__ import annotations

import sys
from pathlib import Path

# Windows 默认 GBK 控制台无法输出部分字符；统一用 UTF-8，保证中文/数学符号不崩
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import numpy as np
import pandas as pd

import matplotlib

matplotlib.use("Agg")  # 无界面后端：CI / 无显示器也能出图
import matplotlib.pyplot as plt

# 中文显示（Windows 常见字体；缺字体则回退，不影响数值结果）
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

RNG = np.random.default_rng(20260622)  # 固定随机种子，保证可复现


def _find_repo_root(start: Path) -> Path:
    """向上找含 pyproject.toml 的目录作为仓库根——脚本移到任何子目录都无需改路径。"""
    for p in [start, *start.parents]:
        if (p / "pyproject.toml").exists():
            return p
    return start.parents[-1]


REPO_ROOT = _find_repo_root(Path(__file__).resolve())
GUIDE_DIR = REPO_ROOT / "guide"
IMG_DIR = GUIDE_DIR / "img" / "ch0F"  # 发布到站点的教学图目录（每章独立子目录）
IMG_DIR.mkdir(parents=True, exist_ok=True)

TRADING_DAYS = 252  # A股年化常用交易日数


def section(title: str) -> None:
    print("\n" + "=" * 64 + f"\n{title}\n" + "=" * 64)


# ---------------------------------------------------------------------------
# 1) 复权：除权除息后如何还原真实收益
# ---------------------------------------------------------------------------
def demo_adjustment() -> pd.DataFrame:
    """构造一段含「现金分红」与「10 送 10 送股」的行情，演示三种价格口径。

    口径：
      不复权(raw)  —— 交易所原样打印的收盘价，除权日有"假跳空"；
      后复权(hfq)  —— 以最早一天为锚，向后把分红/送股按再投资还原，序列连续，反映**真实总收益**；
      前复权(qfq)  —— 以最新一天为锚（=当前真实价格），把历史价向下还原，画近端图最直观。
    """
    raw = np.array([10.0, 10.2, 10.5, 10.3, 10.6, 9.7, 9.9, 10.1, 5.15, 5.25])
    n = len(raw)

    # 公司行为：第 5 天每股现金分红 1.0 元（除息）；第 8 天 10 送 10（每股拆成 2 股，价格约减半）
    cash_div = np.zeros(n)
    cash_div[5] = 1.0
    split = np.ones(n)
    split[8] = 2.0  # 当日 1 股 → 2 股

    # 持有人的"真实日收益因子" g_t：把当天落袋的现金分红、拆股后的股数都算进财富
    #   普通日:        g = raw_t / raw_{t-1}
    #   除息日(分红 D): g = (raw_t + D) / raw_{t-1}        —— 价格虽跌，但拿到了现金
    #   送股日(拆 s 倍): g = (raw_t * s) / raw_{t-1}        —— 价格虽减半，但股数翻倍
    g = np.ones(n)
    for t in range(1, n):
        g[t] = (raw[t] * split[t] + cash_div[t]) / raw[t - 1]

    hfq = np.empty(n)  # 后复权：最早一天锚定为 raw[0]，向后累乘真实收益因子
    hfq[0] = raw[0]
    for t in range(1, n):
        hfq[t] = hfq[t - 1] * g[t]
    qfq = hfq * (raw[-1] / hfq[-1])  # 前复权：整体缩放使最新一天 = 当前真实价格

    df = pd.DataFrame(
        {"不复权": raw, "现金分红": cash_div, "送股倍数": split,
         "真实日收益%": (g - 1) * 100, "后复权": hfq, "前复权": qfq}
    )
    df.index.name = "交易日"

    ret_raw = raw[-1] / raw[0] - 1            # 不复权"总收益"——既漏掉分红，又被送股扭曲成暴跌
    ret_adj = hfq[-1] / hfq[0] - 1            # 复权后的真实总收益
    section("1) 复权：除权除息后还原真实收益")
    with pd.option_context("display.float_format", lambda x: f"{x:8.4f}"):
        print(df.to_string())
    print(f"\n  不复权口径的'总收益' = {ret_raw:+.2%}   ← 把 10送10 看成了腰斩，严重失真")
    print(f"  复权后的真实总收益   = {ret_adj:+.2%}   ← 含分红再投资、剔除送股影响，才是持有人真实赚到的")
    print("  结论：算收益/做回测/喂模型，一律用复权价；不复权价只用于看'当时盘面真实成交价'。")

    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(df.index, df["不复权"], "o--", color="#888", label="不复权(交易所原始价)")
    ax.plot(df.index, df["后复权"], "o-", color="#1f77b4", label="后复权(锚最早,反映真实总收益)")
    ax.plot(df.index, df["前复权"], "s-", color="#d62728", label="前复权(锚最新=当前价)")
    ax.axvline(5, color="green", ls=":", alpha=.6)
    ax.text(5, ax.get_ylim()[1] * .96, " 除息 现金分红1.0", color="green", fontsize=9)
    ax.axvline(8, color="purple", ls=":", alpha=.6)
    ax.text(8, ax.get_ylim()[1] * .80, " 10送10", color="purple", fontsize=9)
    ax.set_xlabel("交易日"); ax.set_ylabel("价格"); ax.set_title("三种价格口径：不复权 vs 前/后复权")
    ax.legend(loc="center left", fontsize=9); ax.grid(alpha=.3)
    fig.tight_layout(); fig.savefig(IMG_DIR / "ch0F_fuquan.png", dpi=130); plt.close(fig)
    print(f"  [图] {IMG_DIR / 'ch0F_fuquan.png'}")
    return df


# ---------------------------------------------------------------------------
# 2) 收益口径：简单/对数、算术/几何平均、年化、波动拖累
# ---------------------------------------------------------------------------
def demo_returns() -> dict:
    section("2) 收益口径：简单 vs 对数、算术 vs 几何、年化、波动拖累")

    # 合成一年日度简单收益：正漂移 + 适中波动（贴近股票量级）
    daily_simple = RNG.normal(loc=0.0009, scale=0.013, size=TRADING_DAYS)
    nav = np.cumprod(1 + daily_simple)          # 净值曲线（初始 1.0）
    total_return = nav[-1] - 1

    daily_log = np.log1p(daily_simple)           # 对数收益 = ln(1+简单收益)
    # 关键性质：对数收益**可加**——逐日相加即得区间对数收益；简单收益不可加
    assert np.isclose(daily_log.sum(), np.log(nav[-1]))

    arith_mean = daily_simple.mean()             # 算术平均（高估长期增长）
    geo_mean = nav[-1] ** (1 / TRADING_DAYS) - 1 # 几何平均（与终值一致，才是真实复利速度）
    # 年化：几何复利年化收益 与 波动率年化（sqrt 法则）
    ann_return = (1 + geo_mean) ** TRADING_DAYS - 1
    ann_vol = daily_simple.std(ddof=1) * np.sqrt(TRADING_DAYS)
    # 波动拖累(volatility drag)：几何 ≈ 算术 − 方差/2
    drag = arith_mean - geo_mean
    drag_approx = 0.5 * daily_simple.var(ddof=0)

    print(f"  全年累计(总)收益       = {total_return:+.2%}   (= 终值/初值 - 1)")
    print(f"  日算术平均收益         = {arith_mean:+.4%}   ← 简单求平均，**高估**长期增长")
    print(f"  日几何平均收益         = {geo_mean:+.4%}   ← 与终值自洽，才是真实复利速度")
    print(f"  波动拖累 = 算术 − 几何 = {drag:.4%}  ≈ 方差/2 = {drag_approx:.4%}  (二者吻合)")
    print(f"  年化收益(几何)         = {ann_return:+.2%}")
    print(f"  年化波动率(sqrt252)    = {ann_vol:.2%}")
    print(f"  对数收益可加性自检：逐日对数收益之和 = ln(终值)  →  {daily_log.sum():.4f} == {np.log(nav[-1]):.4f}")

    # 图：算术 vs 几何 复利外推 —— 同一个'平均'，多年后差距被复利放大
    years = np.arange(0, 11)
    fig, ax = plt.subplots(figsize=(7.6, 4.2))
    ax.plot(years, (1 + ann_return) ** years, "o-", color="#1f77b4",
            label=f"按几何年化 {ann_return:.1%} 复利(真实)")
    arith_ann = (1 + arith_mean) ** TRADING_DAYS - 1
    ax.plot(years, (1 + arith_ann) ** years, "s--", color="#d62728",
            label=f"按算术年化 {arith_ann:.1%} 复利(高估)")
    ax.set_xlabel("年"); ax.set_ylabel("净值(初始=1)")
    ax.set_title("算术平均 vs 几何平均：复利下的差距被逐年放大")
    ax.legend(fontsize=9); ax.grid(alpha=.3)
    fig.tight_layout(); fig.savefig(IMG_DIR / "ch0F_return_measures.png", dpi=130); plt.close(fig)
    print(f"  [图] {IMG_DIR / 'ch0F_return_measures.png'}")
    return {"daily_simple": daily_simple, "nav": nav, "ann_return": ann_return, "ann_vol": ann_vol}


# ---------------------------------------------------------------------------
# 3) 风险的基本量：波动率/下行波动/最大回撤/夏普/索提诺
# ---------------------------------------------------------------------------
def demo_risk(daily_simple: np.ndarray, nav: np.ndarray, rf_annual: float = 0.02) -> None:
    section("3) 风险的金融含义：波动率、下行波动、最大回撤、夏普、索提诺")

    rf_daily = (1 + rf_annual) ** (1 / TRADING_DAYS) - 1
    excess = daily_simple - rf_daily

    vol = daily_simple.std(ddof=1) * np.sqrt(TRADING_DAYS)                     # 总波动（上下都算）
    # 下行偏差（target semideviation，标准 Sortino 口径）：只罚低于 MAR(此处取无风险利率) 的部分，
    # 分母用**全样本期数 T**（达标日记 0），故 dd ≤ 总波动；分母若改用"负收益个数"会得到">总波动"的反常值。
    downside_diff = np.minimum(daily_simple - rf_daily, 0.0)
    dd_daily = np.sqrt((downside_diff ** 2).mean())                            # 日度下行偏差
    downside_dev = dd_daily * np.sqrt(TRADING_DAYS)                            # 年化下行波动
    sharpe = excess.mean() / daily_simple.std(ddof=1) * np.sqrt(TRADING_DAYS)  # 夏普：每单位总波动的超额收益
    sortino = excess.mean() / dd_daily * np.sqrt(TRADING_DAYS)                 # 索提诺：每单位下行波动的超额收益（分母更小→通常 > 夏普）

    peak = np.maximum.accumulate(nav)            # 历史最高净值
    drawdown = nav / peak - 1                     # 回撤序列（≤0）
    mdd = drawdown.min()                          # 最大回撤
    mdd_at = int(drawdown.argmin())

    print(f"  年化波动率(总)         = {vol:.2%}    ← 上行下行一起算，刻画整体颠簸")
    print(f"  年化下行波动率         = {downside_dev:.2%}    ← 只罚低于无风险利率的部分(分母=全样本T)，≤ 总波动")
    print(f"  最大回撤(MDD)          = {mdd:.2%}  (第 {mdd_at} 个交易日触及谷底)")
    print(f"  夏普比率(rf={rf_annual:.0%})       = {sharpe:.2f}    ← 每单位总波动换来的超额收益")
    print(f"  索提诺比率(rf={rf_annual:.0%})     = {sortino:.2f}    ← 每单位下行波动换来的超额收益(分母更小→＞夏普)")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 5.0), sharex=True,
                                   gridspec_kw={"height_ratios": [2, 1]})
    ax1.plot(nav, color="#1f77b4", label="净值")
    ax1.plot(peak, color="#aaa", ls="--", label="历史高点")
    ax1.set_ylabel("净值"); ax1.set_title("净值曲线与回撤"); ax1.legend(fontsize=9); ax1.grid(alpha=.3)
    ax2.fill_between(np.arange(len(drawdown)), drawdown * 100, color="#d62728", alpha=.5)
    ax2.axhline(mdd * 100, color="#d62728", ls=":", label=f"最大回撤 {mdd:.1%}")
    ax2.set_ylabel("回撤(%)"); ax2.set_xlabel("交易日"); ax2.legend(fontsize=9); ax2.grid(alpha=.3)
    fig.tight_layout(); fig.savefig(IMG_DIR / "ch0F_nav_drawdown.png", dpi=130); plt.close(fig)
    print(f"  [图] {IMG_DIR / 'ch0F_nav_drawdown.png'}")

    # 收益分布直方图：一图说清"波动=离散度、下行只看左尾、近正态假设"三件事。
    # 用同一套 density 直方图，按是否低于 MAR(无风险利率) 给每个柱上色，避免两套密度基准误导。
    from matplotlib.patches import Patch
    fig, ax = plt.subplots(figsize=(7.6, 4.0))
    counts, edges = np.histogram(daily_simple * 100, bins=30, density=True)
    centers = (edges[:-1] + edges[1:]) / 2
    thr = rf_daily * 100                                    # MAR 阈值（低于它即下行）
    bar_colors = ["#d62728" if c < thr else "#9ecae1" for c in centers]
    ax.bar(centers, counts, width=(edges[1] - edges[0]) * 0.95, color=bar_colors, edgecolor="white")
    mu, sd = daily_simple.mean() * 100, daily_simple.std(ddof=1) * 100
    xs = np.linspace(daily_simple.min() * 100, daily_simple.max() * 100, 200)
    ax.plot(xs, np.exp(-(xs - mu) ** 2 / (2 * sd ** 2)) / (sd * np.sqrt(2 * np.pi)),
            color="#333", lw=1.5)
    ax.axvline(mu, color="#1f77b4", ls="--")
    ax.legend(handles=[Patch(fc="#9ecae1", label="日收益分布"),
                       Patch(fc="#d62728", label="下行区(< 无风险利率)"),
                       plt.Line2D([], [], color="#333", lw=1.5, label="正态对照"),
                       plt.Line2D([], [], color="#1f77b4", ls="--", label=f"均值 {mu:.3f}%")], fontsize=8)
    ax.set_xlabel("日收益(%)"); ax.set_ylabel("概率密度")
    ax.set_title("收益分布：波动是离散度，下行风险只罚左尾"); ax.grid(alpha=.3)
    fig.tight_layout(); fig.savefig(IMG_DIR / "ch0F_return_dist.png", dpi=130); plt.close(fig)
    print(f"  [图] {IMG_DIR / 'ch0F_return_dist.png'}")


# ---------------------------------------------------------------------------
# 4) 估值：市值/EPS/BPS/PE/PB/ROE 与杜邦分解
# ---------------------------------------------------------------------------
def demo_valuation() -> None:
    section("4) 公司与估值：PE/PB/ROE 与杜邦分解")
    # 一家"教科书公司"的年报（数值刻意取整，便于看清恒等关系）
    revenue = 100e8      # 营业收入
    net_income = 8e8     # 净利润
    assets = 120e8       # 总资产
    equity = 50e8        # 净资产(股东权益)
    shares = 10e8        # 总股本(股)
    price = 12.0         # 每股股价

    mktcap = price * shares
    eps = net_income / shares          # 每股收益
    bps = equity / shares              # 每股净资产
    pe = price / eps                   # 市盈率
    pb = price / bps                   # 市净率
    roe = net_income / equity          # 净资产收益率

    # 杜邦三分解：ROE = 净利率 × 资产周转率 × 权益乘数
    net_margin = net_income / revenue
    asset_turnover = revenue / assets
    equity_multiplier = assets / equity

    print(f"  总市值 = 价 × 股本      = {mktcap/1e8:.0f} 亿元")
    print(f"  EPS(每股收益)          = {eps:.2f} 元    BPS(每股净资产) = {bps:.2f} 元")
    print(f"  PE(市盈率) = 价/EPS     = {pe:.1f} 倍   ← 按当前盈利'回本'要多少年(静态直觉)")
    print(f"  PB(市净率) = 价/BPS     = {pb:.2f} 倍   ← 为每 1 元净资产付了多少钱")
    print(f"  ROE(净资产收益率)      = {roe:.1%}   ← 股东每 1 元本金一年赚回多少")
    print(f"  恒等关系自检：PB = PE × ROE  →  {pe:.1f} × {roe:.1%} = {pe*roe:.2f}  == PB {pb:.2f}")
    print("  杜邦分解  ROE = 净利率 × 资产周转率 × 权益乘数")
    print(f"           {roe:.1%} = {net_margin:.1%} × {asset_turnover:.3f} × {equity_multiplier:.1f}"
          f"  (验算 {net_margin*asset_turnover*equity_multiplier:.1%})")
    print("  金融含义：同样的 ROE，可由'高毛利'(白酒)、'高周转'(零售)或'高杠杆'(银行)驱动，风险含义大不同。")


# ---------------------------------------------------------------------------
# 5) 可选：akshare 真实数据小例（带快照兜底；无网络则友好跳过）
# ---------------------------------------------------------------------------
def demo_real_data_optional(symbol: str = "600519") -> None:
    section("5) [可选] akshare 真实复权数据小例（快照兜底；正式范式见 ch01）")
    snap_dir = GUIDE_DIR / "data" / "snapshots"
    snap_dir.mkdir(parents=True, exist_ok=True)
    snap = snap_dir / f"akshare_{symbol}_qfq_ch0F.parquet"

    try:
        if snap.exists():
            df = pd.read_parquet(snap)
            print(f"  读快照：{snap.name}（{len(df)} 行）")
        else:
            import akshare as ak  # 仅在需要联网时才导入，缺库不影响主流程
            df = ak.stock_zh_a_hist(symbol=symbol, period="daily",
                                    start_date="20240101", end_date="20240630", adjust="qfq")
            df.to_parquet(snap)
            print(f"  已联网拉取并落盘快照：{snap.name}（{len(df)} 行，as_of=数据获取日）")
        col = "收盘" if "收盘" in df.columns else df.columns[-1]
        print(f"  {symbol} 前复权收盘价：首 {df[col].iloc[0]:.2f} → 末 {df[col].iloc[-1]:.2f}"
              f"  区间收益 {df[col].iloc[-1]/df[col].iloc[0]-1:+.2%}")
    except Exception as e:  # 无网络 / 无 akshare / 接口变更：友好跳过，不影响 ✅
        print(f"  [跳过] 真实数据小例不可用（{type(e).__name__}: {str(e)[:80]}）。")
        print("        核心演示(1–4)均为离线合成数据，不受影响；真实取数+快照的完整范式见 ch01。")


# ---------------------------------------------------------------------------
# 6) 概念示意图：集合竞价撮合 / 订单生命周期 / 成本拆解 / 期权到期损益
#    （这些概念纯文字最难想象，用图把"机制"一眼讲清）
# ---------------------------------------------------------------------------
def fig_call_auction() -> None:
    """集合竞价：为何按'可成交量最大'的价格统一撮合。"""
    prices = np.array([9.8, 9.9, 10.0, 10.1, 10.2, 10.3])
    cum_buy = np.array([100, 85, 70, 50, 30, 12])   # 价越低想买的越多（需求向下）
    cum_sell = np.array([10, 28, 50, 68, 85, 100])  # 价越高想卖的越多（供给向上）
    matched = np.minimum(cum_buy, cum_sell)          # 每个价格的可成交量
    k = int(matched.argmax())                        # 最大成交量原则 → 集合竞价成交价
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.step(prices, cum_buy, where="mid", color="#d62728", marker="o", label="累计买单(需求)")
    ax.step(prices, cum_sell, where="mid", color="#1f77b4", marker="s", label="累计卖单(供给)")
    ax.axvline(prices[k], color="green", ls="--")
    ax.scatter([prices[k]], [matched[k]], color="green", zorder=5)
    ax.text(prices[k] + 0.02, matched[k] + 5, f"成交价 {prices[k]:.1f}\n成交量 {matched[k]}(最大)",
            color="green", fontsize=9)
    ax.set_xlabel("申报价格"); ax.set_ylabel("累计申报量(手)")
    ax.set_title("集合竞价：取'可成交量最大'的价格统一清算")
    ax.legend(fontsize=9); ax.grid(alpha=.3)
    fig.tight_layout(); fig.savefig(IMG_DIR / "ch0F_call_auction.png", dpi=130); plt.close(fig)
    print(f"  [图] {IMG_DIR / 'ch0F_call_auction.png'}")


def fig_order_lifecycle() -> None:
    """订单生命周期状态机：报单 → 已报 → 撮合 →（全部/部分/未成交）→ 撤单/失效。"""
    fig, ax = plt.subplots(figsize=(8.6, 3.6)); ax.axis("off")

    def box(x, y, text, color):
        ax.add_patch(plt.Rectangle((x - 0.6, y - 0.33), 1.2, 0.66, fc=color, ec="#333", lw=1.2, zorder=2))
        ax.text(x, y, text, ha="center", va="center", fontsize=9, zorder=3)

    def arrow(x1, y1, x2, y2):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", lw=1.3, color="#555"))

    box(0.0, 1.5, "报单", "#fde0dd"); box(1.7, 1.5, "已报\n(交易所接收)", "#fff7bc")
    box(3.4, 1.5, "撮合", "#deebf7")
    box(5.3, 2.5, "全部成交", "#c7e9c0"); box(5.3, 1.5, "部分成交", "#c7e9c0")
    box(5.3, 0.5, "未成交", "#f0f0f0"); box(7.4, 1.0, "撤单/失效", "#fdd0a2")
    arrow(0.6, 1.5, 1.1, 1.5); arrow(2.3, 1.5, 2.8, 1.5)
    arrow(4.0, 1.6, 4.7, 2.4); arrow(4.0, 1.5, 4.7, 1.5); arrow(4.0, 1.4, 4.7, 0.6)
    arrow(5.9, 1.45, 6.8, 1.1); arrow(5.9, 0.5, 6.8, 0.95)
    ax.set_xlim(-0.8, 8.2); ax.set_ylim(0, 3.1)
    ax.set_title("一笔订单的生命周期（A股，简化）")
    fig.tight_layout(); fig.savefig(IMG_DIR / "ch0F_order_lifecycle.png", dpi=130); plt.close(fig)
    print(f"  [图] {IMG_DIR / 'ch0F_order_lifecycle.png'}")


def fig_cost_breakdown() -> None:
    """一笔交易成本拆解：买入 10 万 + 卖出 10 万（合计成交 20 万）。"""
    items = ["佣金\n(双边≈万2.5)", "印花税\n(卖出0.05%)", "过户费\n(双边0.001%)"]
    costs = [50, 50, 2]
    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    bars = ax.bar(items, costs, color=["#1f77b4", "#d62728", "#2ca02c"])
    for b, c in zip(bars, costs):
        ax.text(b.get_x() + b.get_width() / 2, c + 1, f"{c} 元", ha="center", fontsize=10)
    ax.set_ylabel("成本(元)")
    ax.set_title(f"一笔交易成本拆解：买卖各 10 万，合计 {sum(costs)} 元 ≈ 单边万 5")
    ax.grid(alpha=.3, axis="y")
    fig.tight_layout(); fig.savefig(IMG_DIR / "ch0F_cost_breakdown.png", dpi=130); plt.close(fig)
    print(f"  [图] {IMG_DIR / 'ch0F_cost_breakdown.png'}")


def fig_option_payoff() -> None:
    """期权到期损益：买入 call/put 的'最大损失=权利金、收益不对称'。"""
    S = np.linspace(8, 16, 200); K, prem_c, prem_p = 12.0, 0.6, 0.5
    call = np.maximum(S - K, 0) - prem_c
    put = np.maximum(K - S, 0) - prem_p
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 3.8), sharey=True)
    for ax, y, prem, title, color in [
        (ax1, call, prem_c, "买入看涨 call：上不封顶、下有底", "#d62728"),
        (ax2, put, prem_p, "买入看跌 put：跌时获利、最多亏权利金", "#2ca02c")]:
        ax.plot(S, y, color=color, lw=2)
        ax.axhline(0, color="#999", lw=.8); ax.axvline(K, color="#999", ls=":")
        ax.axhline(-prem, color="#1f77b4", ls="--", label=f"最大损失 = 权利金 {prem}")
        ax.text(K, ax.get_ylim()[1] * .9, f" 行权价 K={K:.0f}", fontsize=8, color="#666")
        ax.set_title(title, fontsize=10); ax.set_xlabel("到期标的价"); ax.legend(fontsize=8); ax.grid(alpha=.3)
    ax1.set_ylabel("每股损益")
    fig.tight_layout(); fig.savefig(IMG_DIR / "ch0F_option_payoff.png", dpi=130); plt.close(fig)
    print(f"  [图] {IMG_DIR / 'ch0F_option_payoff.png'}")


def main() -> None:
    print("ch0F 金融市场与工具基础 · 配套演示")
    print(f"numpy {np.__version__} | pandas {pd.__version__} | 随机种子 20260622")
    demo_adjustment()
    rets = demo_returns()
    demo_risk(rets["daily_simple"], rets["nav"])
    demo_valuation()
    section("6) 概念示意图：集合竞价 / 订单生命周期 / 成本拆解 / 期权损益")
    fig_call_auction()
    fig_order_lifecycle()
    fig_cost_breakdown()
    fig_option_payoff()
    demo_real_data_optional()
    print("\n完成。教学图已输出到", IMG_DIR)


if __name__ == "__main__":
    main()
