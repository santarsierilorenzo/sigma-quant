.. raw:: html

   <div class="hero-wrapper">
     <div class="hero">

       <div class="hero-content">

         <h1 class="hero-title">Quant-Kit</h1>

         <p class="hero-subtitle">
           A clean, modern Python library for quantitative finance metrics.
         </p>

         <p>
           Quant-Kit provides a collection of widely used performance and risk
           metrics designed for research, backtesting, and portfolio analysis.
           The API is high-level, composable, and easy to integrate into
           existing codebases.
         </p>

         <p>
           In addition to individual metrics, Quant-Kit emphasizes
           <em>clarity</em> and <em>correctness</em>, offering documentation
           that explains not only how each metric is computed, but also why
           specific design choices were made.
         </p>

         <div class="cta-row">

           <a class="cta-pill cta-primary" href="installation/">
             <span class="cta-icon">🚀</span>
             <span class="cta-text">Get Started</span>
           </a>

           <a class="cta-pill cta-secondary"
              href="https://github.com/santarsierilorenzo/quant-kit">
             <span class="cta-text">View on GitHub</span>
           </a>

         </div>
       </div>

     </div>
   </div>


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

   installation/index
   api/index
