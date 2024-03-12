import numpy as np
from flask import Flask, Response
import dash
from dash import html
from dash.dependencies import Input, Output
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from imaging import Imaging
from simulator import Simulator
from anomalies_img import FrameAnomalyDetector
from anomalies_var import VariablesAnomalyDetector

# css file for dash components
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# Initialize Flask app
server = Flask(__name__)

# Initialize Dash app
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.FLATLY, dbc_css])

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
                interval=1*3000, # in milliseconds
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
                            html.H4("Webcam Video Stream"),
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
                            html.H4("Simulation CO Stream"),
                            dcc.Graph(
                                id='live-update-graph-sim',
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

            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Graph(
                                id='live-update-graph-an-imaging',
                                style={'width': '100%', 'height': 'auto'}
                            ),
                            html.H4("Anomaly score (imaging)"),
                        ],
                        width=6,
                    ),
                    dbc.Col(
                        [
                            dcc.Graph(
                                id='live-update-graph-an-variables',
                                style={'width': '100%', 'height': 'auto'}
                            ),
                            html.H4("Anomaly score (variables)"),
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
    Imaging.initialize()
    return Response(Imaging.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Update the webcam image in real-time
@app.callback(Output('live-update-image', 'src'), [Input('start-button', 'n_clicks')], prevent_initial_call=True)
def update_image(n):
    return '/video_feed'

# Run simulation
@app.callback(
        [
            Output('live-update-graph-sim', 'figure'),
            Output("live-update-graph-an-imaging", "figure"),
            Output("live-update-graph-an-variables", "figure"),
            Output('info-row', 'children'),
        ], 
        [
            Input('start-simulation-button', 'n_clicks'),
            Input('interval-component', 'n_intervals'),
        ], 
        prevent_initial_call=True)

def simulation_step(n_clicks, n):
    Simulator.simulate_time_step()
    sim_status = Simulator.status_dict
    sim_predictions = Simulator.predictions
    sim_log_CO = Simulator.CO_log
    an_imaging = FrameAnomalyDetector.get_frame_anomaly()
    an_imaging_log = FrameAnomalyDetector.an_log
    an_variables = VariablesAnomalyDetector.get_variables_anomaly(sim_status)
    an_variables_log = VariablesAnomalyDetector.an_log

    fig_an_imaging = px.line(x=[i for i in range(len(an_imaging_log))], y=an_imaging_log, markers=True, template="plotly_white")
    fig_an_imaging.update_traces(line=dict(color='black', width=3))
    fig_an_imaging.update_layout(transition_duration=100)

    fig_an_variables = px.line(x=[i for i in range(len(an_variables_log))], y=an_variables_log, markers=True, template="plotly_white")
    fig_an_variables.update_traces(line=dict(color='black', width=3))
    fig_an_variables.update_layout(transition_duration=100)

    fig_simulation = go.Figure()
    fig_simulation.add_trace(go.Scatter(x=[i for i in range(len(sim_log_CO))], y=sim_log_CO, name='CO(mg/m^3)', line=dict(color='green', width=4)))
    fig_simulation.add_trace(go.Scatter(x=[i for i in range(len(sim_log_CO)-1,len(sim_log_CO)+10-1)], y=sim_predictions, name='CO(mg/m^3) predicted', line=dict(color='blue', width=4, dash='dash')))
    fig_simulation.update_layout(transition_duration=100)
    fig_simulation.update_layout(template="plotly_white")
    info_row = [
        dbc.Col(html.H4(["People detected ",dbc.Badge(sim_status["N_people"], color="light", text_color="info", className="ms-1")])),
        dbc.Col(html.H4(["Pump power ",dbc.Badge(sim_status["Ambient-Air-Pump_power(%)"], color="danger", className="me-1", id="pump-power")])),
        dbc.Col(html.H4(["Anomaly score (variables) ", dbc.Badge(an_variables, color="danger", className="me-1")])),
        dbc.Col(html.H4(["Anomaly score (imaging) ", dbc.Badge(an_imaging, color="danger", className="me-1")]))
    ]
    
    return fig_simulation, fig_an_imaging, fig_an_variables, info_row

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)