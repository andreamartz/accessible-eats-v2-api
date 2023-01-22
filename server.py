from flask import (Flask, jsonify, request, session)
from model import connect_to_db, db
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# the secret key is needed for flash and session to work
app.secret_key = "dev"

# TODO: remove in production
# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True

# ********************************
# User Routes
# ********************************




if __name__ == "__main__":
    # connect to the database before app.run gets called
    # if you don't do this, Flask won't be able to access your database
    connect_to_db(app)
    # TODO: Remove app.debug line and app.run(host="...) below in production
    # app.debug = True
    # app.run(host="0.0.0.0", debug=True)
    app.run()