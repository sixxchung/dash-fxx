from app_dash import dash_app
#import routes
import os
import environment.settings 
#from environment.settings import APP_HOST, APP_PORT, APP_DEBUG, DEV_TOOLS_PROPS_CHECK
# =============================================================================
# Run app 
# =============================================================================
# if __name__ == '__main__':
#     app.run_server(debug=True)

if __name__ == "__main__":
    dash_app.run_server(
        host=os.environ.get("HOST"),
        port=int(os.environ.get("PORT")),
        debug=bool(os.environ.get("DEBUG")),
        dev_tools_props_check = bool(os.environ.get("DEV_TOOLS_PROPS_CHECK"))
    )

