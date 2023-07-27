# DRAGen: Decision Region Analysis for Generalizability 

**DRAGen is an AI/ML model agnostic approach to assess generalizability.**

```mermaid
graph LR;
  A -----> E --> F
  B --> D --> E
  C ----> F --> G

  style A fill:#913826,stroke:#1f1f1f,stroke-width:4px
  style B fill:#913826,stroke:#1f1f1f,stroke-width:4px
  style C fill:#913826,stroke:#1f1f1f,stroke-width:4px
  subgraph 1 [Input]
    direction LR
    A(["Image data"])
    B{{"Attributes and\nclass labels"}}
    C>"Binary classification model\n(onnx format)"]
  end

  style D fill:#2e426e,stroke:#1f1f1f,stroke-width:4px
  style E fill:#2e426e,stroke:#1f1f1f,stroke-width:4px
  subgraph 2 [Generation]
    direction LR

    D["Triplet\nselection"]
    E["Virtual sample\ngeneration"]
    
  end
  style F fill:#520d3d,stroke:#1f1f1f,stroke-width:4px
  F{"Model\ninference"}

  style G fill:#104a27,stroke:#1f1f1f,stroke-width:4px
  subgraph 3 [Analysis]
    G["Decision regions plots\nand composition"]
  end
```

<p style="text-align: center;"> Overview of the decision region generation and analysis process  </p>

---

This repository contains the implementation for the methodology in the paper "Decision region analysis to deconstruct the subgroup influence on ai/ml predictions". The paper is available at this [link](https://www.spiedigitallibrary.org/conference-proceedings-of-spie/12465/124651H/Decision-region-analysis-to-deconstruct-the-subgroup-influence-on-AI/10.1117/12.2653963.short).

## Additional References
- A. Burgon, N. Petrick, B. Sahiner, G. Pennello, R. K. Samala*, "Predicting AI model behavior on unrepresented subgroups: A test-time approach to increase variability in a finite test set", 2023 FDA Science Forum. ([link](https://www.fda.gov/science-research/fda-science-forum/predicting-ai-model-behavior-unrepresented-subgroups-test-time-approach-increase-variability-finite))
- Alexis Burgon, Nicholas Petrick, Berkman Sahiner, Gene Pennello, and Ravi K. Samala "Decision region analysis to deconstruct the subgroup influence on AI/ML predictions", Proc. SPIE 12465, Medical Imaging 2023: Computer-Aided Diagnosis, 124651H (7 April 2023); https://doi.org/10.1117/12.2653963

<!---
# Citation
To cite our work:

    A. Burgon, N. Petrick, B. Sahiner, G. Pennello, R. K. Samala, “Decision region analysis to deconstruct the subgroup influence on AI/ML predictions”, Proc. of SPIE, 12465, 124651H (2023). doi.org/10.1117/12.2653963

## Bibtex citation
```
    @inproceedings{burgon2023decision,
  title={Decision region analysis to deconstruct the subgroup influence on AI/ML predictions},
  author={Burgon, Alexis and Petrick, Nicholas and Sahiner, Berkman and Pennello, Gene and Samala, Ravi K},
  booktitle={Society of Photo-Optical Instrumentation Engineers (SPIE) Conference Series},
  volume={12465},
  pages={124651H},
  year={2023}
}
```
-->
# Introduction
Understanding an artificial intelligence (AI) model's ability to generalize to its target population is critical to ensure the safe and effective use of AI in medical devices. Traditional generalizability assessment relies on the availability of large, diverse data sets, which are difficult to obtain for medical imaging. We present an approach for enhanced generalizability assessment by examining the decision space beyond the available test set.

A vicinal distribution of virtual images is created by linearly interpolating between a sample "triplet" of three images. The composition of the region of the decision space is then approximated from the model inference on the virtual images. Aggregating the decision region compositions from many triplets provides insight into the overall decision region composition. 

# Getting Started
The documentation for this project is included in the [docs/build/html](https://github.com/DIDSR/RST_Decision_Region_Analysis/tree/main/docs/build/html) folder. To view the documentation, download a copy of this folder and open the file ``index.html``. 

An interactive example of how to use this repository can be found in the [example notebook](https://github.com/DIDSR/RST_Decision_Region_Analysis/blob/main/examples/example_implementation.ipynb)

## Example Output
![Example Output](examples/example_composition_plot.png)

<p style="text-align: center;">  Example decision region composition plot. The decision region compositions are aggregated based on the class of the sample triplet. </p>

---

## System Requirements
```
python 3.10.6
Ubuntu 22.04.2 LTS
```
Python package requirements can be found in [requirements.txt](requirements.txt).
