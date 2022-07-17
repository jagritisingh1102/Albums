from ..utils.schema import BaseSchema, ma
from .models import Users


class UsersSchema(BaseSchema):
    class Meta:
        model = Users

    name = ma.String(allow_none=False)
    active = ma.Boolean(allow_none=False)
