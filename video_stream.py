import cv2
import plotly.express as px
import numpy as np

class VideoStream():
    cam = cv2.VideoCapture(0)
    index = 0

    @classmethod
    def get_frame_fig(cls):
        #print(cv2.getBuildInformation())
        success, frame = VideoStream.cam.read()  # Read frame from webcam
        print("Success: ", success, "Frame: ", frame, "Index: ", VideoStream.index, "Cap: ", VideoStream.cam, "Cap isOpened: ", VideoStream.cam.isOpened())
        if not success:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
        frame_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        fig = px.imshow(frame_image)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        return fig