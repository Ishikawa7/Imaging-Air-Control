# import simple queue
from queue import SimpleQueue
import pickle as pkl
# create a static class to hold the image and process it
class VariablesAnomalyDetector:
    variables_queue = SimpleQueue(maxsize=1)
    # load frame anomaly model with pickle
    with open('variables_anomaly_model.pkl', 'rb') as f:
        variables_anomaly_model = pkl.load("iforest_model_variables.pkl")

    @staticmethod
    def get_frame_anomaly():
        last_variables = VariablesAnomalyDetector.variables_queue.get()
        return VariablesAnomalyDetector.variables_anomaly_model.predict(last_variables)
