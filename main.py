from flask import Flask
from flask_cors import CORS

# load vars (including app)
from globalspace.variables import app, db, config, api

# load model
import model.model

# load routes
import routes.master

cors = CORS(app)

if __name__ == "__main__":
    app.run(
        debug=config["use_debug"],
        use_reloader=True,
        port=config["app_port"],
        host=config["app_host"],
    )
