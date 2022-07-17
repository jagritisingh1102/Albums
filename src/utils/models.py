from .db import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text


class BaseMixin(object):
    __mapper_args__ = {'always_refresh': True}
    id = db.Column(UUID(as_uuid=True), index=True, primary_key=True, server_default=text("uuid_generate_v4()"))
    created_on = db.Column(db.TIMESTAMP(timezone=True), server_default=text("current_timestamp"), index=True)
    updated_on = db.Column(db.TIMESTAMP(timezone=True), onupdate=db.func.current_timestamp(),
                           server_default=text("current_timestamp"))


class ReprMixin(object):
    """Provides a string representible form for objects."""

    __repr_fields__ = ['id', 'name']

    def __repr__(self):
        fields = {f: getattr(self, f, '<BLANK>') for f in self.__repr_fields__}
        pattern = ['{0}={{{0}}}'.format(f) for f in self.__repr_fields__]
        pattern = ' '.join(pattern)
        pattern = pattern.format(**fields)
        return '<{} {}>'.format(self.__class__.__name__, pattern)
