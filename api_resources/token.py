from flask import Flask, jsonify, request, abort
from globalspace.variables import app, config, api, db
import model.model as model
from flask_restplus import Resource
import datetime

from util.crypt import check_password, validate_token

import jwt

_secret = app.config.get("SECRET_KEY")


class Token(Resource):
    def post(self):

        auth_to_user_id = validate_token(validate_only=True)
        # if the user isn't getting a new token
        if not auth_to_user_id:
            data = request.get_json(force=True)
            this_user = model.User.query.filter_by(email=data.get("email")).first()
            # abort if not valid user
            if this_user is None:
                abort(403)
            # abort if password wrong/None
            if not check_password(data.get("password"), this_user.password):
                abort(403)
            # remove password hash from
            dict_user = this_user.to_dict()
            del dict_user["password"]
            auth_to_user_id = dict_user["id"]
        else:
            validate_token()  # so we can abort properly

        token_dict = {
            "user_id": auth_to_user_id,
            # TODO propper expirery
            "valid_to_dttm": str(datetime.datetime.now() + datetime.timedelta(days=14))
            # expirery and other shit
        }

        token = jwt.encode(token_dict, _secret, algorithm="HS256").decode("utf-8")

        return jsonify({"token": token})
