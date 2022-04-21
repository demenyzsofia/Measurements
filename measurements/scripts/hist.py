import matplotlib.pyplot as plt
import json


f = open('language/hu.json', encoding='utf-8')
data = json.load(f)
f.close()

def all_user_HT_hist(dataset, colors, counter, columns, OUTPUT_PNG):
    for i in range(len(columns)):
        if 'HT' in columns[i]:
            plt.hist(dataset.iloc[:, i], bins=30, edgecolor=colors[counter], alpha=0.6)
            counter = counter + 1
            if counter == 8:
                counter = 1

            plt.legend([columns[i]],  loc="best")
            plt.xlabel("HT" + str(i+1) + " (ms)")
            plt.ylabel(data['hist']['y_label'])
            plt.title("HT" + str(i+1) + " (ms) " + data['hist']['title'])
            plt.savefig(OUTPUT_PNG + columns[i] + ".png")
            plt.close()


def all_user_UD_hist(dataset , colors, counter, columns, OUTPUT_PNG):
    for i in range(len(columns)):
        if 'RP' in columns[i] or 'UD' in columns[i]:
            plt.hist(dataset.iloc[:, i], bins=30, edgecolor=colors[counter], alpha=0.6)
            counter = counter + 1
            if counter == 8:
                counter = 1

            plt.legend([columns[i]], loc="best")
            plt.xlabel(columns[i] + " (ms)")
            plt.title(columns[i] + " (ms) " + data['hist']['title'])
            plt.ylabel(data['hist']['y_label'])
            plt.savefig(OUTPUT_PNG +  columns[i] + ".png")
            plt.close()



