import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json


def read_from_json(lang):
    f = open('language/' + lang + '.json', encoding='utf-8')
    data = json.load(f)
    f.close()
    return data


def my_boxplot_auc(dataset1, dataset2, directory, legend, iterator, language):
    data = read_from_json(language)
    data_eer = [dataset1.iloc[:, -1], dataset2.iloc[:, -1]]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    bp = ax.boxplot(data_eer, widths=(0.5, 0.5), patch_artist=True)

    #szines, vonalvastagsagok, stb.
    colors = ['#D35400', '#219631', '#3e4444', '#405d27', '#bc5a45']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)

    for whisker in bp['whiskers']:
        whisker.set(color='#000000',
                    linewidth=1.5,
                    linestyle="-")
    #median vonal
    for median in bp['medians']:
        median.set(color='k', linewidth=1.5)

    fontsize = 16
    font = {'fontname': 'Times New Roman'}
    ax.set_xticklabels(legend)
    ax.set_xlabel(data['detector_auc_box']['detector'], **font, size=fontsize)
    ax.set_ylabel("AUC", **font, size=fontsize)


    if iterator == 1 :
        ax.set_title(data['detector_auc_box']['auc_linear'], **font, size=fontsize - 2)
        plt.savefig(directory + 'AUC_linear.png')
    if iterator == 2:
        ax.set_title(data['detector_auc_box']['auc_ensemble'], **font, size=fontsize - 2)
        plt.savefig(directory + 'AUC_outlier_ensemble.png')
    if iterator == 3:
        ax.set_title(data['detector_auc_box']['auc_probabilistic'], **font, size=fontsize - 2)
        plt.savefig(directory + 'AUC_probabilistic.png')


def my_boxplot3_auc(dataset1, dataset2, dataset3, directory, legend, language):
    data = read_from_json(language)
    data_eer = [dataset1.iloc[:, -1], dataset2.iloc[:, -1], dataset3.iloc[:, -1]]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    bp = ax.boxplot(data_eer, widths=(0.5, 0.5, 0.5), patch_artist=True)

    #szines, vonalvastagsagok, stb.
    colors = ['#D35400', '#219631', '#3e4444', '#405d27', '#bc5a45']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)

    for whisker in bp['whiskers']:
        whisker.set(color='#000000',
                    linewidth=1.5,
                    linestyle="-")
    #median vonal
    for median in bp['medians']:
        median.set(color='k', linewidth=1.5)

    fontsize = 16
    font = {'fontname': 'Times New Roman'}
    ax.set_xticklabels(legend)
    ax.set_xlabel(data['detector_auc_box']['detector'], **font, size=fontsize)
    ax.set_ylabel("AUC", **font, size=fontsize)

    ax.set_title(data['detector_auc_box']['auc_proximity'], **font, size=fontsize - 2)
    plt.savefig(directory + 'AUC_proximity_based.png')


def get_detectors(group):
    L = []
    for detector in group:
        temp = str(detector).split("_")[1]
        detector = temp.split('.')[0]
        L = L +[detector]
    L = np.unique((L))
    L = [each_string.upper() for each_string in L]
    return L


def detector_auc_box(language):

    L = []
    csv_files_list_linear = ["sapipin_ocsvm.csv","sapipin_pca.csv",
                             "easy_ocsvm.csv", "easy_pca.csv",
                              "strong_ocsvm.csv", "strong_pca.csv",
                             "logicalstrong_ocsvm.csv", "logicalstrong_pca.csv",
                             "keystroke2014_ocsvm.csv", "keystroke2014_pca.csv"]
    L = L + [csv_files_list_linear]
    csv_files_list_ensemble = ["sapipin_fb.csv", "sapipin_iforest.csv",
                              "easy_fb.csv", "easy_iforest.csv",
                              "strong_fb.csv", "strong_iforest.csv",
                              "logicalstrong_fb.csv", "logicalstrong_iforest.csv",
                              "keystroke2014_fb.csv", "keystroke2014_iforest.csv"]
    L = L + [csv_files_list_ensemble]
    csv_files_list_probabilistic = ["sapipin_abod.csv", "sapipin_copod.csv",
                               "easy_abod.csv","easy_copod.csv",
                               "strong_abod.csv", "strong_copod.csv",
                               "logicalstrong_abod.csv", "logicalstrong_copod.csv",
                               "keystroke2014_abod.csv", "keystroke2014_copod.csv", ]
    L = L + [csv_files_list_probabilistic]
    csv_files_list_proximity = ["sapipin_hbos.csv", "sapipin_knn.csv", "sapipin_lof.csv",
                                    "easy_hbos.csv", "easy_knn.csv", "easy_lof.csv",
                                    "strong_hbos.csv", "strong_knn.csv", "strong_lof.csv",
                                    "logicalstrong_hbos.csv", "logicalstrong_knn.csv", "logicalstrong_lof.csv",
                                    "keystroke2014_hbos.csv",  "keystroke2014_knn.csv", "keystroke2014_lof.csv",]
    L = L + [csv_files_list_proximity]



    iterator = 0
    for group in L:
        file_index = 0
        iterator = iterator + 1
        OUTPUT_PNG = 'plots/' + language + '/'

        legend = get_detectors(group)
        while file_index < len(group):
            if iterator < 4:
                dataset1 = pd.read_csv("detectors_output/" + str(group[file_index]))
                file_index = file_index + 1
                dataset2 = pd.read_csv("detectors_output/" + str(group[file_index]))
                directory = OUTPUT_PNG + group[file_index].split('_')[0] + '/' + 'detector_auc_box/'
                file_index = file_index + 1

                my_boxplot_auc(dataset1, dataset2, directory, legend, iterator, language)


            else:
                dataset1 = pd.read_csv("detectors_output/" + str(group[file_index]))
                file_index = file_index + 1
                dataset2 = pd.read_csv("detectors_output/" + str(group[file_index]))
                file_index = file_index + 1
                dataset3 = pd.read_csv("detectors_output/" + str(group[file_index]))
                directory = OUTPUT_PNG + group[file_index].split('_')[0] + '/' + 'detector_auc_box/'
                file_index = file_index + 1

                my_boxplot3_auc(dataset1, dataset2, dataset3, directory, legend, language)


