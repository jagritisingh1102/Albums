from flask_restful import Api
from .blueprints import bp
import re


def to_underscore(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class ApiFactory(Api):
    def init_app(self, app):
        super(ApiFactory, self).init_app(app)

    def register(self, **kwargs):

        def decorator(klass):
            document_name = klass.get_resource().model.__name__.lower()
            name = kwargs.pop('name', document_name)
            url = kwargs.pop('url', '/%s' %
                             to_underscore(klass.__name__).replace('_view', ''))
            endpoint = to_underscore(klass.__name__)
            view_func = klass.as_view(name)
            methods = klass.api_methods

            for method in methods:
                if method.slug:
                    self.app.add_url_rule(url + '/<string:slug>', endpoint=endpoint, view_func=view_func,
                                          methods=[method.method], **kwargs)
                else:
                    self.app.add_url_rule(url, endpoint=endpoint, view_func=view_func,
                                          methods=[method.method], **kwargs)
            return klass

        return decorator


api = ApiFactory(bp)
