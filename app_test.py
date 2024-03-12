import numpy as np
from flask import Flask, Response
import dash
from dash import html
from dash.dependencies import Input, Output
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd

#from imaging import Imaging
from simulator import Simulator

import cv2
import torch

# css file for dash components
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# Initialize Flask app
server = Flask(__name__)

# Initialize Dash app
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.FLATLY, dbc_css])



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
        obj_detected = model_results.pandas().xyxy[0][["name"]].values
        count_person = np.count_nonzero(obj_detected == "person")
        Simulator.update_people(count_person)
        #df_detected = pd.DataFrame(columns=list(model_results.names.values()))
        ret, buffer = cv2.imencode('.jpg', model_results.render()[0])
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def create_app_layout():
    return dbc.Container(
        [
            dbc.NavbarSimple(
                id = "navbar",
                children=[
                    #dbc.NavItem(dbc.NavLink("Pagina iniziale", href="/", style={'font-size': '15px'})),
                    ## add space between images
                    #html.Div(style={'display': 'inline-block', 'width': '5px'}),
                    #html.Img(src='/static/icons', height="100px"),
                ],
                brand="Imaging based air Quality Controller Simulator",
                brand_href="#",
                color="primary",
                dark=True,
            ),
            html.Hr(),
            # Add dcc.interval to update the simulation
            dcc.Interval(
                id='interval-component',
                interval=1*1000, # in milliseconds
                n_intervals=0
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H5("Volume(m^3)"),
                            dbc.InputGroup(
                                [
                                    dbc.Button("-", id="input-volume_minus", n_clicks=0),
                                    dbc.Input(id="value-volume", placeholder="27", disabled=True, value=27), # 10 m^2
                                    dbc.Button("+", id="input-volume_plus", n_clicks=0),
                                ]
                            ),
                        ],
                        width=3
                    ),
                    dbc.Col(
                        [
                            html.H5("Pump capacity(L/min)"),
                            dbc.InputGroup(
                                [
                                    dbc.Button("-", id="input-pumpL_minus", n_clicks=0),
                                    dbc.Input(id="value-pumpL", placeholder="566", disabled=True, value=566),#566 = 10 cfm
                                    dbc.Button("+", id="input-pumpL_plus", n_clicks=0),
                                ]
                            ),
                        ],
                        width=3,
                    ),
                    dbc.Col(
                        [
                            html.H5("N pumps"),
                            dbc.InputGroup(
                                [
                                    dbc.Button("-", id="input-pumpN_minus", n_clicks=0),
                                    dbc.Input(id="value-pumpN", placeholder="4", disabled=True, value=4),
                                    dbc.Button("+", id="input-pumpN_plus", n_clicks=0),
                                ]
                            ),
                        ],
                        width=3,
                    ),
                    dbc.Col(
                        [
                            html.H6("CO threshold(mg/m^3)"),
                            dbc.InputGroup(
                                [
                                    dbc.Button("-", id="input-threshold_minus", n_clicks=0),
                                    dbc.Input(id="value-threshold", placeholder="0", disabled=True, value=5.725),
                                    dbc.Button("+", id="input-threshold_plus", n_clicks=0),
                                ]
                            ),
                        ],
                        width=3,
                    ),
                ],
                style={'textAlign': 'center'},
            ),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(html.H4(["People detected ",dbc.Badge("0", color="light", text_color="info", className="ms-1")])),
                    dbc.Col(html.H4(["Pump power ",dbc.Badge("0%", color="danger", className="me-1", id="pump-power")])),
                    dbc.Col(html.H4(["Anomaly score (variables) ", dbc.Badge("0", color="danger", className="me-1")])),
                    dbc.Col(html.H4(["Anomaly score (imaging) ", dbc.Badge("0", color="danger", className="me-1")])),
                ],
                id = "info-row",
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
                                    dbc.Col(dbc.Button("Stop", id="stop-button", n_clicks=0, color="secondary", className="mr-1"), width=6),
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
                            html.Hr(),
                            dbc.Row(
                                [
                                    dbc.Col(dbc.Button("Start Simulation", id="start-simulation-button", n_clicks=0, color="primary", className="mr-1")),
                                    dbc.Col(dbc.Button("Stop Simulation", id="stop-simulation-button", n_clicks=0, color="secondary", className="mr-1")),
                                    dbc.Col(dbc.Button("Simulate fault", id="fault-simulation-button", n_clicks=0, color="warning", className="mr-1")),
                                ],
                                id = "Badges_anomalies",
                            ),
                        ],
                        width=6,
                    ),
                ],
                style={'textAlign': 'center'},
            ),
        ],
        fluid=True,
    )

app.layout = create_app_layout

# Flask route to serve webcam frames
@server.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Update the webcam image in real-time
@app.callback(Output('live-update-image', 'src'), [Input('start-button', 'n_clicks')], prevent_initial_call=True)
def update_image(n):
    return '/video_feed'

# Run simulation
@app.callback(
        [
            Output('live-update-graph', 'figure'),
            Output('info-row', 'children'),
        ], 
        [
            Input('start-simulation-button', 'n_clicks'),
            Input('interval-component', 'n_intervals'),
        ], 
        prevent_initial_call=True)
def simulation_step(n_clicks, n):
    simulated_status = Simulator.simulate_time_step()
    info_row = [
        dbc.Col(html.H4(["People detected ",dbc.Badge(simulated_status["N_people"], color="light", text_color="info", className="ms-1")])),
        dbc.Col(html.H4(["Pump power ",dbc.Badge(simulated_status["Ambient-Air-Pump_power(%)"], color="danger", className="me-1", id="pump-power")])),
        dbc.Col(html.H4(["Anomaly score (variables) ", dbc.Badge("0", color="danger", className="me-1")])),
        dbc.Col(html.H4(["Anomaly score (imaging) ", dbc.Badge("0", color="danger", className="me-1")]))
    ]
    
    return dash.no_update, info_row

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)

'''
            # Create and style traces
            fig.add_trace(go.Scatter(x=df_sim.index, y=df_sim["CO(mg/m^3)_final"].values, name='CO(mg/m^3)',
                                     line=dict(color='green', width=4)))
            fig.add_trace(go.Scatter(x=[i for i in range(df_sim.index[-1],df_sim.index[-1]+11)], y=predictions, name='CO(mg/m^3) predicted',
                                     line=dict(color='blue', width=4,
                                          dash='dash')
            ))
            fig.add_trace(go.Scatter(x=[i for i in range(0,df_sim.index[-1]+10)], y=[simulator.threshold for i in range(0,df_sim.index[-1]+10)], name='Threshold(mg/m^3)',
                                     line=dict(color='firebrick', width=4,
                                          dash='dot')
            ))
            #fig = px.line(df_sim, x=df_sim.index, y="CO(mg/m^3)_final", title="CO(mg/m^3)", markers=True, template="plotly_white")
            fig.update_xaxes(title_text="Time(min)")
            fig.update_yaxes(title_text="CO(mg/m^3)")
            fig.update_layout(transition_duration=500)
            # change theme
            fig.update_layout(template="plotly_white")
'''