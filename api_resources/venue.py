from flask import Flask, jsonify, request, abort
from globalspace.variables import app,config,api,db
import model.model as model
from flask_restplus import Resource
from util.crypt import validate_token

class Venue(Resource):
    def get(self, venue_id=None, user_id=None):
        #abort(403)
        user_id = validate_token()

        # get single venue
        if venue_id and not user_id:
            venue = model.Venue.query.get(venue_id).to_dict()
        # get all vanues for a user
        if user_id and not venue_id:
            venue = model.Venue.query.join(model.VenueUser).join(model.User).filter(model.User.id == user_id).all()
            venue = [r.to_dict() for r in venue]
        
        if venue is None: abort(404)
        return jsonify(venue)

    def post(self):
        #abort(403)
        user_id = validate_token()
        if user_id is None: abort(401)
        data = request.get_json(force=True)

        name = data.get("name")
        address = data.get("address")
        timezone = data.get("timezone")

        this_venue = model.Venue(
            name = name,
            address = address,
            timezone = timezone
        )
        db.session.add(this_venue)
        db.session.flush()
        db.session.refresh(this_venue)

        this_venue_user = model.VenueUser(
            venue_id = this_venue.id,
            user_id = user_id,
            is_admin = True
        )
        db.session.add(this_venue_user)

        db.session.commit()

        return jsonify(this_venue.to_dict())