RST: Decision Region Analysis
=============================

\*Insert basic description of this RST here\*

Getting Started
===============
Three inputs are required for this RST:

1. **Trained Model:** the model must be saved in onnx format. Information on how to convert your model to onnx format can be found at the `onnx GitHub page`_.
2. **Images:** Images can be saved in any format supported by PIL.
3. **Input csv:** A csv file which can be used to map the image paths to subgroup attributes.

Examples of inputs and implementation can be found in [insert link to example folder].

Scripts to generate and analyze decision regions can be found in the ``test`` folder, 
all arguments used to run these scripts are located in ``src/args.py``.
Example inputs are included in the ``examples`` folder.

.. _onnx GitHub page: https://github.com/onnx/tutorials#converting-to-onnx-format

Contents
========
.. toctree::
   :hidden:

   self

.. toctree::
   
   src
   args

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
