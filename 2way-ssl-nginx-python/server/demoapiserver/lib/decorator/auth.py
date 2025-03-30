from functools import wraps

from demoapiserver.lib.common import flask_utils, x509_utils
from demoapiserver.lib.common.flask_utils import log_info, log_error
from demoapiserver.lib.conf import app_settings
from flask import jsonify, make_response, request


def validate_client_identity():
    def wrapper(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            pem_cert = flask_utils.get_remote_ssl_client_cert()
            x509 = x509_utils.pem_str_to_x509(pem_cert)
            cn = x509_utils.get_subject_cn_from_x509(x509)
            if not cn or cn not in app_settings.VALID_CLIENT_CNS:
                log_error("Invalid client identity %s is not in whitelist" % cn)
                return make_response(jsonify({
                    'success': False,
                    'error': "Invalid client identity %s is not in whitelist" % cn,
                })), 401

            return fn(*args, **kwargs)
        return decorated_function
    return wrapper


def validate_client_token():
    def wrapper(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            token = request.headers.get(app_settings.SHARED_SECRET_CLIENT2SERVER_PARAM)
            log_info("header: {}-{}".format(app_settings.SHARED_SECRET_CLIENT2SERVER_PARAM, token))
            if token != app_settings.SHARED_SECRET_CLIENT2SERVER_VALUE:
                return make_response(jsonify({
                    'success': False,
                    'error': "Invalid client token",
                })), 401

            return fn(*args, **kwargs)
        return decorated_function
    return wrapper
