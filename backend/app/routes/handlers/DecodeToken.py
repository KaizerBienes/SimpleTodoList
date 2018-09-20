import jwt
import re
import os
import logging

def get_user_id(request_headers):
    user_token = extract_token(request_headers)
    if user_token is None:
        return None
    else:
        return get_user_id_from_token(user_token)

def extract_token(request_headers):
    if 'Authorization' in request_headers:
        token_parts = request_headers.get('Authorization').split(' ', 1)
        if (re.match('^Bearer$', token_parts[0]) is not None):
            return token_parts[1]
        else:
            return None;

def get_user_id_from_token(token):
    try:
        jwt_contents = jwt.decode(token, os.environ.get('SECRET_CODE'), algorithm='HS256')
        return jwt_contents.get('id', None)
    except (jwt.InvalidSignatureError, jwt.ExpiredSignatureError,\
        jwt.InvalidTokenError, jwt.DecodeError) as e:
        logging.warn(e)
        return None
