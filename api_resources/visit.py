from flask import Flask, jsonify, request, abort
from globalspace.variables import app,config,api,db
import model.model as model
from flask_restplus import Resource
from util.crypt import validate_token
from datetime import datetime
import dateutil.parser


class Visit(Resource):

    def get(self, visit_id=None, venue_id=None, venue_code_id=None):
        if visit_id and not venue_id:
            visit = model.Visit.query.filter_by(id=visit_id).first().to_dict()
        # protected endpoints
        else:
            user_id = validate_token()
            if not model.User.authedto_venue(user_id, venue_id): abort(401)
            # get search params
            in_dttm_min = request.args.get("in_dttm_min") or None
            in_dttm_max = request.args.get("in_dttm_max") or None
            clustered_id_min = request.args.get("clustered_id_min") or None
            max_records = request.args.get("max_records") or None

            # visit can be linked via venue code or directly to venue
            # thomas had never seen such a mess
            q_by_venue_code = model.Visit.query.join(model.VenueCode).join(model.Venue).filter(model.Venue.id==venue_id)
            q_by_venue_id = model.Visit.query.join(model.Venue).filter(model.Venue.id==venue_id)
            q = q_by_venue_code.union(q_by_venue_id)
            if venue_code_id:
                q = q.filter(model.VenueCode.id == venue_code_id)
            if in_dttm_min:
                in_dttm_min = dateutil.parser.parse(in_dttm_min)
                q = q.filter(model.Visit.in_dttm > in_dttm_min)
            if in_dttm_max:
                in_dttm_max = dateutil.parser.parse(in_dttm_max)
                q = q.filter(model.Visit.in_dttm < in_dttm_max)
            if clustered_id_min:
                q = q.filter(model.Visit.clustered_id > clustered_id_min)
            
            q = q.order_by(model.Visit.clustered_id.desc())

            # limit records
            if max_records:
                visit = q.limit(int(max_records))
            else:
                visit = q.all()
            visit = [r.to_dict() for r in visit]

        if visit is None: abort(404)
        return jsonify(visit)

    def post(self, venue_id=None, venue_code=None, venue_code_id=None):
        data = request.get_json(force=True)
        venue_code = request.args.get("venue_code")
        venue_code_id = venue_code_id or data.get("venue_code_id") or \
            model.VenueCode.query.filter_by(code=venue_code,venue_id=venue_id).first() # not restful :(

        in_dttm = dateutil.parser.parse(data["in_dttm"]) #datetime.strptime(data["in_dttm"],'%Y-%m-%d %H:%M:%S.%f')
        out_dttm = None if data.get("out_dttm") is None else dateutil.parser.parse(data["out_dttm"])
        meta_info = data.get("meta_info")
        given_name = data.get("given_name")
        surname = data.get("surname")
        phone = data.get("phone")
        email = data.get("email")
        address = data.get("address")

        this_venue_code = model.VenueCode.query.get(venue_code_id)
        if (this_venue_code.start_dttm is not None and  datetime.now() < this_venue_code.start_dttm):
            abort(400, "venue_code_too_new")
        elif (this_venue_code.end_dttm is not None and  datetime.now() > this_venue_code.end_dttm):
            abort(400, "venue_code_too_old")

        # only
        if venue_code_id is None:
            user_id = validate_token()
            if venue_id is None: abort(400)
            if user_id is None: abort(401)
            if not model.User.authedto_venue(user_id,venue_id): abort(401)

        this_visit = model.Visit(
            in_dttm = in_dttm,
            out_dttm = out_dttm,
            venue_code_id = venue_code_id,
            venue_id = venue_id, # only used if business creates visit
            meta_info = meta_info,
            given_name = given_name,
            surname = surname,
            phone = phone,
            email = email,
            address = address
        )
        db.session.add(this_visit)
        db.session.commit()
        
        return jsonify(this_visit.to_dict())

    # TODO
    def put(self, visit_id=None):
        #this_visit = model.Visit.query.filter_by(id=visit_id)
        #if this_visit is None: abort(404)
        ## let anyone add an out_dttm, only a business can change other details
        #user_id = validate_token()
        #data = request.get_json(force=True)
        ## make sure user is authed to change details
        #if this_visit.venue_id is None:
        #    venue_id = this_visit.venue_id
        #else:
        #    venue_id = model.Visit.query.filter_by(visit_id=this_visit.id).join(model.VenueCode).join(model.Venue).first().id
        #if not model.User.authedto_venue(user_id,venue_id): abort(401)
#
        #this_visit.
#
        return jsonify(this_visit.to_dict())