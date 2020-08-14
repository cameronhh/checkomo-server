from globalspace.variables import api, app

from api_resources.visit import Visit
from api_resources.venue import Venue
from api_resources.venue_code import VenueCode
from api_resources.token import Token
from api_resources.user import User

api.add_resource(User,
    '/api/user',
    '/api/user/<int:user_id>'
)

api.add_resource(Visit,
    '/api/use',
    '/api/visit/<string:visit_id>',
    '/api/venue/<int:venue_id>/visit',
    '/api/venue/<int:venue_id>/venuecode/<string:venue_code_id>/visit'
)

api.add_resource(Venue,
    '/api/venue/<int:venue_id>',
    '/api/user/<int:user_id>/venue',
    '/api/venue'
)

api.add_resource(VenueCode,
    '/api/venue/<int:venue_id>/venuecode',
    '/api/venue/<int:venue_id>/venuecode/<string:venue_code_id>',
    '/api/venuecode/<string:venue_code_id>'
)

api.add_resource(Token,
    '/api/token'
)
