# IMPORT LIBRARIES #####################################################################################################
import dash
from dash import dcc
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path='/guide',
    )

layout = dbc.Container(
    [
        # markdown
        dcc.Markdown('''
        # Guida
        
        https://www.engineeringtoolbox.com/co2-persons-d_691.html
        https://www.epa.gov/indoor-air-quality-iaq/what-average-level-carbon-monoxide-homes
        https://www.co2meter.com/blogs/news/carbon-monoxide-levels-chart
        https://www.certifico.com/costruzioni/379-documenti-costruzioni/documenti-riservati-costruzioni/13271-superficie-minima-abitazioni-normativa-e-requisiti
        https://www.grainger.com/product/BULLARD-Ambient-Air-Pump-10-cfm-3AM92
        '''),
    ],
)

# Pagina della guida in markdown