=================================================================
Pacman: Clean implementations of Distributed Constraint Optimization Algorithms
=================================================================

``pacman`` is available on GitHub at http://github.com/chufansuki/pacman


Main Features
~~~~~~~~~~~~~

- Generation of standard DCOP test problems: weighted graph coloring problems, scale-free problems and related parameter settings to generate the corresponding XML files/YAML files for the problems.
- Test file parsing: parse the XML file/YAML file to map the information in the DCOP problem to the underlying structure.
- Inter-process communication mechanism: implementation of process communication to simulate multi-intelligent body parallel interaction, and implementation of asynchronous and synchronous control methods.
- Multi-platform : Pacman can run on windows, Mac and Linux.
- Reproduce several classical DCOP algorithms methods, including MGM, DPOP, etc.
- Define algorithm performance metrics and implement each performance metric for Visualization interface for statistical testing of algorithm performance and display of algorithm parameters and performance.



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