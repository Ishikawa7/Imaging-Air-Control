# IMPORT LIBRARIES #####################################################################################################
import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import Dash, Input, Output, State, callback, html, dcc
import dash_bootstrap_components as dbc
import cv2
import base64

dash.register_page(
    __name__,
    path='/',
    )

# LOAD RESOURCES #######################################################################################################
activated = False
if not activated:
    activated = True
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

def generate_frames():
    #print(cv2.getBuildInformation())
    while True:
        success, frame = cap.read()  # Read frame from webcam
        if not success:
            print('Empty frame')
            # generate empty frame
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            #break
        else:
            #_, buffer = cv2.imencode('.jpg', frame)
            #frame_bytes = base64.b64encode(buffer)
            #frame_base64 = 'data:image/jpeg;base64,' + frame_bytes.decode('utf-8')
            pass
        yield frame

def create_layout_home():

    return dbc.Container(
        [
            html.Br(),
            html.Div([
                html.Img(id='video', style={'width': '100%', 'height': 'auto'}),
                dcc.Interval(id='interval-component', interval=1000)
            ]),
        ],
    )

layout = create_layout_home

@callback(
    Output('video', 'src'),
    Input('interval-component', 'n_intervals')
)
def update_video_src(autoPlay):
    return next(generate_frames())