Returns
=======

Functions for computing and aggregating returns, as well as measuring
performance over time.


cum_returns
-----------

Compute cumulative performance over time from a sequence of returns or
PnL values.

.. autofunction:: quant_kit.returns.cum_returns


Examples
~~~~~~~~

Simple returns:

.. code-block:: python

   import numpy as np
   import quant_kit as qt

   returns = np.array([0.01, 0.02, -0.01, 0.03])
   qt.cum_returns(returns)


Log-returns:

.. code-block:: python

   qt.cum_returns(returns, kind="log")


PnL series:

.. code-block:: python

   qt.cum_returns(returns, kind="pnl", starting_value=100.0)
