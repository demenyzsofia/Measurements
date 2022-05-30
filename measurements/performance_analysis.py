from pyod.models.knn import KNN
from pyod.models.pca import PCA
from pyod.models.ocsvm import OCSVM
from pyod.models.lof import LOF
from pyod.models.hbos import HBOS
from pyod.models.iforest import IForest
from pyod.models.feature_bagging import FeatureBagging
from pyod.models.copod import COPOD
from pyod.models.abod import ABOD
import json
from scripts.detectorgroup_box import detectorgroup_box
from scripts.detector_auc_box import detector_auc_box
from scripts.detector_eer_box import detector_eer_box
from scripts.roccurve import roccurve


def read_from_json(lang):
    f = open('language/' + lang + '.json', encoding='utf-8')
    data = json.load(f)
    f.close()
    return data


if __name__ == '__main__':
    """
    select the language
    """
    language = 'en'
    #language = 'hu'

    """
    Detector group - box plots
    """
    #detectorgroup_box(language)

    """
    Detector auc - box plots
    """
    #detector_auc_box(language)

    """
    Detector eer - box plots
    """
    #detector_eer_box(language)




    data = read_from_json(language)
    """
    Detector group - roccurve plots
    """
    linear_models = [(PCA(random_state=131), "PCA"), (OCSVM(), "OCSVM")]
    proximity_based = [(LOF(), "LOF"), (KNN(n_jobs=3), "KNN"), (HBOS(), "HBOS")]
    outlier_ensembles = [(IForest(), "IForest"), (FeatureBagging(), "FB")]
    probabilistic = [(COPOD(), "COPOD"), (ABOD(), "ABOD")]


    """
    select a dataset
    """
    #file = 'easy.csv'
    #file = 'keystroke2014.csv'
    #file = 'logicalstrong.csv'
    #file = 'strong.csv'
    file = 'sapipin.csv'

    """
    select a detector group
    """
    roccurve(linear_models, "linear_models", data["roccurve"]["linear_models"], language, file)
    #roccurve(proximity_based, "proximity_based", data["roccurve"]["proximity_based"], language, file)
    #roccurve(outlier_ensembles, "outlier_ensembles", data["roccurve"]["outlier_ensembles"], language, file)
    #roccurve(probabilistic, "probabilistic", data["roccurve"]["probabilistic"], language, file)