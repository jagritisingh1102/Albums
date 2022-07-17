from flask import request
from ..utils.db import db
from flask import make_response, jsonify
from .schemas import ImagesSchema, ArtistsSchema, ItemsSchema, AlbumsSchema, TracksSchema
from .models import Images, Artists, Items, Albums, Tracks
from flask_jwt_extended import jwt_required
from ..utils.api import api
from ..utils.check_permission import PermissionBase
from ..utils.defaults import Default
from ..utils.security import security_v
from ..utils.blueprints import bp


class ImagesResource(PermissionBase):
    method_decorators = [jwt_required]
    permission = 'IMAGE'

    def get(self):
        if PermissionBase.permission(self.permission, Default.GET_METHOD) is False:
            return make_response(jsonify({'error': True, 'message': 'Permission denied'}), 403)
        try:
            data = request.args
            limit = Default.DEFAULT_LIMIT
            if '__limit' in data and data['__limit']:
                limit = data['__limit']
            images = Images.query.limit(limit).all()
            json_data = [ImagesSchema().dump(image) for image in images]
            return make_response(jsonify({"data": json_data, "error": False}), 200)
        except Exception as e:
            return make_response(jsonify({'error': True, 'message': str(e)}), 422)

    def post(self):
        if PermissionBase.permission(self.permission, Default.POST_METHOD) is False:
            return make_response(jsonify({'error': True, 'message': 'Permission denied'}), 403)
        data = request.json
        try:
            image, errors = ImagesSchema().load(data, many=False, session=db)
            if errors:
                return make_response(jsonify(errors), 422)

            try:
                db.session.add(image)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return make_response(jsonify(e), 422)
            return make_response(jsonify({'error': False, 'data': data,
                                          'message': 'Image added successfully'}), 200)
        except Exception as e:
            return make_response(jsonify({'error': True, 'error_messages': str(e)}), 422)

    def patch(self):
        if PermissionBase.permission(self.permission, Default.PATCH_METHOD) is False:
            return make_response(jsonify({'error': True, 'message': 'Permission denied'}), 403)
        if 'id' in request.args and request.args.get('id'):
            slug = request.args.get('id')
        else:
            return make_response(jsonify({'error': True, 'message': 'Method Not Allowed'}), 405)
        obj = Images.query.get(slug)
        if obj:
            try:
                obj = ImagesSchema().load(request.json, instance=obj, session=db)
                if obj:
                    image = Images.query.filter(Images.id == slug)
                    image.update(request.json)
                    db.session.commit()
                    return make_response(jsonify({'error': False, 'message': 'Image Updated successfully'}), 200)
                else:
                    return make_response(jsonify({'error': True, 'message': 'Image not found'}), 404)
            except Exception as e:
                db.session.rollback()
                return make_response(jsonify(e), 422)
        else:
            return make_response(jsonify({'error': True, 'message': 'Image not found'}), 404)

    def delete(self):
        if PermissionBase.permission(self.permission, Default.DELETE_METHOD) is False:
            return make_response(jsonify({'error': True, 'message': 'Permission denied'}), 403)
        if 'id' in request.args and request.args.get('id'):
            slug = request.args.get('id')
        else:
            return make_response(jsonify({'error': True, 'message': 'Method Not Allowed'}), 405)
        obj = Images.query.get(slug)
        if obj:
            try:
                db.session.delete(obj)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return make_response(jsonify(e), 422)
            return make_response(jsonify({'error': False, 'message': 'Image deleted successfully'}), 200)
        else:
            return make_response(jsonify({'error': True, 'message': 'Image not found'}), 404)


api.add_resource(ImagesResource, '/images', endpoint='images')


class ArtistsResource(PermissionBase):
    method_decorators = [jwt_required]
    permission = 'ARTIST'

    def get(self):
        if PermissionBase.permission(self.permission, Default.GET_METHOD) is False:
            return make_response(jsonify({'error': True, 'message': 'Permission denied'}), 403)
        try:
            data = request.args
            limit = Default.DEFAULT_LIMIT
            if '__limit' in data and data['__limit']:
                limit = data['__limit']
            artists = Artists.query.limit(limit).all()
            json_data = [ArtistsSchema().dump(artist) for artist in artists]
            return make_response(jsonify({"data": json_data, "error": False}), 200)
        except Exception as e:
            return make_response(jsonify({'error': True, 'message': str(e)}), 422)

    def post(self):
        if PermissionBase.permission(self.permission, Default.POST_METHOD) is False:
            return make_response(jsonify({'error': True, 'message': 'Permission denied'}), 403)
        data = request.json
        try:
            artist, errors = ArtistsSchema().load(data, many=False, session=db)
            if errors:
                return make_response(jsonify(errors), 422)
            try:
                db.session.add(artist)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return make_response(jsonify(e), 422)
            return make_response(jsonify({'error': False, 'data': data,
                                          'message': 'Artist added successfully'}), 200)
        except Exception as e:
            return make_response(jsonify({'error': True, 'message': str(e)}), 422)

    def patch(self):
        if PermissionBase.permission(self.permission, Default.POST_METHOD) is False:
            return make_response(jsonify({'error': True, 'message': 'Permission denied'}), 403)
        if 'id' in request.args and request.args.get('id'):
            slug = request.args.get('id')
        else:
            return make_response(jsonify({'error': True, 'message': 'Method Not Allowed'}), 405)
        obj = Artists.query.get(slug)
        if obj:
            try:
                obj = ArtistsSchema().load(request.json, instance=obj, partial=True, session=db)
                if obj:
                    artist = Artists.query.filter(Artists.id == slug)
                    artist.update(request.json)
                    db.session.commit()
                    return make_response(jsonify({'error': False, 'message': 'Artist Updated successfully'}), 200)
                else:
                    return make_response(jsonify({'error': True, 'message': 'Artist not found'}), 404)
            except Exception as e:
                print(e)
                db.session.rollback()
                return make_response(jsonify({'errors': str(e)}), 422)
        else:
            return make_response(jsonify({'error': True, 'message': 'Artist not found'}), 404)

    def delete(self):
        if PermissionBase.permission(self.permission, Default.POST_METHOD) is False:
            return make_response(jsonify({'error': True, 'message': 'Permission denied'}), 403)
        if 'id' in request.args and request.args.get('id'):
            slug = request.args.get('id')
        else:
            return make_response(jsonify({'error': True, 'message': 'Method Not Allowed'}), 405)
        obj = Artists.query.get(slug)
        if obj:
            try:
                db.session.delete(obj)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return make_response(jsonify(e), 422)
            return make_response(jsonify({'error': False, 'message': 'Artist deleted successfully'}), 200)
        else:
            return make_response(jsonify({'error': True, 'message': 'Artist not found'}), 404)


api.add_resource(ArtistsResource, '/artists', endpoint='artists')


class ItemsResource(PermissionBase):
    method_decorators = [jwt_required]
    permission = 'ITEM'

    def get(self):
        if PermissionBase.permission(self.permission, Default.GET_METHOD) is False:
            return make_response(jsonify({'error': True, 'message': 'Permission denied'}), 403)
        try:
            data = request.args
            limit = Default.DEFAULT_LIMIT
            if '__limit' in data and data['__limit']:
                limit = data['__limit']
            items = Items.query.limit(limit).all()
            json_data = [ItemsSchema().dump(item) for item in items]
            return make_response(jsonify({"data": json_data, "error": False}), 200)
        except Exception as e:
            return make_response(jsonify({'error': True, 'message': str(e)}), 422)

    def post(self):
        if PermissionBase.permission(self.permission, Default.POST_METHOD) is False:
            return make_response(jsonify({'error': True, 'message': 'Permission denied'}), 403)
        data = request.json
        try:
            item, errors = ItemsSchema().load(data, many=False, session=db)
            if errors:
                return make_response(jsonify(errors), 422)
            try:
                db.session.add(item)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return make_response(jsonify(e), 422)
            return make_response(jsonify({'error': False, 'data': data,
                                          'message': 'Items added successfully'}), 200)
        except Exception as e:
            return make_response(jsonify({'error': True, 'message': str(e)}), 422)

    def patch(self):
        if PermissionBase.permission(self.permission, Default.PATCH_METHOD) is False:
            return make_response(jsonify({'error': True, 'message': 'Permission denied'}), 403)
        if 'id' in request.args and request.args.get('id'):
            slug = request.args.get('id')
        else:
            return make_response(jsonify({'error': True, 'message': 'Method Not Allowed'}), 405)
        obj = Items.query.get(slug)
        if obj:
            try:
                obj = ItemsSchema().load(request.json, instance=obj, partial=True, session=db)
                if obj:
                    item = Items.query.filter(Items.id == slug)
                    item.update(request.json)
                    db.session.commit()
                    return make_response(jsonify({'error': False, 'message': 'Item Updated successfully'}), 200)
                else:
                    return make_response(jsonify({'error': True, 'message': 'Item not found'}), 404)
            except Exception as e:
                print(e)
                db.session.rollback()
                return make_response(jsonify({'errors': str(e)}), 422)
        else:
            return make_response(jsonify({'error': True, 'message': 'Item not found'}), 404)

    def delete(self):
        if PermissionBase.permission(self.permission, Default.DELETE_METHOD) is False:
            return make_response(jsonify({'error': True, 'message': 'Permission denied'}), 403)
        if 'id' in request.args and request.args.get('id'):
            slug = request.args.get('id')
        else:
            return make_response(jsonify({'error': True, 'message': 'Method Not Allowed'}), 405)
        obj = Items.query.get(slug)
        if obj:
            try:
                db.session.delete(obj)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return make_response(jsonify(e), 422)
            return make_response(jsonify({'error': False, 'message': 'Item deleted successfully'}), 200)
        else:
            return make_response(jsonify({'error': True, 'message': 'Item not found'}), 404)


api.add_resource(ItemsResource, '/items', endpoint='items')


class TracksResource(PermissionBase):
    method_decorators = [jwt_required]
    permission = 'TRACK'

    def get(self):
        if PermissionBase.permission(self.permission, Default.GET_METHOD) is False:
            return make_response(jsonify({'error': True, 'message': 'Permission denied'}), 403)
        try:
            data = request.args
            limit = Default.DEFAULT_LIMIT
            if '__limit' in data and data['__limit']:
                limit = data['__limit']
            tracks = Tracks.query.limit(limit).all()
            json_data = [TracksSchema().dump(track) for track in tracks]
            return make_response(jsonify({"data": json_data, "error": False}), 200)
        except Exception as e:
            return make_response(jsonify({'error': True, 'message': str(e)}), 422)

    def post(self):
        if PermissionBase.permission(self.permission, Default.POST_METHOD) is False:
            return make_response(jsonify({'error': True, 'message': 'Permission denied'}), 403)
        data = request.json
        try:
            track, errors = TracksSchema().load(data, many=False, session=db)
            if errors:
                return make_response(jsonify(errors), 422)
            try:
                db.session.add(track)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return make_response(jsonify(e), 422)
            return make_response(jsonify({'error': False, 'data': data,
                                          'message': 'Tracks added successfully'}), 200)
        except Exception as e:
            return make_response(jsonify({'error': True, 'message': str(e)}), 422)

    def patch(self):
        if PermissionBase.permission(self.permission, Default.PATCH_METHOD) is False:
            return make_response(jsonify({'error': True, 'message': 'Permission denied'}), 403)
        if 'id' in request.args and request.args.get('id'):
            slug = request.args.get('id')
        else:
            return make_response(jsonify({'error': True, 'message': 'Method Not Allowed'}), 405)
        obj = Tracks.query.get(slug)
        if obj:
            try:
                obj = TracksSchema().load(request.json, instance=obj, partial=True, session=db)
                if obj:
                    exist_record = Tracks.query.filter(Tracks.id == slug)
                    exist_record.update(request.json)
                    db.session.commit()
                    return make_response(jsonify({'error': False, 'message': 'Track Updated successfully'}), 200)
                else:
                    return make_response(jsonify({'error': True, 'message': 'Track not found'}), 404)
            except Exception as e:
                print(e)
                db.session.rollback()
                return make_response(jsonify({'errors': str(e)}), 422)
        else:
            return make_response(jsonify({'error': True, 'message': 'Track not found'}), 404)

    def delete(self):
        if PermissionBase.permission(self.permission, Default.DELETE_METHOD) is False:
            return make_response(jsonify({'error': True, 'message': 'Permission denied'}), 403)
        if 'id' in request.args and request.args.get('id'):
            slug = request.args.get('id')
        else:
            return make_response(jsonify({'error': True, 'message': 'Method Not Allowed'}), 405)
        obj = Tracks.query.get(slug)
        if obj:
            try:
                db.session.delete(obj)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return make_response(jsonify(e), 422)
            return make_response(jsonify({'error': False, 'message': 'Track deleted successfully'}), 200)
        else:
            return make_response(jsonify({'error': True, 'message': 'Track not found'}), 404)


api.add_resource(TracksResource, '/tracks', endpoint='tracks')


class AlbumsResource(PermissionBase):
    method_decorators = [jwt_required]
    permission = 'ALBUM'

    def get(self):
        if PermissionBase.permission(self.permission, Default.GET_METHOD) is False:
            return make_response(jsonify({'error': True, 'message': 'Permission denied'}), 403)
        try:
            data = request.args
            limit = Default.DEFAULT_LIMIT
            if '__limit' in data and data['__limit']:
                limit = data['__limit']
            albums = Albums.query.limit(limit).all()
            json_data = [AlbumsSchema().dump(album) for album in albums]
            return make_response(jsonify({"data": json_data, "error": False}), 200)
        except Exception as e:
            return make_response(jsonify({'error': True, 'message': str(e)})), 422

    def post(self):
        if PermissionBase.permission(self.permission, Default.POST_METHOD) is False:
            return make_response(jsonify({'error': True, 'message': 'Permission denied'}), 403)
        data = request.json
        try:
            album, errors = AlbumsSchema().load(data, many=False, session=db)
            if errors:
                return make_response(jsonify(errors), 422)
            try:
                db.session.add(album)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return make_response(jsonify(e), 422)
            return make_response(jsonify({'error': False, 'data': data,
                                          'message': 'Album added successfully'}), 200)
        except Exception as e:
            return make_response(jsonify({'error': True, 'message': str(e)}), 422)

    def patch(self):
        if PermissionBase.permission(self.permission, Default.PATCH_METHOD) is False:
            return make_response(jsonify({'error': True, 'message': 'Permission denied'}), 403)
        if 'id' in request.args and request.args.get('id'):
            slug = request.args.get('id')
        else:
            return make_response(jsonify({'error': True, 'message': 'Method Not Allowed'}), 405)
        obj = Albums.query.get(slug)
        if obj:
            try:
                obj = AlbumsSchema().load(request.json, instance=obj, partial=True, session=db)
                if obj:
                    album = Albums.query.filter(Albums.id == slug)
                    album.update(request.json)
                    db.session.commit()
                    return make_response(jsonify({'error': False, 'message': 'Album Updated successfully'}), 200)
                else:
                    return make_response(jsonify({'error': True, 'message': 'Album not found'}), 404)
            except Exception as e:
                print(e)
                db.session.rollback()
                return make_response(jsonify({'errors': str(e)}), 422)
        else:
            return make_response(jsonify({'error': True, 'message': 'Album not found'}), 404)

    def delete(self):
        if PermissionBase.permission(self.permission, Default.DELETE_METHOD) is False:
            return make_response(jsonify({'error': True, 'message': 'Permission denied'}), 403)
        if 'id' in request.args and request.args.get('id'):
            slug = request.args.get('id')
        else:
            return make_response(jsonify({'error': True, 'message': 'Method Not Allowed'}), 405)
        obj = Albums.query.get(slug)
        if obj:
            try:
                db.session.delete(obj)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return make_response(jsonify(e), 422)
            return make_response(jsonify({'error': False, 'message': 'Album deleted successfully'}), 200)
        else:
            return make_response(jsonify({'error': True, 'message': 'Album not found'}), 404)


api.add_resource(AlbumsResource, '/album', endpoint='albums')


@bp.route('/user_login', methods=['POST'])
def login():
    data = request.json
    user_id = security_v.get_user(email=data['email'])

    if not user_id:
        return make_response(jsonify({'message': 'User not found'}), 403)

    verified = security_v.check_password(user_id, data['password'])
    if not verified:
        return make_response(jsonify({'message': 'Invalid password'}), 403)

    access_token = security_v.get_token(user_id)
    return make_response(
        jsonify({'token': 'Bearer ' + access_token}), 200)
