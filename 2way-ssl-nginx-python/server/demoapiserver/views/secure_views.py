from demoapiserver.lib.decorator.auth import validate_client_identity, validate_client_token
from flask import Blueprint, jsonify, make_response

bp = Blueprint("secure", __name__, url_prefix="/secure")


@bp.route('/hello')
@validate_client_token()
@validate_client_identity()
def hello():
    return make_response(jsonify({
        "success": True
    })), 200


@bp.route('/lookup/<string:code>', methods=['GET'])
@validate_client_token()
@validate_client_identity()
def lookup(code):
    if code in [
        "unknown"
    ]:
        return make_response(jsonify({
            "success": False,
            "error": "Unknown code `{}`".format(code),
            "data": None
        })), 404

    return make_response(jsonify({
        "success": True,
        "data": {
            "code": code
        }
    })), 200
