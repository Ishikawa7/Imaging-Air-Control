# import simple queue
from queue import Queue
import pickle
import numpy as np
class VariablesAnomalyDetector:
    an_log = [0]
    # load frame anomaly model with pickle
    variables_anomaly_model = pickle.load(open('iforest_model_variables.pkl', 'rb'))

    @staticmethod
    def get_variables_anomaly(status_dict):
        #if len(VariablesAnomalyDetector.an_log) == 1:
        #    return 0
        array_status_dict = np.array(list(status_dict.values())).reshape(1, -1)
        an_score =  round(VariablesAnomalyDetector.variables_anomaly_model.decision_function(array_status_dict)[0], 3)
        VariablesAnomalyDetector.an_log.append(an_score)
        return an_score