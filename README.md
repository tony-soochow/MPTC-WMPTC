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
- Zheng, S., Tan, Y., Wang, Z., Li, C., Zhang, Z., Sang, X., ... & Yang, Y. (2022). Accelerated rational PROTAC design via deep learning and molecular simulations. Nature Machine Intelligence, 4(9), 739-748.

