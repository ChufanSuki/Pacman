Usage
=====

.. _installation:

Installation
------------

To use Pacman, first install it using pip:

.. code-block:: console

   (.venv) $ pip install pacman

Creating recipes
----------------

To retrieve a list of random ingredients,
you can use the ``pacman.get_random_ingredients()`` function:

.. autofunction:: pacman.get_random_ingredients

The ``kind`` parameter should be either ``"meat"``, ``"fish"``,
or ``"veggies"``. Otherwise, :py:func:`pacman.get_random_ingredients`
will raise an exception.

.. autoexception:: pacman.InvalidKindError

For example:

>>> import pacman
>>> pacman.get_random_ingredients()
['shells', 'gorgonzola', 'parsley']
