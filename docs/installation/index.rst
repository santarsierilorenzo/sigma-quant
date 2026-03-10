Installation
=============
Quant-Kit can be installed using ``pip``:

.. code-block:: bash

   pip install quant-kit

Import
~~~~~~~~~~~~~~~~~~~~
The recommended import pattern is the following:

.. code-block:: python

   import quant_kit as qt

For subpackage-oriented imports:

.. code-block:: python

   from quant_kit.performance import sharpe_ratio, drawdown
   from quant_kit.research.autocorr import ljung_box

Example
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import numpy as np
   import quant_kit as qt

   returns = np.array([0.2, 0.3, -0.5, 0.7, 0.2, 0.1, -0.7])

   qt.sharpe_ratio(
       returns,
       frequency="D",
   )

.. toctree::
   :maxdepth: 1
