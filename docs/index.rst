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
           The API is high-level, composable, and easy to integrate into existing
           codebases.
         </p>

         <p>
           In addition to individual metrics, Quant-Kit emphasizes
           <em>clarity</em> and <em>correctness</em>, offering documentation that
           explains not only how each metric is computed, but also why specific
           design choices were made.
         </p>

         <div class="cta-row">
           <a class="cta-pill cta-primary" href="getting_started.html">
             <span class="cta-icon">🚀</span>
             <span class="cta-text">Get Started</span>
           </a>

           <a class="cta-pill cta-secondary"
              href="https://github.com/your-org/quant-kit">
             <span class="cta-icon">
               <svg xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    width="18"
                    height="18"
                    fill="currentColor"
                    aria-hidden="true">
                 <path d="M12 0.296c-6.63 0-12 5.373-12 12
                          0 5.303 3.438 9.8 8.205 11.387
                          .6.113.82-.258.82-.577
                          0-.285-.01-1.04-.015-2.04
                          -3.338.724-4.042-1.61-4.042-1.61
                          -.546-1.387-1.333-1.756-1.333-1.756
                          -1.089-.745.084-.729.084-.729
                          1.205.084 1.838 1.236 1.838 1.236
                          1.07 1.835 2.809 1.305 3.495.998
                          .108-.776.418-1.305.762-1.605
                          -2.665-.3-5.466-1.332-5.466-5.93
                          0-1.31.469-2.381 1.236-3.221
                          -.123-.303-.536-1.523.117-3.176
                          0 0 1.008-.322 3.301 1.23
                          .957-.266 1.983-.399 3.003-.404
                          1.02.005 2.047.138 3.006.404
                          2.291-1.552 3.297-1.23 3.297-1.23
                          .655 1.653.242 2.873.119 3.176
                          .77.84 1.235 1.911 1.235 3.221
                          0 4.61-2.807 5.625-5.479 5.921
                          .43.372.823 1.102.823 2.222
                          0 1.606-.015 2.898-.015 3.293
                          0 .319.216.694.825.576
                          C20.565 22.092 24 17.592 24 12.296
                          c0-6.627-5.373-12-12-12z"/>
               </svg>
             </span>
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