import logging

from demoapiserver.lib.conf import app_settings
from flask import Flask, request

from demoapiserver.views import exception_views, general_views, secure_views

logger = logging.getLogger("demoapiserver")


def create_app():
    app = Flask(__name__)

    @app.after_request
    def secure_reply(response):
        if response.status_code not in [
            200, 201,
        ]:
            # we don't give out shared secret token. just return the response as is.
            return response

        if not request.endpoint.startswith("secure."):  # "secure" is the Blueprint name
            return response

        response.headers[app_settings.SHARED_SECRET_SERVER2CLIENT_PARAM] = app_settings.SHARED_SECRET_SERVER2CLIENT_VALUE
        return response

    # register error handling
    app.register_error_handler( 401, exception_views.http401)
    app.register_error_handler( 404, exception_views.http404)
    app.register_error_handler( Exception, exception_views.exceptions)

    # register the blueprints
    app.register_blueprint(general_views.bp)
    app.register_blueprint(secure_views.bp)

    return app


application = create_app()
gunicorn_logger = logging.getLogger("gunicorn.error")
application.logger.handlers = gunicorn_logger.handlers
application.logger.setLevel(gunicorn_logger.level)


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=80, debug=True)
