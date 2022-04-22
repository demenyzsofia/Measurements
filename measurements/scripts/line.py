import matplotlib.pyplot as plt
import pandas as pd
import json


def read_from_json(lang):
    f = open('language/' + lang + '.json', encoding='utf-8')
    data = json.load(f)
    f.close()
    return data


def typing_line_plot_sapipin(dataset, user_number, head_list, OUTPUT_PNG, language):
    data = read_from_json(language)
    userdata_lower_limit = user_number * 20 - 20
    userdata_upper_limit = user_number * 20
    HT1_userdata = dataset[userdata_lower_limit:userdata_upper_limit][head_list[0:1]]
    HT2_userdata = dataset[userdata_lower_limit:userdata_upper_limit][head_list[1:2]]
    HT3_userdata = dataset[userdata_lower_limit:userdata_upper_limit][head_list[2:3]]
    HT4_userdata = dataset[userdata_lower_limit:userdata_upper_limit][head_list[3:4]]
    HT5_userdata = dataset[userdata_lower_limit:userdata_upper_limit][head_list[4:5]]
    HT6_userdata = dataset[userdata_lower_limit:userdata_upper_limit][head_list[5:6]]
    UD1_userdata = dataset[userdata_lower_limit:userdata_upper_limit][head_list[11:12]]
    UD2_userdata = dataset[userdata_lower_limit:userdata_upper_limit][head_list[12:13]]
    UD3_userdata = dataset[userdata_lower_limit:userdata_upper_limit][head_list[13:14]]
    UD4_userdata = dataset[userdata_lower_limit:userdata_upper_limit][head_list[14:15]]
    UD5_userdata = dataset[userdata_lower_limit:userdata_upper_limit][head_list[15:16]]
    userdata = pd.concat([HT1_userdata, UD1_userdata, HT2_userdata, UD2_userdata, HT3_userdata, UD3_userdata,
                          HT4_userdata, UD4_userdata, HT5_userdata, UD5_userdata,  HT6_userdata], axis=1)

    plt.figure(figsize=(7, 4))
    for i in range(20):
        plt.plot(userdata.iloc[i])

    plt.xlabel(data['line']['x_label'])
    plt.ylabel(data['line']['y_label'])
    csfont = {'fontname': 'Comic Sans MS'}
    plt.title(str(user_number) + data['line']['title'], **csfont, fontsize='16')
    plt.savefig(OUTPUT_PNG + "user" + str(user_number) + "_typing" + '.png')
    # plt.show()
    plt.close()


def typing_line_plot_datasets(df, userid, head_list, UP_poz, OUTPUT_PNG, language):
    data = read_from_json(language)
    user_data = df.loc[df.iloc[:, -1].isin([userid])]
    dataframe = pd.DataFrame()
    for i in range(UP_poz-1):
        dataframe[head_list[i]] = user_data[head_list[i]]
        dataframe[head_list[UP_poz + i]] = user_data[head_list[UP_poz + i]]
    dataframe[head_list[UP_poz-1]] = user_data[head_list[UP_poz-1]]

    head_list = list(dataframe.columns)
    dataframe1 = dataframe[head_list[0: int(len(head_list)/2)]]
    dataframe2 = dataframe[head_list[int(len(head_list)/2): len(head_list)]]


    plt.figure(1, figsize=(7, 4))
    plt.subplot2grid((2, 2), (0, 0), colspan=2)
    for i in range (user_data.shape[1]):
        plt.plot(dataframe1.iloc[i])
    plt.xlabel(data['line']['x_label'])
    plt.ylabel(data['line']['y_label'])

    csfont = {'fontname': 'Comic Sans MS'}
    plt.title(str(userid) + data['line']['title'], **csfont, fontsize='14')

    plt.subplot2grid((2, 2), (1, 0), colspan=2)
    for i in range(user_data.shape[1]):
        plt.plot(dataframe2.iloc[i])

    plt.xlabel(data['line']['x_label'])
    plt.ylabel(data['line']['y_label'])


    plt.savefig(OUTPUT_PNG + "user" + str(userid) + "_typing" + '.png')
    # plt.show()
    plt.close()








