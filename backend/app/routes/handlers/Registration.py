from app import db
from app.models import UserCredential
from werkzeug.security import generate_password_hash
from flask_api import status

class Registration:
    def register_user(self, registration_form):
        credential_details = registration_form.get('credentials')
        registration_username = credential_details.get('username')
        if not self.is_username_valid(registration_username):
            return status.HTTP_406_NOT_ACCEPTABLE
        if not self.is_username_existing(registration_username):
            return status.HTTP_409_CONFLICT

        user_credential = self.create_new_user_credential(credential_details)
        commitSuccessFlag = self.commit_new_user(user_credential)
        return status.HTTP_201_CREATED if commitSuccessFlag else status.HTTP_500_INTERNAL_SERVER_ERROR

    def is_username_valid(self, registration_username):
        if registration_username == "" or registration_username is None:
            return False
        if (registration_username[0].isdigit()):
            return False
        for username_char in registration_username:
            if not (username_char.isalnum() or username_char == '_'):
                return False
        return True

    def is_username_existing(self, register_username):
        existing_username = UserCredential.query.filter_by(username=register_username).first()
        return True if existing_username is None else False
    
    def create_new_user_credential(self, credential_details):
        register_username = credential_details.get('username').lower()
        register_password = generate_password_hash(credential_details.get('password'))
        return UserCredential(username=register_username, password=register_password)

    def commit_new_user(self, user_credential):
        db.session.add(user_credential)
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            return False
