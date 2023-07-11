Command Line Arguments
======================
Command line arguments to be used with the files in the ``test/`` directory.

.. autoclass:: src.args.CustomParser

General Arguments
-----------------
Arguments used during both the generation and analysis of decision regions.

* ``--save_loc/--save-loc``: directory in which to save program outputs.
* ``--save_name/--save-name``: name to use for the created decision region hdf5 file.
* ``--classes``: model output classes, in format category:option1,option2 (ex. COVID_positive:Yes,No).
* ``--class_order``: used to designate which class corresponds with a model output of 0 or 1; default: 0,1.
* ``--subgroup_attributes``: attributes to be used in addition to `--classes` to group samples and analysis.
* ``--overwrite``: if passed, previously generated hdf5 or analysis files may be overwritten.

Generation Arguments
--------------------
Arguments used exclusivly during the generation of decision regions.

* ``--model_file/--model-file``: file path to the onnx model file.
* ``--data_csv/--data-csv``: csv file which pairs sample ids with image file paths and class and attribute information.
* ``--batch_size/--batch-size``: batch size to be used with the data loader.
* ``--shape``: the shape of the generated vicinal distributions; default: triangle.
* ``--steps``: the number of steps to take between samples in the triplet when creating the vicinal distribution. With --shape=rectangle, approximately step^2 virtual samples will be generated.
* ``--n_triplets/--n-triplets``: the number of triplets to generate for each group.
* ``--img_rel_path/--img-rel-path``: the common directory for the image file paths, include if the file paths in ``--data_csv`` are relative.

Analysis Arguments
------------------
Arguments used exclusivly during the analysis and plotting of decision regions.

* ``--out_function``: the function to be applied to model output scores; see `utilities <src/utils.py>` for options.
* ``--aggregate/--agg``: how to aggregate composition analysis; options: class, group, all.
	Note: decision region compositions are always calculated by triplet before being aggregating to ensure that each triplet has the same impact on the calculated compositiond despite slight variations in the number of virtual samples between triplets' decision regions.
* ``--threshold``: the treshold applied during composition analysis; does not affect region plots.
* ``--plot_only/--plot-only``: pass to not save composition analysis files.
* ``--plot``: type of plot to generate; options: composition, performance, region; no plots will be generated if argument is not passed.
* ``--show``: pass to show plots.
* ``--display-only``: pass to not save plots.
* ``--hide-percent``: pass to not include percent text on composition/performance plots.
* ``--hide-errorbar``: pass to not include errorbars on composition/performance plots.
* ``--save_dpi/--save-dpi``: dpi used when saving summary plots.
* ``--plot_output_format/--plot-output-format``: Output formats in which the plots should be saved.
* ``--plot_palette/--plot-palette``: color palette to be used during plotting, can be either a matplotlib colorpalette or a custom palette.
* ``--plot_threshold/--plot-threshold``: threshold applied to ouput scores in 'region' plots; if None, no threshold is applied.
* ``--n_per_group/--n-per-group``: number of decision regions to plot per group if plot = 'region'.
*