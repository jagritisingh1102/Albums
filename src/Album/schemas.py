from ..utils.schema import BaseSchema, ma
from .models import Images, Artists, Items, Tracks, Albums
from marshmallow import validate


class ImagesSchema(BaseSchema):
    class Meta:
        model = Images
        include_relationships = True
        load_instance = True

    url = ma.String(allow_none=True, validate=validate.Length(max=125))
    width = ma.String(allow_none=True)
    height = ma.String(allow_none=True)


class ArtistsSchema(BaseSchema):
    class Meta:
        model = Artists
        include_relationships = True
        load_instance = True

    name = ma.String(allow_none=False)
    href = ma.String(allow_none=False)
    type = ma.String(allow_none=False)
    url = ma.String(allow_none=True)
    image_id = ma.UUID(allow_none=True)
    images = ma.Nested('ImagesSchema', allow_none=True)
    popularity = ma.Integer(allow_none=True)


class ItemsSchema(BaseSchema):
    class Meta:
        model = Items
        include_relationships = True
        load_instance = True

    name = ma.String(allow_none=False)
    href = ma.String(allow_none=False)


class TracksSchema(BaseSchema):
    class Meta:
        model = Tracks
        include_relationships = True
        load_instance = True

    limit = ma.Integer(allow_none=False)
    offset = ma.Integer(allow_none=False)
    total = ma.Integer(allow_none=False)
    previous = ma.String(allow_none=True)
    next = ma.String(allow_none=True)
    href = ma.String(allow_none=True)
    width = ma.String(allow_none=True)
    height = ma.String(allow_none=True)
    album_id = ma.UUID(allow_none=False)
    albums = ma.Nested('AlbumsSchema', dump_only=True)


class AlbumsSchema(BaseSchema):
    class Meta:
        model = Albums
        include_relationships = True
        load_instance = True

    album_type = ma.String(allow_none=False)
    name = ma.String(allow_none=False)
    release_date = ma.DateTime(allow_none=False)
    url = ma.String(allow_none=True)
    type = ma.String(allow_none=True)
    href = ma.String(allow_none=True)
    available_markets = ma.Dict(allow_none=True)
    image_id = ma.UUID(allow_none=True)
    images = ma.Nested('ImagesSchema', allow_none=True)
    artist_id = ma.UUID(allow_none=True)
    artists = ma.Nested('ArtistsSchema', allow_none=True)
