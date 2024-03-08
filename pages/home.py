# IMPORT LIBRARIES #####################################################################################################
import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import Dash, Input, Output, State, callback, html, dcc
import dash_bootstrap_components as dbc
import time
import cv2

dash.register_page(
    __name__,
    path='/',
    )

# LOAD RESOURCES #######################################################################################################
cam = None
index = 1

def create_layout_home():

    return dbc.Container(
        [
            html.Br(),
            html.Div([
                html.Img(id='video', style={'width': '100%', 'height': 'auto'}),
                dcc.Graph(id='video-frame', figure=px.imshow(np.zeros((480, 640, 3), dtype=np.uint8)), style={'width': '100%', 'height': 'auto'}, config={'displayModeBar': False}),
                dcc.Interval(id='interval-component', interval=10)
            ]),
        ],
    )

layout = create_layout_home

@callback(
    Output('video-frame', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_video_src(n_intervals):
    global cam, index
    if cam is None:
        cam = cv2.VideoCapture(0)
        cam.release()
        cam = cv2.VideoCapture(0)
    success, frame = cam.read()  # Read frame from webcam
    print("Success: ", success, "Cap: ", cam, "Cap isOpened: ", cam.isOpened())
    #cam.release()
    if not success:
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
    frame_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    fig = px.imshow(frame_image)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    return fig#VideoStream.get_frame_fig()