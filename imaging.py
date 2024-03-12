import cv2
import torch
from simulator import Simulator

class Imaging:
    cap = cv2.VideoCapture(0)
    cap.release()
    cap = cv2.VideoCapture(0)
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5n.pt')

    # Function to generate frames from webcam
    @staticmethod
    def generate_frames():
        while True:
            ret, frame = Imaging.cap.read()
            if not ret:
                continue
            model_results = Imaging.model(frame)
            obj_detected = model_results.pandas().xyxy[0][["name"]].values
            count_person = np.count_nonzero(obj_detected == "person")
            Simulator.update_people(count_person)
            #df_detected = pd.DataFrame(columns=list(model_results.names.values()))
            ret, buffer = cv2.imencode('.jpg', model_results.render()[0])
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')