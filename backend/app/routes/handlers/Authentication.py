from app import db
from app.models import UserCredential
from werkzeug.security import check_password_hash
from flask_api import status
import logging
import os
import jwt
import datetime

class Authentication:
    def login(self, login_form):
        login_details = login_form.get('credentials')
        user_found = UserCredential.query.filter_by(username=login_details.get('username')).first()
        if not self.is_username_existing(user_found):
            return self.construct_authentication_dict(status.HTTP_404_NOT_FOUND, {})
        else:
            if self.is_password_valid(user_found, login_details.get('password')):
                return self.construct_authentication_dict(status.HTTP_202_ACCEPTED, {
                    "token":  jwt.encode(self.construct_jwt(user_found.id),\
                        os.environ.get('SECRET_CODE'), algorithm='HS256')     
                })
            else:
                return self.construct_authentication_dict(status.HTTP_401_UNAUTHORIZED, {})
    
    def construct_jwt(self, user_id):
        return {
            'id': user_id,
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
        }


    def construct_authentication_dict(self, http_code, data={}):
        return {
            "http_code": http_code,
            "data": data
        }


    def is_username_existing(self, user_found):
        return True if user_found else False

    def is_password_valid(self, user_found, login_password):
        user_password = user_found.password
        if user_password is not None \
            and check_password_hash(user_password, login_password):
            return True
        else:
            return False

