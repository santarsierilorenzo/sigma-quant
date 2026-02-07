Usage
====================================
Quant-Kit can be installed using ``pip``:

.. code-block:: bash

   pip install quant-kit

Import
~~~~~~
The recommended import pattern is the following:

.. code-block:: python

   import quant_kit as qt


Example
~~~~~~
.. code-block:: python
    import quant_kit as qt

    returns = np.array([0.2, 0.3, -0.5, 0.7, 0.2, 0.1, -0.7])

    qt.sharpe_ratio(
        returns,
        frequency="D"
    )

.. toctree::
   :maxdepth: 2

   api/index
