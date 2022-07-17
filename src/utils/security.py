import base64
import binascii
import hashlib
import hmac
import os
from datetime import timedelta
from src.Users import models, schemas
from flask_jwt_extended import create_access_token


class FlaskSecurity(object):

    def __init__(self, app=None, data_store=None):
        self.app = app
        self.data_store = data_store

        if app is not None and data_store is not None:
            self.init_app(app, data_store)

    def init_app(self, app, data_store=None):
        self.app = app
        if data_store:
            self.data_store = data_store
        return

    def get_user(self, email: str = None, mobile_number: str = None) -> str:
        if email:
            return self.data_store.query.with_entities(self.data_store.id) \
                .filter(self.data_store.email == email, self.data_store.active.isnot(False)) \
                .limit(1).scalar()
        else:
            return self.data_store.query.with_entities(self.data_store.id) \
                .filter(self.data_store.mobile_number == mobile_number, self.data_store.active.isnot(False)) \
                .limit(1).scalar()

    def check_password(self, auth_id, verify_password) -> bool:
        password = self.data_store.query.with_entities(self.data_store.password) \
            .filter(self.data_store.id == auth_id).limit(1).scalar()
        try:
            if len(base64.b64decode(password).hex()) == 128:
                return password == self.get_hmac(verify_password)
            else:
                raise binascii.Error
        except binascii.Error as e:
            print(e)
            new_password = self.get_hmac(password)
            self.data_store.query \
                .filter(self.data_store.id == auth_id).update({'password': new_password})
            models.db.session.commit()
            return password == verify_password

    def get_hmac(self, password):
        return base64.b64encode(hmac.new(os.environ.get('SECRET_KEY').encode('utf-8'), password.encode('utf-8'),
                                         hashlib.sha512).digest()).decode('ascii')

    def get_token(self, user_id):
        identity = schemas.UsersSchema().dump(self.data_store.query.get(user_id)).data

        user_claims = dict(USER={'READ': True, 'WRITE': True, 'UPDATE': True, 'DELETE': True},
                           IMAGE={'READ': True, 'WRITE': True, 'UPDATE': True, 'DELETE': True},
                           ARTIST={'READ': True, 'WRITE': True, 'UPDATE': True, 'DELETE': True},
                           ITEM={'READ': True, 'WRITE': True, 'UPDATE': True, 'DELETE': True},
                           TRACK={'READ': True, 'WRITE': True, 'UPDATE': True, 'DELETE': True},
                           ALBUM={'READ': True, 'WRITE': True, 'UPDATE': True, 'DELETE': True})

        return create_access_token(identity=identity, user_claims=user_claims,
                                   expires_delta=timedelta(days=1))


security_v = FlaskSecurity(data_store=models.Users)
