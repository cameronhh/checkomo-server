from globalspace.variables import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
import uuid

class Venue(db.Model,SerializerMixin):
    __tablename__ = 'venue'
    
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    address = db.Column(db.String(800))
    timezone = db.Column(db.String(64), nullable=False)

# schedules for making new codes
class VenueCodeTemplate(db.Model,SerializerMixin):
    __tablename__ = 'venue_code_template'
    id = db.Column(db.Integer(), primary_key=True)
    # TODO: make this table 

# codes created by a venue - i.e. checkomo/venue/code
class VenueCode(db.Model,SerializerMixin):
    __tablename__ = 'venue_code'
    #id's
    id = db.Column(db.String(64), primary_key=True, default=uuid.uuid4)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'),nullable=False)
    venue_code_template_id = db.Column(db.Integer, db.ForeignKey('venue_code_template.id'),nullable=True)
    # code
    code = db.Column(db.String(64), nullable=False)
    # code info
    name = db.Column(db.String(64))
    sys_name = db.Column(db.String(64))
    start_dttm = db.Column(db.DateTime())
    end_dttm = db.Column(db.DateTime())
    checkout_enabled = (db.Integer)



class Visit(db.Model,SerializerMixin):
    __tablename__ = 'visit'
    # id's
    clustered_id = db.Column(db.Integer(), primary_key=True) # this only exists for performance reasons
    id = db.Column(db.String(64), nullable=False, default=uuid.uuid4)
    # visit stuff
    in_dttm = db.Column(db.DateTime(),nullable=False)
    out_dttm = db.Column(db.DateTime())
    approved_in = db.Column(db.Boolean() )
    approved_out = db.Column(db.Boolean() )
    # venue code
    venue_code_id = db.Column(db.String(64), db.ForeignKey('venue_code.id'),nullable=True)
    # venue id - only used if created by venue
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'),nullable=True)
    # customer info
    given_name = db.Column(db.String(60), nullable=False)
    surname = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    # meta info
    meta_info = db.Column(db.String(1024)) # device info

#not needed yet
class User(db.Model,SerializerMixin):
    __tablename__ = 'user'
    # id
    id = db.Column(db.Integer(), primary_key=True)
    # details
    #username = db.Column(db.String(30), unique=True, nullable=False)
    contact_number = db.Column(db.String(30))
    email = db.Column(db.String(80), unique=True, nullable=False)
    # DO NOT INCLUDE THIS IN JSON SERIALIZATION (please)
    password = db.Column(db.String(200), nullable=False)

    token_register = db.Column(db.String(128))
    token_password_reset = db.Column(db.String(128))

    def to_dict(self):
        is_registered = True if self.token_register is None else False
        d = super.to_dict()
        del d["token_register"]
        del d["token_password_reset"]
        del d["password"]
        d["is_registered"] = is_registered
        return d
    

    @staticmethod
    def authedto_venue(user_id, venue_id):
        return bool( User.query.filter_by(id=user_id).join(VenueUser).join(Venue).filter(Venue.id == venue_id).first() )

class VenueUser(db.Model,SerializerMixin):
    __tablename__ = 'venue_user'
    venue_id = db.Column(db.Integer(), db.ForeignKey('venue.id'), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), primary_key=True)
    is_admin = db.Column(db.Boolean())

class Settings(db.Model,SerializerMixin):
    __tablename__ = 'settings'
    setting_key = db.Column(db.String(30), primary_key=True)
    setting_value = db.Column(db.String(2048), nullable=True)