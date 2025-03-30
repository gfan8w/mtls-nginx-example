import pprint

from flask import Blueprint, jsonify, make_response, request

from demoapiserver.lib.decorator.auth import validate_client_identity

bp = Blueprint("general", __name__, url_prefix="/")


@bp.route('/hello')
def hello():
    return make_response(jsonify({
        "success": True
    })), 200


@bp.route('/req_headers')
def request_headers():
    return make_response(jsonify({
        "success": True,
        "data": pprint.pformat(request.headers)
    })), 200


@bp.route('/req_env')
def request_env():
    return make_response(jsonify({
        "success": True,
        "data": pprint.pformat(request.environ)
    })), 200
