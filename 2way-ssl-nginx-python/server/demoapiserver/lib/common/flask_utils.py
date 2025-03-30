import inspect

from flask import request

from demoapiserver.lib import logger


def get_real_remote_ip():
    """
    :return: (str)
    """
    if request.headers.getlist("X-Forwarded-For"):
        remote_ip = request.environ['HTTP_X_FORWARDED_FOR']
    else:
        remote_ip = request.remote_addr

    if remote_ip:
        remote_ip = remote_ip.split(",")[0]  # the first IP is the remote and the next IP is the reverse proxy

    return remote_ip


def get_remote_ssl_client_cert():
    """
    :return: (str)
    """
    if request.headers.getlist("X-Client-Cert"):
        return request.environ['HTTP_X_CLIENT_CERT']
    else:
        log_info("no X-Client-Cer in headers")
    return None


def log_error(msg):
    last_frame = inspect.currentframe().f_back
    frameinfo = inspect.getframeinfo(last_frame)

    if not msg:
        msg = u""

    msg = "[{}:{}]: [{}] {}\n--------- Request info ---------\nReferral url: {}\nRequest url: {}\n\n".format(
        frameinfo.filename, frameinfo.lineno,
        get_real_remote_ip(), msg,
        request.referrer,
        request.url,
    )
    logger.error(msg)


def log_info(msg):
    last_frame = inspect.currentframe().f_back
    frameinfo = inspect.getframeinfo(last_frame)

    if not msg:
        msg = u""

    msg = "[{}:{}]: [{}] {} ({} -> {})".format(
        frameinfo.filename, frameinfo.lineno,
        get_real_remote_ip(), msg,
        request.referrer,
        request.url,
    )
    logger.info(msg)
