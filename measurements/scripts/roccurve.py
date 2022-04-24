import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pyod.models.knn import KNN
from pyod.models.pca import PCA
from pyod.models.ocsvm import OCSVM
from pyod.models.lof import LOF
from pyod.models.hbos import HBOS
from pyod.models.iforest import IForest
from pyod.models.feature_bagging import FeatureBagging
from pyod.models.copod import COPOD
from pyod.models.abod import ABOD
from sklearn import metrics
import json


def read_from_json(lang):
    f = open('language/' + lang + '.json', encoding='utf-8')
    data = json.load(f)
    f.close()
    return data


def scores_calc(df, userid, percentage, detector):
    #kiszurjuk az adott userre vonatkozo sorokat, levagjuk a userid-t
    user_data = df.loc[df.iloc[:, -1].isin([userid])]
    user_data = user_data.drop(user_data.columns[-1], axis=1)

    row_num = user_data.shape[0]
    row_num_train_data = int(percentage * row_num)
    # print(row_num)
    # print(userid)

    #Kivalasztjuk a tanito adatokat

    user_train_data = user_data[0:row_num_train_data]
    user_train_data_array = user_train_data.values

    # row_num_test_data = row_num - row_num_train_data
    # print(row_num_test_data)
    #kivalasztjuk a pozitiv tesztadatokat
    user_test_data = user_data[row_num_train_data:row_num]
    user_test_data_array = user_test_data.values

    #kivalasztjuk a negativ (csalo) tesztadatokat
    other_users_data = df.loc[~df.iloc[:, -1].isin([userid])]
    other_users_data = other_users_data.drop(other_users_data.columns[-1], axis=1)
    other_users_array = other_users_data.values

    #Tanítás
    clf = detector
    clf.fit(user_train_data_array)

    #Tesztelés
    positive_scores = clf.decision_function(user_test_data_array)
    negative_scores = clf.decision_function(other_users_array)

    return (positive_scores, negative_scores)


def plot_ROC_curve(positive_scores, negative_scores, counter):
    zeros = np.zeros(len(negative_scores))
    ones = np.ones(len(positive_scores))
    y = np.concatenate((zeros, ones))
    scores = np.concatenate((negative_scores, positive_scores))
    FPR, TPR, _ = metrics.roc_curve(y, scores, pos_label=0)

    linestyles = ["dashdot", "dashed", "dotted", "solid","densely dashdotted", "dashdotted", "loosely dashdotted", "densely dashdotted" ]
    colors = ["#581845", "#D35400", "#0B1F64", "#C70039", "#64140B", "#556B58", "#FE11B6", "#0C453A"]

    auc = metrics.auc(FPR, TPR)
    plt.plot(
        FPR,
        TPR,
        color=colors[counter],
        linestyle=linestyles[counter],
        label="AUC %s blocks = %0.2f" % (1, auc),
    )
    fnr = 1 - TPR
    EER_fpr = FPR[np.argmin(np.absolute((fnr - FPR)))]
    EER_fnr = fnr[np.argmin(np.absolute((fnr - FPR)))]
    EER = 0.5 * (EER_fpr + EER_fnr)


def roccurve(selected_detector_group, selected_detector_group_name, selected_detector_group_title, language):
    data = read_from_json(language)
    Lcsv = ['sapipin.csv', 'easy.csv', 'keystroke2014.csv', 'strong.csv', 'logicalstrong.csv']
    for file in Lcsv:
        df = pd.read_csv(f'datasets/{file}')
        NUM_USERS = int(df.iloc[-1]['userid'])

        counter = 0
        percentage = 75
        percentage = percentage / 100

        # print(file)
        for j in selected_detector_group:
            detector = j
            all_positive_scores = []
            all_negative_scores = []
            # all pozitive and all negetive score calc
            for i in range(1, NUM_USERS + 1):
                userid = i
                (positive_scores, negative_scores) = scores_calc(df, userid, percentage, detector[0])
                all_positive_scores = all_positive_scores + list(positive_scores)
                all_negative_scores = all_negative_scores + list(negative_scores)
            plot_ROC_curve(all_positive_scores, all_negative_scores, counter)
            counter = counter + 1


        plt.legend([i[1] for i in selected_detector_group], loc="best")
        plt.title("AUC " + selected_detector_group_title)

        plt.xlabel(data["roccurve"]["fpr"])
        plt.ylabel(data["roccurve"]["tpr"])
        plt.grid()
        OUTPUT_PNG = 'plots/' + language + '/' + file.split(".")[0] + '/roccurve/'
        plt.savefig(OUTPUT_PNG + 'auc_' + str(selected_detector_group_name) + '.png')
        plt.close()