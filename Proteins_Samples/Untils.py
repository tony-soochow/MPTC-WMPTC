# 对Intra以及Intar分别采样生成训练集以及测试集
# Intra：Po：727，Ne：4005 阈值分数为0.5
# Inter：Po：3549，Ne：18247 阈值分数为0.5
# 根据每个蛋白质以及位点信息取得OhmNet编码后得到得特征
#
import random

import numpy as np
import xlrd

Dataset_file_path = '../Dataset.xlsx'
Intra_Po_file_path = './Intra/Intra_positive_sel.xlsx'
Intra_Ne_file_path = './Intra/Intra_negative_sel.xlsx'
Inter_Po_file_path = './Inter/Inter_positive_sel.xlsx'
Inter_Ne_file_path = './Inter/Inter_negative_sel.xlsx'
Embedding_features_file = '../OhmNet/tmp.emb'

# Cross_talk_wb = xlrd.open_workbook(Dataset_file_path)

# Intra_Cross_talk_sheet = Cross_talk_wb.sheet_by_name('Intra_Combine_All')
# Inter_Cross_talk_sheet = Cross_talk_wb.sheet_by_name('Inter_Combine_All')

Embedding_features = dict()

with open(Embedding_features_file, 'r') as f:
    lines = f.readlines()[1:]
    for line in lines:
        name = line.strip('\n').split(' ')[0]
        features = line.strip('\n').split(' ')[1:]
        Embedding_features[name] = features


def encode_intra_sites_feature(protein, site, Embedding_features):
    protein_nums_dict = {'O': '1', 'P': '2', 'Q': '3'}
    new_name = 'Cross-talk_edgelists1_' + protein + '.edgelist__' + protein_nums_dict[protein[0]] + protein[1:] + str(
        site[1:])
    return Embedding_features[new_name]


# inter和Intra不一样encode


def encode_inter_sites_feature(protein1, protein2, site, Embedding_features):
    protein_nums_dict = {'O': '1', 'P': '2', 'Q': '3'}
    new_name = 'Cross-talk_edgelists1_' + protein1 + '.edgelist__' + protein_nums_dict[protein2[0]] + protein2[
                                                                                                      1:] + str(
        site[1:])
    return Embedding_features[new_name]


# features = encode_sites_feature('P04637', 'K101', Embedding_features)
# print(features)


def generate_intra_samples(Embedding_features, Cross_talk_features_path, Negative_features_path, Train_Sample_nums,
                           Test_Sample_nums,
                           Train_path, Test_path, flag_feature):  # 对数据集进行采样
    Cross_talk_features_workbook = xlrd.open_workbook(Cross_talk_features_path)
    Negative_features_workbook = xlrd.open_workbook(Negative_features_path)
    # prediction_nums = []
    Cross_talk_features_sheet = Cross_talk_features_workbook.sheet_by_name('Sheet1')
    Negative_features_sheet = Negative_features_workbook.sheet_by_name('Sheet1')
    Po_nums = Cross_talk_features_sheet.nrows
    Ne_nums = Negative_features_sheet.nrows
    Po_nums = [i for i in range(1, Po_nums)]
    Ne_nums = [i for i in range(1, Ne_nums)]
    random.shuffle(Ne_nums)
    random.shuffle(Po_nums)
    print(Po_nums)
    print(len(Ne_nums))

    def merge_features(Sample_nums, Nums, flag):  # po:50, 100, True; Ne:10, 100, False
        for Sample_num in range(Sample_nums):
            Samples = []
            if flag:  # 提前将训练集测试集对半分，然后再从中采样
                Po_samples_numbers = random.sample(Po_nums[:int((len(Po_nums) * 0.8))], Nums)
                Ne_samples_numbers = random.sample(Ne_nums[:int((len(Ne_nums) * 0.8))], Nums)
            else:
                Po_samples_numbers = random.sample(Po_nums[int((len(Po_nums) * 0.8)):], Nums)
                Ne_samples_numbers = random.sample(Ne_nums[int((len(Ne_nums) * 0.8)):], Nums)

            print(Ne_samples_numbers)
            print(Po_samples_numbers)
            for Po_num in Po_samples_numbers:
                Protein = Cross_talk_features_sheet.row_values(Po_num)[1]
                Site1 = Cross_talk_features_sheet.row_values(Po_num)[2]
                Site2 = Cross_talk_features_sheet.row_values(Po_num)[4]
                ProteinSite1_features = encode_intra_sites_feature(Protein, Site1, Embedding_features)
                ProteinSite2_features = encode_intra_sites_feature(Protein, Site2, Embedding_features)
                Po_W_features = Cross_talk_features_sheet.row_values(Po_num)[6:]
                if flag_feature == 1:  # 单使用分层网络特征
                    Po_Features = ProteinSite1_features + ProteinSite2_features
                    Po_Features = [float(item) for item in Po_Features]
                else:  # 使用生物特征加上分层网络特征
                    Po_W_features = np.array(Po_W_features, dtype='float32').reshape(-1, 1)
                    Po_ML_Features = np.array(ProteinSite1_features + ProteinSite2_features, dtype='float32').reshape(1, -1)
                    Po_Features = Po_W_features.dot(Po_ML_Features).reshape(-1)
                    Po_Features = Po_Features.tolist()
                Samples.append([1] + Po_Features)
            for Ne_num in Ne_samples_numbers:
                Protein = Negative_features_sheet.row_values(Ne_num)[1]
                Site1 = Negative_features_sheet.row_values(Ne_num)[2]
                Site2 = Negative_features_sheet.row_values(Ne_num)[4]
                ProteinSite1_features = encode_intra_sites_feature(Protein, Site1, Embedding_features)
                ProteinSite2_features = encode_intra_sites_feature(Protein, Site2, Embedding_features)
                Ne_W_features = Negative_features_sheet.row_values(Ne_num)[6:]
                if flag_feature == 1:  # 单使用分层网络特征
                    Ne_Features = ProteinSite1_features + ProteinSite2_features
                    Ne_Features = [float(item) for item in Ne_Features]
                else:  # 使用生物特征加上分层网络特征
                    Ne_W_features = np.array(Ne_W_features, dtype='float32').reshape(-1, 1)
                    Ne_ML_Features = np.array(ProteinSite1_features + ProteinSite2_features, dtype='float32').reshape(1, -1)
                    Ne_Features = Ne_W_features.dot(Ne_ML_Features).reshape(-1)
                    Ne_Features = Ne_Features.tolist()
                Samples.append([0] + Ne_Features)
            Samples_np = np.array(Samples)
            if flag:
                np.save(Train_path + '/sample' + str(Sample_num) + '.npy',
                        Samples_np)
            else:
                np.save(Test_path + '/sample' + str(Sample_num) + '.npy',
                        Samples_np)

    merge_features(Train_Sample_nums, 300, True)
    merge_features(Test_Sample_nums, 80, False)


# generate_intra_samples(Embedding_features, Intra_Po_file_path, Intra_Ne_file_path, 5, 1, 'Intra/ML_727/Train',
#                        'Intra/ML_727/Test', 1)
# generate_intra_samples(Embedding_features, Intra_Po_file_path, Intra_Ne_file_path, 5, 1, 'Intra/WML/Train',
#                        'Intra/WML/Test', 2)


def generate_inter_samples(Embedding_features, Cross_talk_features_path, Negative_features_path, Train_Sample_nums,
                           Test_Sample_nums,
                           Train_path, Test_path, flag_feature):  # 对数据集进行采样
    Cross_talk_features_workbook = xlrd.open_workbook(Cross_talk_features_path)
    Negative_features_workbook = xlrd.open_workbook(Negative_features_path)
    # prediction_nums = []
    Cross_talk_features_sheet = Cross_talk_features_workbook.sheet_by_name('Sheet1')
    Negative_features_sheet = Negative_features_workbook.sheet_by_name('Sheet1')
    Po_nums = Cross_talk_features_sheet.nrows
    Ne_nums = Negative_features_sheet.nrows
    Po_nums = [i for i in range(1, Po_nums)]
    Ne_nums = [i for i in range(1, Ne_nums)]
    random.shuffle(Ne_nums)
    random.shuffle(Po_nums)
    print(Po_nums)
    print(len(Ne_nums))

    def merge_features(Sample_nums, Nums, flag):  # po:50, 100, True; Ne:10, 100, False
        for Sample_num in range(Sample_nums):
            Samples = []
            if flag:  # 提前将训练集测试集对半分，然后再从中采样
                Po_samples_numbers = random.sample(Po_nums[:int((len(Po_nums) * 0.8))], Nums)
                Ne_samples_numbers = random.sample(Ne_nums[:int((len(Ne_nums) * 0.8))], Nums)
            else:
                Po_samples_numbers = random.sample(Po_nums[int((len(Po_nums) * 0.8)):], Nums)
                Ne_samples_numbers = random.sample(Ne_nums[int((len(Ne_nums) * 0.8)):], Nums)

            print(Ne_samples_numbers)
            print(Po_samples_numbers)
            for Po_num in Po_samples_numbers:
                Protein1 = Cross_talk_features_sheet.row_values(Po_num)[1]
                Protein2 = Cross_talk_features_sheet.row_values(Po_num)[5]
                Site1 = Cross_talk_features_sheet.row_values(Po_num)[2]
                Site2 = Cross_talk_features_sheet.row_values(Po_num)[6]
                ProteinSite1_features = encode_inter_sites_feature(Protein1, Protein1, Site1, Embedding_features)
                ProteinSite2_features = encode_inter_sites_feature(Protein1, Protein2, Site2, Embedding_features)
                Po_W_features = Cross_talk_features_sheet.row_values(Po_num)[8:]
                if flag_feature == 1:  # 单使用分层网络特征
                    Po_Features = ProteinSite1_features + ProteinSite2_features
                    Po_Features = [float(item) for item in Po_Features]
                else:  # 使用生物特征加上分层网络特征
                    Po_W_features = np.array(Po_W_features, dtype='float32').reshape(-1, 1)
                    Po_ML_Features = np.array(ProteinSite1_features + ProteinSite2_features, dtype='float32').reshape(1,-1)
                    Po_Features = Po_W_features.dot(Po_ML_Features).reshape(-1)
                    Po_Features = Po_Features.tolist()
                Samples.append([1] + Po_Features)
            for Ne_num in Ne_samples_numbers:
                Protein1 = Negative_features_sheet.row_values(Ne_num)[1]
                Protein2 = Negative_features_sheet.row_values(Ne_num)[5]
                Site1 = Negative_features_sheet.row_values(Ne_num)[2]
                Site2 = Negative_features_sheet.row_values(Ne_num)[6]
                ProteinSite1_features = encode_inter_sites_feature(Protein1, Protein1, Site1, Embedding_features)
                ProteinSite2_features = encode_inter_sites_feature(Protein1, Protein2, Site2, Embedding_features)
                Ne_W_features = Negative_features_sheet.row_values(Ne_num)[8:]
                if flag_feature == 1:  # 单使用分层网络特征
                    Ne_Features = ProteinSite1_features + ProteinSite2_features
                    Ne_Features = [float(item) for item in Ne_Features]
                else:  # 使用生物特征加上分层网络特征
                    Ne_W_features = np.array(Ne_W_features, dtype='float32').reshape(-1, 1)
                    Ne_ML_Features = np.array(ProteinSite1_features + ProteinSite2_features, dtype='float32').reshape(1,-1)
                    Ne_Features = Ne_W_features.dot(Ne_ML_Features).reshape(-1)
                    Ne_Features = Ne_Features.tolist()
                Samples.append([0] + Ne_Features)
            Samples_np = np.array(Samples)
            if flag:
                np.save(Train_path + '/sample' + str(Sample_num) + '.npy',
                        Samples_np)
            else:
                np.save(Test_path + '/sample' + str(Sample_num) + '.npy',
                        Samples_np)

    merge_features(Train_Sample_nums, 70, True)
    merge_features(Test_Sample_nums, 18, False)


# generate_inter_samples(Embedding_features, Inter_Po_file_path, Inter_Ne_file_path, 5, 1, './Inter/ML_1000/Train',
#                        './Inter/ML_1000/Test', 1)
generate_inter_samples(Embedding_features, Inter_Po_file_path, Inter_Ne_file_path, 5, 1, './Inter/WML/Train',
                       './Inter/WML/Test', 2)
