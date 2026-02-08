.. image:: _static/logo.svg
   :align: right
   :height: 8.5rem


Quant-Kit
=========

A clean, modern Python library for quantitative finance metrics.

Quant-Kit provides a collection of widely used performance and risk metrics
designed for research, backtesting, and portfolio analysis. The API is
high-level, composable, and easy to integrate into existing codebases.

In addition to individual metrics, Quant-Kit emphasizes *clarity* and
*correctness*, offering documentation that explains not only how each metric
is computed, but also why specific design choices were made.


.. raw:: html

   <div class="sd-container-fluid sd-mb-4">
     <div class="sd-row sd-g-3">
       <div class="sd-col sd-col-auto">
         <a class="sd-btn sd-btn-primary sd-rounded-pill"
            href="installation/index.html">
           <span class="bz-emoji">🚀</span> Get Started
         </a>
       </div>

       <div class="sd-col sd-col-auto">
         <a class="sd-btn sd-btn-outline-secondary sd-rounded-pill"
            href="https://github.com/your-org/quant-kit">
           <svg xmlns="http://www.w3.org/2000/svg"
                width="1em" height="1em"
                viewBox="0 0 16 16"
                aria-hidden="true"
                style="vertical-align: -0.125em;">
             <path fill="currentColor"
               d="M8 0C3.58 0 0 3.58 0 8a8 8 0 0 0
               5.47 7.59c.4.07.55-.17.55-.38
               0-.19-.01-.82-.01-1.49
               -2.01.37-2.53-.49-2.69-.94
               -.09-.23-.48-.94-.82-1.13
               -.28-.15-.68-.52-.01-.53
               .63-.01 1.08.58 1.23.82
               .72 1.21 1.87.87 2.33.66
               .07-.52.28-.87.51-1.07
               -1.78-.2-3.64-.89-3.64-3.95
               0-.87.31-1.59.82-2.15
               -.08-.2-.36-1.02.08-2.12
               0 0 .67-.21 2.2.82
               .64-.18 1.32-.27 2-.27
               .68 0 1.36.09 2 .27
               1.53-1.04 2.2-.82 2.2-.82
               .44 1.1.16 1.92.08 2.12
               .51.56.82 1.27.82 2.15
               0 3.07-1.87 3.75-3.65 3.95
               .29.25.54.73.54 1.48
               0 1.07-.01 1.93-.01 2.2
               0 .21.15.46.55.38A8.01
               8.01 0 0 0 16 8
               c0-4.42-3.58-8-8-8Z"/>
           </svg>
           View on GitHub
         </a>
       </div>
     </div>
   </div>


Overview
~~~~~~~~

.. grid:: 3
   :gutter: 2

   .. grid-item-card:: 📊 Performance Metrics
      :link: api/returns.html

      Portfolio and strategy performance metrics such as cumulative returns,
      Sharpe ratio, drawdowns, volatility, and related statistics.

   .. grid-item-card:: ⚠️ Risk Analysis
      :link: api/risk.html

      Downside and tail-risk measures, including value-at-risk,
      expected shortfall, and stress-oriented indicators.

   .. grid-item-card:: 🧪 Research Tools
      :link: api/research.html

      Utilities designed for quantitative research workflows, including
      factor analysis helpers and strategy evaluation tools.


.. toctree::
   :hidden:
   :maxdepth: 2

   inst
