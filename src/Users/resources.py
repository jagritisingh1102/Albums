from flask import request
from ..utils.db import db
from flask import make_response, jsonify
from .schemas import UsersSchema
from .models import Users
from flask_restful import Resource
from ..utils.api import api
from ..utils.defaults import Default


class UsersResource(Resource):
    permission = 'USER'

    def get(self):
        try:
            data = request.args
            limit = Default.DEFAULT_LIMIT
            if '__limit' in data and data['__limit']:
                limit = data['__limit']
            users = Users.query.limit(limit).all()
            json_data = [UsersSchema().dump(user) for user in users]
            return make_response(jsonify({"data": json_data, "error": False}), 200)
        except Exception as e:
            return make_response(jsonify({'error': True, 'message': str(e)})), 422

    def post(self):
        data = request.json
        try:
            user, errors = UsersSchema().load(data, many=False, session=db)
            if errors:
                return make_response(jsonify({"err": errors}), 422)
            try:
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return make_response(jsonify(e), 422)
            return make_response(jsonify({'error': False, 'data': data,
                                          'message': 'User added successfully'}), 200)
        except Exception as e:
            return make_response(jsonify({'error': True, 'message': str(e)}), 422)

    def patch(self):
        if 'id' in request.args and request.args.get('id'):
            slug = request.args.get('id')
        else:
            return make_response(jsonify({'error': True, 'message': 'Method Not Allowed'}), 405)
        obj = Users.query.get(slug)
        if obj:
            try:
                obj = UsersSchema().load(request.json, instance=obj, partial=True, session=db)
                if obj:
                    user = Users.query.filter(Users.id == slug)
                    user.update(request.json)
                    db.session.commit()
                    return make_response(jsonify({'error': False, 'message': 'User Updated successfully'}), 200)
                else:
                    return make_response(jsonify({'error': True, 'message': 'User not found'}), 404)
            except Exception as e:
                print(e)
                db.session.rollback()
                return make_response(jsonify({'errors': str(e)}), 422)
        else:
            return make_response(jsonify({'error': True, 'message': 'User not found'}), 404)

    def delete(self):
        if 'id' in request.args and request.args.get('id'):
            slug = request.args.get('id')
        else:
            return make_response(jsonify({'error': True, 'message': 'Method Not Allowed'}), 405)
        obj = Users.query.get(slug)
        if obj:
            try:
                db.session.delete(obj)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return make_response(jsonify(e), 422)
            return make_response(jsonify({'error': False, 'message': 'User deleted successfully'}), 200)
        else:
            return make_response(jsonify({'error': True, 'message': 'User not found'}), 404)


api.add_resource(UsersResource, '/users', endpoint='users')

