"""地基库联调冒烟测试 —— 验证回测/因子/Qlib/绩效/数据 库能否在当前 numpy/pandas 主栈共存。

运行（隔离环境，不污染主 venv；NUMBA_DISABLE_JIT=1 让 vectorbt 跳过首次 JIT 编译，秒级出结果）：

    NUMBA_DISABLE_JIT=1 uv run --isolated \
        --with "numpy>=2.4" --with "pandas>=3.0" \
        --with vectorbt --with pyqlib --with quantstats --with polars --with pyarrow \
        --with alphalens-reloaded --with empyrical-reloaded --with pyfolio-reloaded \
        python guide/code/smoke_baseline_libs.py

2026-06-22 实测结论（Python 3.11.11 / numpy 2.4.6 / pandas 3.0.3）：
    [OK]   vectorbt 0.28.2     import + from_holding 回测 + stats()(24 指标)
    [OK]   pyqlib   0.9.7      import；qlib.contrib.eva.alpha.calc_ic / calc_long_short_return 可用
    [OK]   quantstats 0.0.81   组合绩效（夏普/回撤/月度）
    [OK]   polars   1.41.2     数据处理；与 pandas 双向互转 OK（可作特征工程加速层）
    [FAIL] alphalens-reloaded  empyrical -> pandas_datareader 撞 pandas3 deprecate_kwarg
    [FAIL] empyrical-reloaded  同上根因
    [FAIL] pyfolio-reloaded    同上根因
    （升级最新 pandas-datareader 0.10 无效；该库 2021 停更、未适配 pandas3。
     社区共识见 pandas-datareader#1005「Breakage coming in pandas 3.0」。）

决策：主栈（numpy2/pandas3）用 vectorbt + pyqlib + quantstats（+ polars 选配数据加速）；
      因子 IC/分层/多空用 qlib.contrib.eva.alpha 或从零实现，放弃 alphalens 系（绑定 pandas1.x）。
      polars 不能"修复"alphalens（其内部硬依赖 pandas）；pandas 仍是生态对接通用格式。
"""
import os
os.environ.setdefault("NUMBA_DISABLE_JIT", "1")  # 冒烟只验证逻辑，跳过 numba 首次编译

import numpy as np
import pandas as pd

print(f"base stack:  numpy {np.__version__}  pandas {pd.__version__}\n")


def probe(name, fn):
    try:
        print(f"[OK]   {name}: {fn()}")
    except Exception as e:
        print(f"[FAIL] {name}: {type(e).__name__}: {str(e)[:140]}")


def _vectorbt():
    import vectorbt as vbt
    price = pd.Series([1.0, 2.0, 3.0, 2.0, 4.0, 5.0])
    pf = vbt.Portfolio.from_holding(price, init_cash=100)
    return f"{vbt.__version__}  total_return={float(pf.total_return()):.2f}  stats={len(pf.stats())}项"


def _pyqlib():
    import qlib
    from qlib.contrib.eva.alpha import calc_ic, calc_long_short_return  # noqa: F401
    return f"{qlib.__version__}  calc_ic/calc_long_short_return 可用"


def _quantstats():
    import quantstats as qs
    return qs.__version__


def _polars():
    import polars as pl
    df = pl.DataFrame({"sym": ["a", "a", "b"], "ret": [0.1, -0.2, 0.3]})
    pl.from_pandas(df.to_pandas())  # 与 pandas 往返
    return f"{pl.__version__}  to_pandas/from_pandas 往返 OK"


def _alphalens():
    import alphalens
    return alphalens.__version__


def _empyrical():
    import empyrical
    return empyrical.__version__


def _pyfolio():
    import pyfolio
    return pyfolio.__version__


print("— 主栈可用主力 —")
probe("vectorbt", _vectorbt)
probe("pyqlib", _pyqlib)
probe("quantstats", _quantstats)
probe("polars", _polars)
print("\n— Quantopian 系（预期失败：绑定 pandas1.x）—")
probe("alphalens-reloaded", _alphalens)
probe("empyrical-reloaded", _empyrical)
probe("pyfolio-reloaded", _pyfolio)
