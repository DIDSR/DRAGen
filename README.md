# Decision Region Analysis for Generalizability (DRAGen) of AI models: Estimating model generalizability in the case of cross-reactivity and population shift
## Regulatory Science Tool
Prediction model deployment of virtual images generated from vicinal distribution provides smooth decision region transitions between various subgroups. This RST is used to analyze the compositions of these decision regions for many subgroups to provide insight into the how well they are represented in the data and the discontinuity of subgroup decision regions leading to incorrect predictions.

### Purpose
Understanding an artificial intelligence (AI) model's ability to generalize to its target population is critical to ensure the safe and effective use of AI in medical devices. Traditional generalizability assessment relies on the availability of large, diverse data sets, which are difficult to obtain for medical imaging. We present an approach for enhanced generalizability assessment by examining the decision space beyond the available test set. 

## Decision Region Analysis
A model's decision space can be analyzed by mapping a change in the input to a change in the output. However, as deep convolutional neural networks (DCNN) are both feature extractors and classifiers, it is challenging to modify inputs in a way that is meaningful to both the model and the user.

In this RST, we present a decision region analysis approach which uses the creation of vicinal distributions of virtual images to better characterize the model's decision space, either overall or for individual subgroups.

> **Virtual Image:** An image that was created by modifying existing image(s), rather than obtained through a typical image acquisition method.

> **Vicinal Distribution:** The collection of virtual images created by linearly interpolating between a 'triplet' of three images.


---


## References
1. <a id="Somepalli"> G. Somepalli, L. Fowl, A. Bansal, et al., “Can neural nets learn the same model twice? investigating reproducibility and double descent from the decision boundary perspective,” Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 13699–13708 (2022). </a>

2. <a id = "SPIE"> A. Burgon, N. Petrick, G. Berkman Sahiner, et al., “Decision region analysis to deconstruct the subgroup influence on ai/ml predictions,” in Proc. of SPIE Vol, 12465, 124651H–1 (2023). </a>
