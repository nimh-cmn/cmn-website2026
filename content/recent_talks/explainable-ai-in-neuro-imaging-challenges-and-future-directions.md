Title: Explainable AI in Neuro-Imaging: Challenges and Future Directions
Date: 2024-10-19 14:08
Talk_month: March 2020
Slug: explainable-ai-in-neuro-imaging-challenges-and-future-directions
Speaker_Slug: 69
Part_of:[The Machine Learning in Brain Imaging Series](/talks/machine-learning-in-brain-imaging/)
Links: [View Talk](https://www.youtube.com/watch?v=_enZG0ly5aE&ab_channel=NIMHCenterforMultimodalNeuroimaging)
Template: talk_detail

Decoding and encoding models are widely applied in cognitive neuroscience to find statistical associations between experimental context and brain response patterns. Depending on the nature of their application, these models can be used to read out representational content from functional activity data, determine if a brain region contains specific information, predict diagnoses, and test theories about brain information processing. These multivariate models typically contain fitted linear components. However, even with linear models - the limit of simplicity - interpretation is complex. Voxels that carry little predictive information alone may be assigned a strong weight if used for noise cancelation purposes, and informative voxels may be assigned a small weight when predictor variables carry overlapping information. In the deep learning setting, determining which inputs contribute to model predictions is even more complex. A variety of recent techniques are now available to map relevance weights through the layers of a deep learning network onto input brain images. However, small noise perturbations, common in the MRI scanning environment, can produce large alterations in the relevance maps without altering the model prediction. In certain settings, explanations can be highly divergent without even altering the model weights. In clinical applications, both false positives and omissions can have severe consequences. Explanatory methods should be reliable and complete before interpretation can appropriately reflect the level of generalization that the model provides.

