# import simple queue
from queue import SimpleQueue
import pickle as pkl
# create a static class to hold the image and process it
class FrameAnomalyDetector:
    frames_queue = SimpleQueue(maxsize=1)
    # load frame anomaly model with pickle
    with open('frame_anomaly_model.pkl', 'rb') as f:
        frame_anomaly_model = pkl.load("iforest_model_detected.pkl")

    @staticmethod
    def get_frame_anomaly():
        last_frame = FrameAnomalyDetector.frames_queue.get()
        return FrameAnomalyDetector.frame_anomaly_model.predict(last_frame)
