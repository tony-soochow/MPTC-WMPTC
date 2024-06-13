import numpy as np
import random
from keras.utils.np_utils import to_categorical


def get_three_class_data(data, label):
    '''
	从原始全部的训练数据中得到1:1:1的部分数据及其标签
	'''
    # print(data.shape, label.shape)

    class_0_index = np.where(label == 0)[0]  # 找出0类的索引
    class_1_index = np.where(label == 1)[0]
    class_2_index = np.where(label == 2)[0]
    # print(len(class_0_index), len(class_1_index), len(class_2_index))  # 47433 4418 16356

    # print(class_0_index[50])  # 76

    class_0_data = data[class_0_index]  # 类别0的数据
    class_1_data = data[class_1_index]
    class_2_data = data[class_2_index]
    # print(class_0_data.shape, class_1_data.shape, class_2_data.shape)

    min_value = min([len(class_0_index), len(class_1_index), len(class_2_index)])  # 得到最少的数量
    # print(min_value)

    random_class_0 = random.sample(range(0, len(class_0_index)), min_value)  # 生成min_value个0到len中的数
    random_class_1 = random.sample(range(0, len(class_1_index)), min_value)
    random_class_2 = random.sample(range(0, len(class_2_index)), min_value)

    final_data = np.vstack([class_0_data[random_class_0], class_1_data[random_class_1], class_2_data[random_class_2]])
    final_label = np.zeros(min_value * 3)
    final_label[:min_value] = 0
    final_label[min_value: 2 * min_value] = 1
    final_label[2 * min_value:] = 2

    # print(final_data.shape)  # (13254, 11, 56)
    # print(final_label.shape)   # (13254, 11, 56)

    return final_data, to_categorical(final_label)  # 把标签one-hot化


def get_two_class_data(data, label):
    '''
	从原始全部的训练数据中得到1:1的部分数据（数据不重复）及其标签
	'''
    # print(data.shape, label.shape)   # (51851, 11, 56) (51851,)

    ratio = 1
    class_0_index = np.where(label == 0)[0]  # 找出0类的索引
    class_1_index = np.where(label == 1)[0]

    # print(len(class_0_index), len(class_1_index))  # 47433 4418

    # print(class_0_index[50])  # 76

    class_0_data = data[class_0_index]  # 类别0的数据
    class_1_data = data[class_1_index]
    # print(class_0_data.shape, class_1_data.shape)

    min_value = min([len(class_0_index), len(class_1_index)])  # 得到最少的数量
    # print(min_value)

    random_class_0 = random.sample(range(0, len(class_0_index)), int(min_value * ratio))  # 生成min_value个0到len中的数 不重复
    random_class_1 = random.sample(range(0, len(class_1_index)), min_value)
    # print(len(np.unique(random_class_0)))
    # print(np.unique(random_class_0))

    final_data = np.vstack([class_0_data[random_class_0], class_1_data[random_class_1]])
    final_label = np.zeros(final_data.shape[0])
    # print(final_data.shape)
    final_label[:-min_value] = 0
    final_label[-min_value:] = 1

    # print(final_data.shape)  # (8836, 11, 56)
    # print(final_label.shape)   # (8836,)

    return final_data, final_label


def generate_two_data(data, label):
    '''
	选取1：ratio的数据，会遍历完所有的样本数多的数据
	'''
    ratio = 1
    class_0_index = np.where(label == 0)[0]  # 找出0类的索引
    class_1_index = np.where(label == 1)[0]

    # print(len(class_0_index), len(class_1_index))  # 47433 4418

    # print(class_0_index[50])  # 76

    class_0_data = data[class_0_index]  # 类别0的数据
    class_1_data = data[class_1_index]
    # print(class_0_data.shape, class_1_data.shape)

    max_size = class_0_data.shape[0]  # 负样本数
    size = int(class_1_data.shape[0] * ratio)  # 得到正样本数数量的ratio倍
    # print(max_size, size)  # 47433 4418

    i = 0
    while i < max_size:
        final_data, final_label = None, None
        final_data = np.vstack([class_0_data[i:(i + size)], class_1_data])
        final_label = np.zeros(final_data.shape[0])
        final_label[: -class_1_data.shape[0]] = 0
        final_label[-class_1_data.shape[0]:] = 1
        yield final_data, final_label
        i += size


if __name__ == '__main__':
    # data = np.load('data/三分类/train_data_2d.npy', allow_pickle=True).astype(float)
    # label = np.load('data/三分类/train_label_2d.npy').astype(float)
    # get_three_class_data(data, label)

    data = np.load('data/二分类/train_data_2d.npy', allow_pickle=True).astype(float)
    label = np.load('data/二分类/train_label_2d.npy').astype(float)
    for new_data, new_label in generate_two_data(data, label):
        print(new_data.shape, new_label.shape)
    # print(new_label[-4419],new_label[-4418])

# get_two_class_data(data, label)
