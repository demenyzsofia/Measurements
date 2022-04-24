import pandas as pd

from scripts.detectorgroup_box import detectorgroup_box
from scripts.detector_auc_box import detector_auc_box
from scripts.detector_eer_box import detector_eer_box


if __name__ == '__main__':
    # dataset_list = ['sapipin.csv', 'easy.csv', 'keystroke2014.csv', 'strong.csv', 'logicalstrong.csv']
    language = 'en'

    # detectorgroup_box(language)

    #detector_auc_box(language)

    detector_eer_box(language)