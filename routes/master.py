from globalspace.variables import api, app

from api_resources.visit import Visit
from api_resources.venue import Venue
from api_resources.venue_code import VenueCode
from api_resources.token import Token
from api_resources.user import User

api.add_resource(User, "/user", "/user/<int:user_id>")

api.add_resource(
    Visit,
    "/visit",
    "/visit/<string:visit_id>",
    "/venue/<int:venue_id>/visit",
    "/venue/<int:venue_id>/venuecode/<string:venue_code_id>/visit",
)

api.add_resource(Venue, "/venue/<int:venue_id>", "/user/<int:user_id>/venue", "/venue")

api.add_resource(
    VenueCode,
    "/venue/<int:venue_id>/venuecode",
    "/venue/<int:venue_id>/venuecode/<string:venue_code_id>",
    "/venuecode/<string:venue_code_id>",
)

api.add_resource(Token, "/token")
