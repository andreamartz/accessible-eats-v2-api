from flask import (Flask, jsonify, request, session)
from model import connect_to_db, db
import os
import werkzeug.security
import crud
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


@app.route('/login', methods=['POST'])
def login():
    """Login a user.

    Checks for a user with the submitted username.
        - if none is found, returns jsonified dictionary:
            {
                "user": None,
                "success": False,
                "message": "No user exists with that username.",
            }
        - if one is found, the submitted password is checked against the 
            database
            - if the password is correct, returns the jsonified user:
                {
                    "user": <the user object>,
                    "success": True,
                    "message": "",
                }
            - if password is incorrect, 
        - multiple users should not be found, because this is prevented at 
            user sign up

    Args: none

    Data payload should be a dictionary with username and password keys.
    """

    result = {
        "user": None,
        "success": False,
        "message": "",
    }

    login_data = request.get_json()
    username, password = list(login_data.values())

    count = crud.count_users_by_username(username)

        # if no users found
    if count == 0:
        result["message"] = "No user exists with that username."
        return jsonify(result)

    # if one user found
    user = crud.get_user_by_username(username)

        # if password does NOT match
    if werkzeug.security.check_password_hash(user.password, password) == False:
        result["message"] = 'Username or password is incorrect. Please try again.'
        return jsonify(result)

    # if password does match
    session["current_user_id"] = user.id
    result["user"] = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
    }
    result["success"] = True
    result["message"] = 'Success! You\'re now logged in.'

    return jsonify(result)



if __name__ == "__main__":
    # connect to the database before app.run gets called
    # if you don't do this, Flask won't be able to access your database
    connect_to_db(app)
    # TODO: Remove app.debug line and app.run(host="...) below in production
    # app.debug = True
    # app.run(host="0.0.0.0", debug=True)
    app.run()