=================================================================
Pacman: Clean implementations of Distributed Constraint Optimization Algorithms
=================================================================

``pacman`` is available on GitHub at http://github.com/chufansuki/pacman


Main Features
~~~~~~~~~~~~~

- pyDCOP provides implementations of many classic DCOP algorithms(DSA, MGM, MaxSum, DPOP, etc.).
- pyDCOP allows you to implement our own DCOP algorithm easily, by providing all the required infrastructure: agents, messaging system, metrics collection, etc.
- Agents can run on the same computer or on different machines, making real distributed experiments easy.
- Multi-platform : pyDCOP can run on windows, Mac and Linux.
- pyDCOP is especially suited for IoT use-case and can run agents on single-board computers like the Raspberry Pi.
- In addition to classical DCOP algorithm, pyDCOP also provide novel approaches
  for using DCOP in IoT systems: several strategies are available to distribute
  DCOP computations on agents and achieve resiliency.


.. toctree::
   :maxdepth: 2
   :caption: User Guide
   :hidden:

   guide/install


.. toctree::
   :maxdepth: 3
   :caption: API
   :hidden:

   modules/pacman



Index
==================

* :ref:`genindex`
* :ref:`modindex`