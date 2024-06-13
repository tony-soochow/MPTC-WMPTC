import time


def get_result(path, outpath):
    metric_result_all = {'accuracy': 0, 'auc': 0, 'precision': 0, 'sensitivity': 0, 'specificity': 0,
                         'true_positive_rate': 0, 'true_negative_rate': 0, 'false_positive_rate': 0,
                         'false_negative_rate': 0, 'f1_score': 0, 'matthews_correlation_coefficient': 0}

    def read_result(file_path, metric_result):
        with open(file_path, 'r') as f1:
            lines = [item.strip('\t\n') for item in f1.readlines()]
            for line in lines:
                if line.startswith('accuracy'):
                    items = line.split('\t')
                    for item in items:
                        # print(item.split(': '))
                        metric_result[item.split(': ')[0]] += float(item.split(': ')[1])

    read_result(path + '/Result_0307.txt', metric_result_all)

    def write_result(write_name, metric_result_all):
        for key in metric_result_all.keys():
            metric_result_all[key] /= 5
        print(metric_result_all)

        with open(outpath, 'a') as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n')
            f.write(write_name + '\n')
            for key in metric_result_all.keys():
                f.write(key + ': ' + str(round(metric_result_all[key], 3)) + '\t')
            f.write('\n')

    write_result('Result_0307: ', metric_result_all)


result_path = './RF_Result/'

# get_result(result_path + 'Intra_300/ML/', './Final_result/RF/Intra_ML_300.txt')
# get_result(result_path + 'Intra_500/ML/', './Final_result/RF/Intra_ML_500.txt')
# get_result(result_path + 'Intra_727/ML/', './Final_result/RF/Intra_ML_727.txt')
# get_result(result_path + 'Intra_300/WML/', './Final_result/RF/Intra_WML_300.txt')
# get_result(result_path + 'Intra_500/WML/', './Final_result/RF/Intra_WML_500.txt')
# get_result(result_path + 'Intra_727/WML/', './Final_result/RF/Intra_WML_727.txt')

get_result(result_path + 'Inter_1000/ML/', './Final_result/RF/Inter_ML_1000.txt')
get_result(result_path + 'Inter_2000/ML/', './Final_result/RF/Inter_ML_2000.txt')
get_result(result_path + 'Inter_3549/ML/', './Final_result/RF/Inter_ML_3549.txt')
get_result(result_path + 'Inter_1000/WML/', './Final_result/RF/Inter_WML_1000.txt')
get_result(result_path + 'Inter_2000/WML/', './Final_result/RF/Inter_WML_2000.txt')
get_result(result_path + 'Inter_3549/WML/', './Final_result/RF/Inter_WML_3549.txt')