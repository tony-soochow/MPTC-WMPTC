import time

import matplotlib.pyplot as plt
import numpy as np

from model.cal.cal_metric import cal_two_class_roc
from model.Rf_model import Rf_model
from model.Fnn_model import Fnn_model
from model.Lstm_attention_model import Lstm_attention_model
from Roc_plot import plot_auc, ROC_plot

Intra_WML = '../Proteins_Samples/Intra/WML'
Inter_WML = '../Proteins_Samples/Inter/WML'

Train_set_path = '/Train'
Test_set_path = '/Test'

result_fpr_all = []
result_tpr_all = []
avg_auc_all = []


def get_result(model, Train_samplepath, Test_samplepath, nums, outpath):
    avg_auc = 0
    bias_min = 1
    result_fpr = []
    result_tpr = []
    auc_alls = []
    pred_probs = []
    preds = []
    labels = []

    for num in range(nums):
        metric_result = {'accuracy': 0, 'precision': 0, 'sensitivity': 0, 'specificity': 0,
                         'true_positive_rate': 0, 'true_negative_rate': 0, 'false_positive_rate': 0,
                         'false_negative_rate': 0, 'f1_score': 0, 'auc': 0, 'matthews_correlation_coefficient': 0}
        # metric_roc = {'fpr': [], 'tpr': []}
        test_label, pred, pred_prob, _, metric, fpr, tpr, threshold = model(
            Train_samplepath + '/sample' + str(num) + '.npy',
            Test_samplepath + '/sample' + str(int(num/5)) + '.npy')
        print(num, ': ', metric)
        print(len(fpr), len(tpr), len(threshold))
        preds += pred.tolist()
        pred_probs += pred_prob.tolist()
        labels += test_label.tolist()

        def merge_dict(y, x):
            for k, v in x.items():
                if k in y.keys():
                    y[k] += v
                else:
                    y[k] = v

        merge_dict(metric_result, metric)

        def write_result(outpath, metric_result):
            with open(outpath, 'a') as f:
                f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n')
                f.write('sample ' + str(num) + '\n')
                for key in metric_result.keys():
                    f.write(key + ': ' + str(round(metric_result[key], 3)) + '\t')
                f.write('\n')

        write_result(outpath + 'Result_0307.txt', metric_result)
        auc_alls.append(metric_result['auc'])

        if num == nums - 1:
            final_fpr, final_tpr, thresholds = cal_two_class_roc(np.array(labels), np.array(pred_probs))
            # with open('./Figure_result/roc_' + outpath.split('/')[2] + 'AUC_Alphafold_0801.txt', 'w') as f1:
            #     f1.writelines(' '.join([str(item) for item in final_fpr]))
            #     f1.write('\n')
            #     f1.writelines(' '.join([str(item) for item in final_tpr]))
            result_fpr_all.append(final_fpr)
            result_tpr_all.append(final_tpr)
            avg_auc_all.append(sum(auc_alls) / nums)


# Samples_path = '../Samples/Inter/WML/'
# Result_path = './Result/Inter/WML/'
get_result(Rf_model, Intra_WML+Train_set_path, Intra_WML+Test_set_path, 5, './Proteins_RF_Result/Intra/')
get_result(Rf_model, Inter_WML+Train_set_path, Inter_WML+Test_set_path, 5, './Proteins_RF_Result/Inter/')


def plot_auc():
    # models = ['Intra_ML_300']
    # models = ['Intra_ML_300', 'Intra_ML_500', 'Intra_ML_727', 'Intra_WML_300', 'Intra_WML_500', 'Intra_WML_727']
    models = ['Inter_ML_1000', 'Inter_ML_2000', 'Inter_ML_3549', 'Inter_WML_1000', 'Inter_WML_2000', 'Inter_WML_3549']
    # models = ['Intra_WML_300', 'Intra_WML_500', 'Intra_WML_727']
    for i in range(len(avg_auc_all)):
        print(len(result_fpr_all[i]), len(result_tpr_all[i]))
        plt.plot(result_fpr_all[i], result_tpr_all[i], label=models[i] + ' AUC: %0.3f' % avg_auc_all[i])
        plt.legend(loc='lower right')
        plt.plot([0, 1], [0, 1], 'r--')
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        # plt.text(0.6, 0.05, 'Avg auc = %0.3f' % avg_auc_all[i], bbox=dict(facecolor='yellow', alpha=0.5), fontsize=15)
        plt.ylabel('True Positive Rate', fontdict={'family': 'Times New Roman',
                                                   'weight': 'normal',
                                                   'size': 20, })
        plt.xlabel('False Positive Rate', fontdict={'family': 'Times New Roman',
                                                    'weight': 'normal',
                                                    'size': 20, })
        plt.savefig('./Fig/Inter.png', dpi=400)


# plot_auc()
print(avg_auc_all)
