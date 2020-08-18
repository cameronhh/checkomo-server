from flask import Flask, jsonify, request, abort
from globalspace.variables import app,config,api,db
import model.model as model
from flask_restplus import Resource
from util.crypt import validate_token
import dateutil.parser

class VenueCode(Resource):

    def post(self, venue_id):
        user_id = validate_token()
        data = request.get_json(force=True)

        if model.Venue.query.get(venue_id) is None: abort(404)
        if not model.User.authedto_venue(user_id,venue_id): abort(403)

        venue_code_template_id = None # this should only be set if created from a template, NI yet
        code = data.get("code")
        name = data.get("name")
        # sys_name = data.get("sys_name")
        start_dttm = data.get("start_dttm")
        start_dttm = dateutil.parser.parse(start_dttm) if start_dttm is not None else None
        end_dttm = data.get("end_dttm")
        end_dttm = dateutil.parser.parse(end_dttm) if end_dttm is not None else None

        checkout_enabled = data.get("checkout_enabled")

        this_venue_code = model.VenueCode(
            venue_id = venue_id,
            venue_code_template_id = venue_code_template_id,
            code = code,
            name = name,
            start_dttm = start_dttm,
            end_dttm = end_dttm,
            checkout_enabled = checkout_enabled
        )    
        db.session.add(this_venue_code)
        db.session.commit()

        return jsonify(this_venue_code.to_dict())

    def get(self, venue_code_id=None, venue_id=None):
        vencode=None
        q = model.VenueCode.query
        if venue_code_id is not None:
            vencode = q.get(venue_code_id).to_dict()
        elif request.args.get("code"):
            q = q.filter_by(code=request.args.get("code"), venue_id=venue_id)
            vencode = q.first().to_dict()
        # protected conditions
        elif venue_id and not venue_code_id:
            user_id = validate_token()
            # if user is authed to venue id
            vencode = q.filter_by(venue_id=venue_id)
            vencode = [r.to_dict() for r in vencode]
        
        # final return
        if vencode is None: abort(404)
        return jsonify(vencode)

    def put(self, venue_code_id=None, **kwargs):
        user_id = validate_token()
        data = request.get_json(force=True)
        this_venue_code = model.VenueCode.query.get(venue_code_id)
        if not model.User.authedto_venue(user_id, this_venue_code.venue_id): return 401

        name = data.get("name")
        start_dttm = data.get("start_dttm")
        start_dttm = dateutil.parser.parse(start_dttm) if start_dttm is not None else None
        end_dttm = data.get("end_dttm")
        end_dttm = dateutil.parser.parse(end_dttm) if end_dttm is not None else None
        checkout_enabled = data.get("checkout_enabled")

        this_venue_code.name = name
        this_venue_code.start_dttm = start_dttm
        this_venue_code.end_dttm = end_dttm
        this_venue_code.checkout_enabled = checkout_enabled

        db.session.commit()
        return jsonify(this_venue_code.to_dict())
        
