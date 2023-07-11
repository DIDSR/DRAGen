Getting Started
===============
Three inputs are required for this RST:

1. **Trained Model:** the model must be saved in onnx format. Information on how to convert your model to onnx format can be found at the `onnx GitHub page`_.
2. **Images:** Images can be saved in any format supported by PIL.
3. **Input csv:** A csv file which can be used to map the image paths to subgroup attributes.

Examples implementation can be found in the `examples folder`_.

Scripts to generate and analyze decision regions can be found in the ``test`` folder, 
all arguments used to run these scripts are located in ``src/args.py``.
Example inputs are included in the ``examples`` folder.

.. _onnx GitHub page: https://github.com/onnx/tutorials#converting-to-onnx-format
.. _examples folder: https://github.com/DIDSR/RST_Decision_Region_Analysis/tree/main/examples

Terminology
===========
* ``class``: An attribute by which the model classifies images. Only binary classification models are currently supported.
* ``subgroup attribute``: An attribute by which the model *does not* classify images, but can be used to group samples into subgroups. 
* ``decision region``: A portion of the decision space. The decision regions generated in this RST are the regions of the decision space near to a 'triplet' of sample images.
* ``virtual image``: An image that was created by modifying existing image(s), rather than obtained through a typical image acquisition method.
* ``vicinal distribution``: The collection of virtual images created by linearly interpolating between a 'triplet' of three images.