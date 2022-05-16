#konyvtarak importalasa
import numpy as np
import pandas as pd
from pyod.models.knn import KNN
from pyod.models.pca import PCA
from pyod.models.mcd import MCD
from pyod.models.ocsvm import OCSVM
from pyod.models.lof import LOF
from pyod.models.cblof import CBLOF
from pyod.models.hbos import HBOS
from pyod.models.iforest import IForest
from pyod.models.feature_bagging import FeatureBagging
from pyod.models.loda import LODA
from pyod.models.copod import COPOD
from pyod.models.abod import ABOD
from sklearn import metrics


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
    clf = detector[0]
    clf.fit(user_train_data_array)

    #Tesztelés
    positive_scores = clf.decision_function(user_test_data_array)
    negative_scores = clf.decision_function(other_users_array)

    return (positive_scores, negative_scores)


def eer_auc_calc(NUM_USERS, percentage, detector, df, FILENAME):

    dictlist = []

    for i in range(1, NUM_USERS + 1):
        userid = i
        (positive_scores, negative_scores) = scores_calc(df, userid, percentage, detector)
        # dictlist.append(my_dict)
        zeros = np.zeros(len(negative_scores))
        ones = np.ones(len(positive_scores))
        y = np.concatenate((zeros, ones))
        scores = np.concatenate((negative_scores, positive_scores))
        FPR, TPR, _ = metrics.roc_curve(y, scores, pos_label=0)
        AUC = metrics.auc(FPR, TPR)
        fnr = 1 - TPR
        EER_fpr = FPR[np.argmin(np.absolute((fnr - FPR)))]
        EER_fnr = fnr[np.argmin(np.absolute((fnr - FPR)))]
        EER = 0.5 * (EER_fpr + EER_fnr)
        my_dict = {
            "userid": userid,
            "EER": EER,
            "AUC": AUC
        }
        dictlist.append(my_dict)

    dataframe = pd.DataFrame.from_dict(dictlist, orient='columns')
    dataframe.to_csv('detectors_output/' + FILENAME + "_" + str(detector[1]), index=False)
    return (dataframe["EER"].mean(), dataframe["AUC"].mean(), dataframe["EER"].std(), dataframe["AUC"].std())


if __name__ == '__main__':
    Lcsv = ['sapipin.csv', 'easy.csv', 'keystroke2014.csv', 'strong.csv', 'logicalstrong.csv']
    for file in Lcsv:
        df = pd.read_csv(f'datasets/{file}')
        FILENAME = file

        NUM_USERS = int(df.iloc[-1]['userid'])
        counter = 0
        percentage = 75
        percentage = percentage / 100


        models = [(PCA(random_state=131), "pca.csv") , (OCSVM(), "ocsvm.csv"),
            (KNN(n_neighbors=3), "knn.csv"), (HBOS(), "hbos.csv"),
            (LOF(), "lof.csv"), (IForest(), "iforest.csv"),
            (COPOD(), "copod.csv"), (ABOD(), "abod.csv"),
            (FeatureBagging(), "fb.csv")]

        for detector in models:
            #mean
            (eer_mean, auc_mean, eer_std, auc_std) = eer_auc_calc(NUM_USERS, percentage, detector, df, FILENAME.split('.')[0])

            # print(auc_mean, auc_std, eer_mean, eer_std)

