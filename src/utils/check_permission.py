from flask_restful import Resource
from flask_jwt_extended import get_jwt_claims


class PermissionBase(Resource):

    def permission(perm, method):
        if method == 'PATCH':
            if perm in get_jwt_claims():
                if get_jwt_claims()[perm]['UPDATE']:
                    return True
                else:
                    return False
            return False
        elif method == 'GET':
            if perm in get_jwt_claims():
                if get_jwt_claims()[perm]['READ']:
                    return True
                else:
                    return False
            return False

        elif method == 'POST':
            if perm in get_jwt_claims():
                if get_jwt_claims()[perm]['WRITE']:
                    return True
                else:
                    return False
            return False

        elif method == 'DELETE':
            if perm in get_jwt_claims():
                if get_jwt_claims()[perm]['DELETE']:
                    return True
                else:
                    return False
            return False
        else:
            return False
