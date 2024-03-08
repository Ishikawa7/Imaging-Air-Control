import dash
from dash import Dash, Input, Output, State, callback, html, dcc
import dash_bootstrap_components as dbc
import os

# css file for dash components
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# DASH APP #############################################################################################################
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.LUX, dbc_css]) #suppress_callback_exceptions=True

def create_app_layout():
    return dbc.Container(
        [
            dbc.NavbarSimple(
                id = "navbar",
                children=[
                    #dbc.NavItem(dbc.NavLink("Pagina iniziale", href="/", style={'font-size': '15px'})),
                    dbc.NavItem(dbc.NavLink("Guide", href="/guide", style={'font-size': '15px'})),
                    #html.Img(src='/static/icons/Logo_COR.png', height="100px"),
                    ## add space between images
                    #html.Div(style={'display': 'inline-block', 'width': '5px'}),
                    #html.Img(src='/static/icons/Logo_semeion.png', height="100px"),
                    #html.Div(style={'display': 'inline-block', 'width': '5px'}),
                    #html.Img(src='/static/icons/Logo_semeiontech.png', height="100px"),
                ],
                brand="Air Quality Controller Simulator",
                brand_href="#",
                color="primary",
                dark=True,
            ),
            html.Hr(),
            # temp for showing all pages
            #html.Div(
            #    [
            #        dbc.Button(
            #            "Pagine",
            #            id="collapse-button-nav",
            #            className="mb-3",
            #            color="primary",
            #            n_clicks=0,
            #        ),
            #        dbc.Collapse(
            #            html.Div([
            #                html.Div(
            #                    dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
            #                ) for page in dash.page_registry.values()
            #            ]),
            #            id="collapse-nav",
            #        ),
            #    ]
            #),
            #########################
    	    dash.page_container,
            # add a footer
            html.Hr(),
            # use a jumbotron to add a description for the app
            #html.Div(
            #    dbc.Container(
            #        [
            #            html.H3("Info"),
            #            html.P(
            #                "Simulator",
            #                className="lead",
            #            ),
            #            html.Hr(className="my-2"),
            #            html.P(
            #                "For more information, please visit the guide page."
            #            ),
            #            html.P(
            #                dbc.Button("Guida", color="primary", href='/guide'), className="lead"
            #            ),
            #        ],
            #        fluid=True,
            #        className="py-3",
            #    ),
            #    className="p-3 bg-light rounded-3",
            #)
        ],
        fluid=True,
    )

app.layout = create_app_layout

#CALLBACKS #######################################################################################################

#@app.callback(
#    Output("collapse-nav", "is_open"),
#    [Input("collapse-button-nav", "n_clicks")],
#    [State("collapse-nav", "is_open")],
#    prevent_initial_call=True
#)
#def toggle_collapse(n, is_open):
#    if n:
#        return not is_open
#    return is_open
# RUN THE APP ###########################################################################################################
if __name__ == "__main__":
    # shut down any running dash processes
    #os.system("taskkill /f /im python.exe")
    # start the dash app
    #app.run_server(host='0.0.0.0', port=8080, debug=False, use_reloader=False)
    app.run_server(debug=True, use_reloader=True)

# if Python [Errno 98] Address already in use 
# kill -9 $(ps -A | grep python | awk '{print $1}')