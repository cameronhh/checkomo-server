from flask import Flask, jsonify, request, abort
from globalspace.variables import app,config,api,db
import model.model as model
from flask_restplus import Resource

from util.crypt import check_password

import jwt
_secret = app.config.get('SECRET_KEY')

class Token(Resource):

    def post(self):
        data = request.get_json(force=True)
        this_user = model.User.query.filter_by(email=data.get("email")).first()
        # abort if not valid user
        if this_user is None: abort(403)
        # abort if password wrong/None
        if not check_password(data.get("password"), this_user.password): abort(403)
        # remove password hash from
        dict_user = this_user.to_dict()
        del dict_user['password']
        
        token_dict = {
            "user_id" : dict_user['id'],
            "user" : dict_user
            #expirery and other shit
        }

        token = jwt.encode(token_dict, _secret, algorithm='HS256').decode('utf-8')

        return jsonify({"token":token})
