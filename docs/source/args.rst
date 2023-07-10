Command Line Arguments
======================
Command line arguments to be used with test/analysis and test/main

.. autoclass:: src.args.CustomParser

General Arguments
-----------------
Arguments used during both the generation and analysis of decision regions.

* ``--save_loc``: directory in which to save program outputs.
* ``--save_name``: name to use for the created decision region hdf5 file.
* ``--classes``: model output classes, in format category:option1,option2 (ex. COVID_positive:Yes,No).
* ``--class_order``: [TODO]
* ``--subgroup_attributes``: attributes to be used in addition to `--classes` to group samples and analysis

Generation Arguments
--------------------
Arguments used exclusivly during the generation of decision regions.

* ``--model_file``: file path to the onnx model file.
* ``--data_csv``: csv file which pairs sample ids with image file paths and class and attribute information.
* ``--batch_size``: batch size to be used with the data loader
* ``--overwrite``: [TODO]
* ``--steps``: [TODO]
* ``--n_triplets``: [TODO]
* ``--img_rel_path``: the common directory for the image file paths, include if the file paths in ``--data_csv`` are relative.

Analysis Arguments
------------------
Arguments used exclusivly during the analysis of decision regions.

* ``--out_function``: [TODO]
* ``--aggregate/--agg``: [TODO]
* ``--plot``: [TODO]
* ``--show``: [TODO]
* ``--display-only``: [TODO]
* ``--hide-percent``: [TODO]
* ``--hide-errorbar``: [TODO]