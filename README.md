# MPTC/WMPTC

## Introduction
The MPTC/WMPTC model is a model based on a Multilayer Network structure, which is capable of predicting both Intra PTM cross-talk within proteins and Inter PTM cross-talk between proteins.

## Requirements
We recommend using the following command to install the necessary environment. 
```
conda env create -f Inter-Intra-Cross-talk.yml
```

## Usage
* To train the model to predict PTM cross-talk, use the following command: 
```
python main_rf.py
```
* To process the results, use the following command: 
```
python get_result.py
```
## Reference
- Zhu F, Deng L, Dai Y, et al. PPICT: an integrated deep neural network for predicting inter-protein PTM cross-talk[J]. Briefings in Bioinformatics, 2023, 24(2): bbad052.
- Deng L, Zhu F, He Y, et al. Prediction of post-translational modification cross-talk and mutation within proteins via imbalanced learning[J]. Expert Systems with Applications, 2023, 211: 118593.
- Huang R, Huang Y, Guo Y, et al. Systematic characterization and prediction of post-translational modification cross-talk between proteins[J]. Bioinformatics, 2019, 35(15): 2626-2633.
- Li Y, Huang Y, Li T. Ptm-x: Prediction of post-translational modification crosstalk within and across proteins[J]. Computational Methods for Predicting Post-Translational Modification Sites, 2022: 275-283.
- Huang Y, Xu B, Zhou X, et al. Systematic characterization and prediction of post-translational modification cross-talk[J]. Molecular & Cellular Proteomics, 2015, 14(3): 761-770.
- Liu H F, Liu R. Structure-based prediction of post-translational modification cross-talk within proteins using complementary residue-and residue pair-based features[J]. Briefings in Bioinformatics, 2020, 21(2): 609-620.
- Zitnik M, Leskovec J. Predicting multicellular function through multi-layer tissue networks[J]. Bioinformatics, 2017, 33(14): i190-i198.
- Zhang S, Krieger J M, Zhang Y, et al. ProDy 2.0: increased scale and scope after 10 years of protein dynamics modelling with Python[J]. Bioinformatics, 2021, 37(20): 3657-3659.

