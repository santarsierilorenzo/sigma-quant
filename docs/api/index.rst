API Reference
=============

Quant-Kit exposes a flat, high-level API that covers the majority of common
quantitative finance use cases. In most scenarios, users do not need to import
functions directly from submodules.

This section provides an overview of the available API domains. Use the
navigation below to access detailed function signatures and documentation.


Returns
~~~~~~~

Functions for computing and aggregating returns, as well as measuring
performance over time.

Examples include cumulative returns, annualized returns, and active returns.


Metrics
~~~~~~~

Risk-adjusted performance metrics commonly used in quantitative finance.

This includes Sharpe, Sortino, Calmar, and other widely adopted ratios.


Risk
~~~~

Functions for measuring downside risk, drawdowns, and volatility-related
statistics.


Rolling
~~~~~~~

Rolling-window versions of selected metrics, useful for time-varying analysis.


.. toctree::
   :maxdepth: 1
   :hidden:

   returns
   risk
   metrics
   rolling


