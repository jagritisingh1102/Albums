from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import UniqueConstraint
from ..utils.db import db
from ..utils.models import BaseMixin, ReprMixin


class Images(BaseMixin, ReprMixin, db.Model):
    url = db.Column(db.String(256), nullable=True)
    width = db.Column(db.String(25), nullable=True)
    height = db.Column(db.String(25), nullable=True)


class Artists(BaseMixin, ReprMixin, db.Model):
    name = db.Column(db.String(256), nullable=False)
    href = db.Column(db.String(25), nullable=False)
    type = db.Column(db.String(25), nullable=False)
    image_id = db.Column(db.ForeignKey('images.id', ondelete='CASCADE'))
    images = db.relationship('Images', foreign_keys=[image_id])
    url = db.Column(db.String(256), nullable=True)
    popularity = db.Column(db.Integer(), default=1, nullable=True)
    UniqueConstraint(name, type)


class Items(BaseMixin, ReprMixin, db.Model):
    name = db.Column(db.String(256), nullable=True, unique=True)
    href = db.Column(db.String(25), nullable=True)


class Tracks(BaseMixin, ReprMixin, db.Model):
    limit = db.Column(db.Integer(), default=1, nullable=False)
    offset = db.Column(db.Integer(), default=1, nullable=False)
    total = db.Column(db.Integer(), default=1, nullable=False)
    previous = db.Column(db.String(256), nullable=True)
    href = db.Column(db.String(256), nullable=True)
    next = db.Column(db.String(256), nullable=True)
    width = db.Column(db.String(25), nullable=True)
    height = db.Column(db.String(25), nullable=True)
    album_id = db.Column(db.ForeignKey('albums.id'))
    albums = db.relationship('Albums', foreign_keys=[album_id])


class Albums(BaseMixin, ReprMixin, db.Model):
    album_type = db.Column(db.String(25), nullable=True)
    name = db.Column(db.String(256), nullable=True)
    release_date = db.Column(db.TIMESTAMP(timezone=True), nullable=True)
    url = db.Column(db.String(256), nullable=True)
    type = db.Column(db.String(256), nullable=True)
    href = db.Column(db.String(256), nullable=True)
    available_markets = db.Column(JSON(), default=[])
    image_id = db.Column(db.ForeignKey('images.id', ondelete='CASCADE'))
    images = db.relationship('Images', foreign_keys=[image_id])
    artist_id = db.Column(db.ForeignKey('artists.id', ondelete='CASCADE'))
    artists = db.relationship('Artists', foreign_keys=[artist_id])
    UniqueConstraint(album_type, name, type)
