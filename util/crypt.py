# don't fuck with this file too much
from globalspace.variables import app
_secret = app.config.get('SECRET_KEY')

import bcrypt

# when a user creates their password, use this to create their stored salted hash
def make_hashed_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt(8)).decode('utf-8')

# use this to check an incoming password against a user's hashed password
def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))


from flask import request
import jwt

# validate a token and return user id or None
def validate_token():
    if request.headers.get('Authorization') is None: return None
    token_str = request.headers.get('Authorization').split(" ")[1]
    try:
        decoded_token = jwt.decode(token_str.encode('utf-8'), _secret, algorithms=['HS256'])
    except jwt.exceptions.InvalidSignatureError:
        # invalid signature
        return None
    #this_user = model.User.query.get()
    return decoded_token.get('user_id')