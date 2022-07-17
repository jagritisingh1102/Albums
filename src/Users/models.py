from ..utils.models import BaseMixin, ReprMixin
from ..utils.db import db


class Users(BaseMixin, ReprMixin, db.Model):
    name = db.Column(db.String(55), nullable=False)
    mobile_number = db.Column(db.String(55), nullable=True)
    email = db.Column(db.String(125), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=True)
    active = db.Column(db.Boolean(), nullable=False, default=False)
