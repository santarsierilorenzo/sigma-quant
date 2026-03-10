
<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy">
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/Quantitative%20Finance-2E8B57?style=for-the-badge" alt="Quant Finance">
  <img src="https://img.shields.io/badge/Research%20Grade-6A0DAD?style=for-the-badge" alt="Research Grade">
</p>

<p align="center">
  <b>Research-Grade Performance & Risk Metrics</b><br>
  <i>Statistically consistent analytics for quantitative finance</i>
</p>


sigma-quant is a lightweight Python library providing performance,
risk, and distribution metrics for quantitative finance workflows.


### 📦 Installation (PyPI Package)
------------
Install the package from **PyPI**:

```bash
pip install sigma-quant
```

### 📘Documentation
-------------
This README is intentionally high-level.

For the complete API reference, mathematical definitions, statistical
conventions, and usage examples, please refer to the official
documentation:

https://sigma-quant.readthedocs.io/en/latest/index.html


### ASCII Report

Generate a fast portfolio performance report using `ascii_report`.
If the input series represents **PnL**, set `kind="pnl"` and optionally
specify the currency.

```python
import sigmaquant

report = sigmaquant.ascii_report(
    returns=portfolio_returns,
    frequency="D",
    strategy_name="My Portfolio",
    kind="simple",
)

print(report)

# Optional exports
df = report.to_dataframe()
data = report.to_dict()
```

### 🪪 License
------------
MIT © 2025 — Developed with ❤️ by Lorenzo Santarsieri & Tommaso Grandi
