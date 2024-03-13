# import simple queue
from queue import Queue
import pickle

class FrameAnomalyDetector:
    detected = Queue(maxsize=1)
    an_log = [0]
    # load frame anomaly model with pickle
    frame_anomaly_model = pickle.load(open('iforest_model_detected.pkl', 'rb'))
    
    @staticmethod
    def update_detected(df_detected):
        FrameAnomalyDetector.detected.put(df_detected)

    @staticmethod
    def get_frame_anomaly():
        # if queue is empty, return 0
        if FrameAnomalyDetector.detected.empty():
            return FrameAnomalyDetector.an_log[-1]
        df_detected = FrameAnomalyDetector.detected.get()
        an_score =  round(FrameAnomalyDetector.frame_anomaly_model.decision_function(df_detected)[0] * 10, 3)
        FrameAnomalyDetector.an_log.append(an_score)
        return an_score 
