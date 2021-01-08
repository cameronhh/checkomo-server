from flask import Flask, jsonify, request, abort
from globalspace.variables import app, config, api, db
import model.model as model
from flask_restplus import Resource
from util.crypt import validate_token, make_hashed_password


class User(Resource):
    def get(self, user_id=None):
        auth_user_id = validate_token()
        if auth_user_id != user_id:
            abort(400)
        this_user = model.User.query.get(auth_user_id)
        if this_user is None:
            abort(404)
        this_user_dict = this_user.to_dict()
        del this_user_dict["password"]
        return jsonify(this_user_dict)

    # register
    def post(self):
        data = request.get_json(force=True)

        contact_number = data.get("contact_number")
        email = data.get("email")
        address = data.get("address")
        # username = data.get("username")
        unhashed_password = data.get("password")

        if unhashed_password is None:
            abort(400)
        password = make_hashed_password(unhashed_password)

        this_user = model.User(
            contact_number=contact_number,
            email=email,
            # username = username,
            password=password,
        )

        db.session.add(this_user)
        db.session.commit()
        user_dict = this_user.to_dict()
        del user_dict["password"]
        return jsonify(user_dict)

    def put(self):
        data = request.get_json(force=True)