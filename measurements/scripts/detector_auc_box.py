import pandas as pd
import matplotlib.pyplot as plt
import json


def read_from_json(lang):
    f = open('language/' + lang + '.json', encoding='utf-8')
    data = json.load(f)
    f.close()
    return data


def my_boxplot_auc(dataset1, dataset2, dataset3, dataset4, dataset5, detector, data,  language):
    data_auc = [dataset1.iloc[:, -1], dataset2.iloc[:, -1], dataset3.iloc[:, -1], dataset4.iloc[:, -1], dataset5.iloc[:, -1]]

    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111)
    bp = ax.boxplot(data_auc, widths=(0.5, 0.5, 0.5, 0.5, 0.5), patch_artist=True)

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
    ax.set_xticklabels(['sapipin', 'easy', 'strong', 'logicalstrong', 'keystroke2014'])
    ax.set_xlabel(data['detector_auc_box']['dataset'], **font, size=fontsize)
    ax.set_ylabel("AUC", **font, size=fontsize)
    ax.set_title(str(detector.upper() + data['detector_auc_box']['compare_models']), **font, size=fontsize-2)
    plt.savefig("plots/" + language + '/all_dataset/' + detector + '_auc.png')


def detector_auc_box(language):
    data = read_from_json(language)
    csv_files_list = ["sapipin_pca.csv", "easy_pca.csv", "strong_pca.csv", "logicalstrong_pca.csv", "keystroke2014_pca.csv",
                      "sapipin_abod.csv", "easy_abod.csv", "strong_abod.csv", "logicalstrong_abod.csv", "keystroke2014_abod.csv",
                      "sapipin_copod.csv", "easy_copod.csv", "strong_copod.csv", "logicalstrong_copod.csv","keystroke2014_copod.csv",
                      "sapipin_fb.csv", "easy_fb.csv", "strong_fb.csv", "logicalstrong_fb.csv","keystroke2014_fb.csv",
                      "sapipin_hbos.csv", "easy_hbos.csv", "strong_hbos.csv", "logicalstrong_hbos.csv","keystroke2014_hbos.csv",
                      "sapipin_iforest.csv", "easy_iforest.csv", "strong_iforest.csv", "logicalstrong_iforest.csv","keystroke2014_iforest.csv",
                      "sapipin_knn.csv", "easy_knn.csv", "strong_knn.csv", "logicalstrong_knn.csv","keystroke2014_knn.csv",
                      "sapipin_lof.csv", "easy_lof.csv", "strong_lof.csv", "logicalstrong_lof.csv","keystroke2014_lof.csv",
                      "sapipin_ocsvm.csv", "easy_ocsvm.csv", "strong_ocsvm.csv", "logicalstrong_ocsvm.csv","keystroke2014_ocsvm.csv",
                      ]
    file_index = 0
    while file_index < len(csv_files_list):
        dataset1 = pd.read_csv("detectors_output/" + str(csv_files_list[file_index]))
        dataset2 = pd.read_csv("detectors_output/" + str(csv_files_list[file_index+1]))
        dataset3 = pd.read_csv("detectors_output/" + str(csv_files_list[file_index+2]))
        dataset4 = pd.read_csv("detectors_output/" + str(csv_files_list[file_index+3]))
        dataset5 = pd.read_csv("detectors_output/" + str(csv_files_list[file_index+4]))

        detector = csv_files_list[file_index].split('_')[1].split('.')[0]
        my_boxplot_auc(dataset1, dataset2, dataset3, dataset4, dataset5, detector, data, language)
        file_index = file_index + 5