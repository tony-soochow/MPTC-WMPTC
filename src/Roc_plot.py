from matplotlib import pyplot as plt


def plot_auc(avg_auc_all, result_tpr_all, result_fpr_all, avg_aucs):
    # models = ['W', 'W_PPI', 'W_CT', 'PPICT+', 'PPICT']
    # models = ['PTM_X', 'W', 'PPICT']
    # models = ['Cancer']
    # models = ['PPICT_Phos']
    models = ['PTM_X_Phos', 'PPICT_Phos']
    # models = ['Proteins_pairs']
    # models = ['PTM_X']
    for i in range(len(avg_auc_all)):
        print(len(result_fpr_all[i]), len(result_tpr_all[i]))
        if models[i] == "PPICT+":
            plt.plot(result_fpr_all[i], result_tpr_all[i], label='PPICT* AUC: %0.3f' % avg_aucs[models[i]])
        else:
            plt.plot(result_fpr_all[i], result_tpr_all[i], label=models[i] + ' AUC: %0.3f' % avg_aucs[models[i]])
        plt.legend(loc='lower right')
        plt.plot([0, 1], [0, 1], 'r--')
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        # plt.text(0.6, 0.05, 'Avg auc = %0.3f' % avg_auc_all[i], bbox=dict(facecolor='yellow', alpha=0.5), fontsize=15)
        plt.ylabel('True Positive Rate')
        plt.xlabel('False Positive Rate')
        plt.savefig('./Figure/Phos_Comp_auc_1216.png', dpi=400)
        print(avg_auc_all)


# plot ROC curve for classification

import numpy as np
import matplotlib.pyplot as plt


def set_style(label_size=12):
    import seaborn
    import matplotlib
    seaborn.set_style("white")
    seaborn.set_style("ticks")

    matplotlib.rcParams['grid.alpha'] = 0.4
    matplotlib.rcParams['xtick.labelsize'] = label_size
    matplotlib.rcParams['ytick.labelsize'] = label_size * 1.1
    matplotlib.rcParams['legend.fontsize'] = label_size * 1.1
    matplotlib.rcParams['axes.labelsize'] = label_size * 1.1
    matplotlib.rcParams['axes.titlesize'] = label_size * 1.2
    matplotlib.rcParams['axes.titleweight'] = 'bold'


def ROC_plot(state, scores, threshold=None, color=None, legend_on=True,
             label="predict.py", base_line=True, linewidth=1.0, rm_NA=True):
    """
    Plot ROC curve and calculate the Area under the curve (AUC) from the
    with the prediction scores and true labels.
    The threshold is the step of the ROC cureve.
    """

    score_gap = np.unique(scores)
    # print score_gap, len(score_gap), len(scores)
    if len(score_gap) > 2000:
        idx = np.random.permutation(len(score_gap))
        score_gap = score_gap[idx[:2000]]
    score_gap = np.append(np.min(score_gap) - 0.1, score_gap)
    score_gap = np.append(score_gap, np.max(score_gap) + 0.1)
    if threshold is not None:
        thresholds = np.sort(np.append(threshold, score_gap))
        print(thresholds)
        _idx = np.where(scores >= threshold)[0]
        print(_idx)
        _fpr = np.sum(state[_idx] == 0) / np.sum(state == 0).astype('float')
        print(_fpr)
        _tpr = np.sum(state[_idx] == 1) / np.sum(state == 1).astype('float')
        print(_tpr)
        # plt.scatter(_fpr, _tpr, marker="o", s=80, facecolors='none', edgecolors=color)
        if color is None:
            plt.plot(_fpr, _tpr, marker='o', markersize=8, mfc='none')
        else:
            plt.plot(_fpr, _tpr, marker='o', markersize=8, mec=color, mfc=color)

    else:
        thresholds = np.sort(score_gap)
    # thresholds = np.arange(np.min(threshold), 1+2*threshold, threshold)
    # plt.show()
    print(thresholds.shape)
    fpr, tpr = np.zeros(thresholds.shape[0]), np.zeros(thresholds.shape[0])
    for i in range(thresholds.shape[0]):
        idx = np.where(scores >= thresholds[i])[0]
        fpr[i] = np.sum(np.array(state)[idx] == 0) / np.sum(np.array(state) == 0).astype('float')
        tpr[i] = np.sum(np.array(state)[idx] == 1) / np.sum(np.array(state) == 1).astype('float')
    auc = 0
    for i in range(thresholds.shape[0] - 1):
        auc = auc + (fpr[i] - fpr[i + 1]) * (tpr[i] + tpr[i + 1]) / 2.0
    print(auc)

    if color is None:
        plt.plot(fpr, tpr, "-", linewidth=linewidth,
                 label="%s: AUC=%.3f" % (label, auc))
    else:
        plt.plot(fpr, tpr, "-", linewidth=linewidth, color=color,
                 label="%s: AUC=%.3f" % (label, auc))
    if base_line:
        plt.plot(np.arange(0, 2), np.arange(0, 2), "k--", linewidth=1.0,
                 label="random: AUC=0.500")

    if legend_on:
        plt.legend(loc="best", fancybox=True, ncol=1)

    plt.xlim(-0.01, 1.01)
    plt.ylim(-0.01, 1.01)
    plt.xlabel("False Positive Rate (1-Specificity)")
    plt.ylabel("True Positive Rate (Sensitivity)")

    plt.show()

    return fpr, tpr, thresholds, auc


