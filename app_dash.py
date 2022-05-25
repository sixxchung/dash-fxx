import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_admin_components as dac
import flask
# from flask_caching import Cache

from utils.external_assets import ROOT, EXTERNAL_STYLESHEETS, FONT_AWSOME
from layout_ui.main_content import layout


# =============================================================================
# Dash App and Flask Server
# =============================================================================
server = flask.Flask(__name__)

dash_app = dash.Dash(
    name= __name__,
    server=server,
    routes_pathname_prefix='/dash/',
    requests_pathname_prefix="/dash/",
    assets_folder = ROOT+"/assets/", 

    suppress_callback_exceptions=True, 
    external_stylesheets=[
        dbc.themes.CYBORG, 
        FONT_AWSOME,
        #EXTERNAL_STYLESHEETS
    ],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)

#app.css.config.serve_locally = True
#app.scripts.config.serve_locally = True
#app.scripts.config.serve_locally = False

#dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'
#                                  'https://unpkg.com/dash-core-components@2.0.0/dash_core_components/async-datepicker.js'

# cfg = {
#     'DEBUG' : True,
#     'CACHE_TYPE': 'filesystem',
#     'CACHE_DIR': 'cache-directory',
#     'CACHE_DEFAULT_TIMEOUT': 666
# }
# cache = Cache(app.server, config=cfg)

#server = app.server 

# =============================================================================
# Dash Admin Components
# =============================================================================
dash_app.layout = layout

