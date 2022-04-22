import pandas as pd

from scripts.hist import all_user_HT_hist
from scripts.hist import all_user_UD_hist
from scripts.line import typing_line_plot_sapipin
from scripts.line import typing_line_plot_datasets


def hist_plot(dataset, colors, counter, columns, OUTPUT_PNG, language):
    """
            hist plots
    """
    all_user_HT_hist(dataset, colors, counter, columns, OUTPUT_PNG, language)
    all_user_UD_hist(dataset, colors, counter, columns, OUTPUT_PNG, language)


def line_plot(dataset, head_list, OUTPUT_PNG, language):
    """
            line plots
    """
    if file == 'sapipin.csv':
        for i in range(1, NUM_USERS + 1):
            typing_line_plot_sapipin(dataset, i, head_list, OUTPUT_PNG, language)
    else:
        UD_poz = 0
        for head in head_list:
            if 'HT' in head:
                UD_poz = UD_poz + 1
        for i in range(1, NUM_USERS + 1):
            typing_line_plot_datasets(dataset, i, head_list, UD_poz, OUTPUT_PNG, language)


if __name__ == '__main__':
    dataset_list = ['sapipin.csv', 'easy.csv', 'keystroke2014.csv', 'strong.csv', 'logicalstrong.csv']
    language = 'hu'

    for file in dataset_list:
        #colors for diagrams
        colors = ["#6A5ACD", "#008080", "#4682B4", "#87CEEB", "#4169E1", "#191970", "#778899", "#2F4F4F"]
        counter = 0

        #the current dataset name
        FILENAME = file
        #read the dataset
        dataset = pd.read_csv(f'datasets/{file}')

        #number of users in dataset
        NUM_USERS = int(dataset.iloc[-1]['userid'])


        """
            hist plots
        """
        last_column = dataset[dataset.columns[-1]]
        dataset_without_idColumn = dataset.iloc[:, :-1]
        value = 1000
        dataset_without_idColumn = (dataset_without_idColumn * value)
        dataset_without_idColumn['userid'] = last_column

        columns = []
        for col_name in dataset_without_idColumn.columns:
            columns = columns + [col_name]
        columns = columns[:-1]

        OUTPUT_PNG = "plots/" + language + "/" + file.split(".")[0] + "/hist/"
        # hist_plot(dataset_without_idColumn, colors, counter, columns, OUTPUT_PNG, language)


        """
        line plots
        """
        head_list = list(dataset.columns)
        head_list = head_list[:-1]
        OUTPUT_PNG = "plots/" + language + "/" + file.split(".")[0] + "/line/"
        line_plot(dataset, head_list, OUTPUT_PNG, language)








