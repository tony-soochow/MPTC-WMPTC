import numpy as np
import pandas as pd


# 读取样本数据生成一维numpy数组进行训练及测试
def read_samples_1d(filepath):
    features = np.load(filepath, allow_pickle=True)
    features_data = features[:, 1:]
    # print(features_data)
    features_data.astype('float32')
    features_label = np.array([int(item) for item in features[:, 0].tolist()])
    # print(features_data)
    return features_data, features_label



def read_samples_2d(filepath, flag):  # flag: True 仅使用W的特征
    features = np.load(filepath, allow_pickle=True)
    if not flag:
        features_data = features[:, 1:].reshape(-1, 256, 37)
    else:
        features_data = features[:, 1:].reshape(-1, 1, 1000)
    features_label = np.array([int(item) for item in features[:, 0].tolist()])
    return features_data, features_label


# features_data, features_label = read_samples_1d('../Datasets/Samples/W_pre_Train/sample0.npy')
# print(features_data.shape)
# print(features_label)