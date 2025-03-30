import sys
import traceback
from datetime import datetime

from flask import jsonify, make_response, request

from demoapiserver.lib.common import flask_utils
from demoapiserver.views import logger


def http401(_):
    ip = flask_utils.get_real_remote_ip()
    url = request.url
    logger.warn("Unidentified client [{}] accessing {}".format(ip, url))
    return make_response(jsonify({
        'message': 'Unidentified'
    })), 401


def http404(_):
    return make_response(jsonify({
        'message': "Nothing here and that's all we know."
    })), 404


def exceptions(e):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    stack_str = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))

    ip = flask_utils.get_real_remote_ip()
    msg = "{}: {} ...\nremote ip: {}\nuser_agent: {}\nreq method: {}\nreq scheme: {}\nreq path: {}\ndatetime(utc): {}\nreferrer: {}\n--------- stack trace ---------\n{}\n\n".format(
        type(e), e,
        ip, request.user_agent, request.method, request.scheme, request.full_path, datetime.utcnow(),
        request.referrer,
        stack_str
    )
    logger.error(msg)
