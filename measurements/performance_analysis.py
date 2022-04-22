import pandas as pd

from scripts.detectorgroup_box import detectorgroup_box


if __name__ == '__main__':
    # dataset_list = ['sapipin.csv', 'easy.csv', 'keystroke2014.csv', 'strong.csv', 'logicalstrong.csv']
    language = 'hu'
    detectorgroup_box(language)