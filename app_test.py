import cv2
import base64
import numpy as np
from flask import Flask, Response
import dash
from dash import html
from dash.dependencies import Input, Output
from dash import dcc
import dash_bootstrap_components as dbc
import torch
import pandas as pd

# css file for dash components
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# Initialize Flask app
server = Flask(__name__)

# Initialize Dash app
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.LUX, dbc_css])

def create_app_layout():
    return dbc.Container(
        [
            dbc.NavbarSimple(
                id = "navbar",
                children=[
                    dbc.NavItem(dbc.NavLink("Pagina iniziale", href="/", style={'font-size': '15px'})),
                    ## add space between images
                    #html.Div(style={'display': 'inline-block', 'width': '5px'}),
                    #html.Img(src='/static/icons/Logo_semeion.png', height="100px"),
                ],
                brand="Air Quality Controller Simulator",
                brand_href="#",
                color="primary",
                dark=True,
            ),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H3("Webcam Video Stream"),
                            html.Img(id='live-update-image', src='/static/webcam_logo.png'),
                            html.Br(),
                            html.Br(),
                            dbc.Row(
                                [
                                    dbc.Col(dbc.Button("Start", id="start-button", n_clicks=0, color="primary", className="mr-1"), width=6),
                                    dbc.Col(dbc.Button("Stop", id="stop-button", n_clicks=0, color="danger", className="mr-1"), width=6),
                                ],
                            ),
                        ],
                        width=6,
                    ),
                    dbc.Col(
                        [
                            dcc.Graph(
                                id='live-update-graph',
                                style={'width': '100%', 'height': 'auto'}
                            ),
                            html.Br(),
                            html.Hr(),
                            dbc.Row(
                                [
                                    #dbc.Button("Start", id="start-button", n_clicks=0, color="primary", className="mr-1"),
                                    #dbc.Button("Stop", id="stop-button", n_clicks=0, color="danger", className="mr-1"),
                                ],
                            ),
                        ],
                        width=6
                    ),
                ],
                style={'textAlign': 'center'},
            ),
        ],
        fluid=True,
    )

app.layout = create_app_layout

# Function to generate frames from webcam
def generate_frames():
    cap = cv2.VideoCapture(0)
    cap.release()
    cap = cv2.VideoCapture(0)
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5n.pt')
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        model_results = model(frame)
        df_detected = pd.DataFrame(columns=list(model_results.names.values()))
        ret, buffer = cv2.imencode('.jpg', model_results.render()[0])
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Flask route to serve webcam frames
@server.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Update the webcam image in real-time
@app.callback(Output('live-update-image', 'src'), [Input('start-button', 'n_clicks')], prevent_initial_call=True)
def update_image(n):
    print(n)
    return '/video_feed'

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)

