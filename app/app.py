import logging
import os

from flask import Flask
from flask_cors import CORS

from app import jwt_handlers
from app.extensions import database, jwt
from app.routes.error_handler import handle_all_unhandled_exceptions
from app.routes.personal_info_route import personal_info_bp


def create_app() -> Flask:
    """
    Creates and configures the Flask application.

    This function creates a new Flask application, configures it from a
    configuration file, sets up CORS, logging, extensions, and registers
    blueprints. Also sets up a global error handler for unhandled exceptions.

    :returns: The configured Flask application.
    """

    personal_info_api = Flask(__name__)
    personal_info_api.config.from_pyfile('config.py')
    personal_info_api.errorhandler(Exception)(handle_all_unhandled_exceptions)

    CORS(personal_info_api, resources={r"/api/*": {
        "origins": "https://client-service-f45dc8e85ddf.herokuapp.com"}})

    setup_logging(personal_info_api)
    setup_extensions(personal_info_api)
    register_blueprints(personal_info_api)

    return personal_info_api


def setup_logging(personal_info_api: Flask) -> None:
    """
    Sets up logging for the Flask application.

    This function sets up logging for the Flask application. If LOG_TO_STDOUT
    is enabled in the configuration, it sets up logging to stdout. Otherwise,
    it configures logging to a file.

    :param personal_info_api: The Flask application.
    """

    log_level = personal_info_api.config.get('LOG_LEVEL', 'INFO').upper()
    log_format = personal_info_api.config.get(
            'LOG_FORMAT',
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if personal_info_api.config.get('LOG_TO_STDOUT'):
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(log_level)
        stream_handler.setFormatter(logging.Formatter(log_format))
        logging.getLogger().addHandler(stream_handler)
    else:
        log_dir = personal_info_api.config.get('LOG_DIR', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        file_handler = logging.FileHandler(personal_info_api.config.get(
                'LOG_FILE', os.path.join(log_dir, 'app.log')))
        file_handler.setLevel(log_level)
        file_handler.setFormatter(logging.Formatter(log_format))
        logging.getLogger().addHandler(file_handler)

    logging.getLogger().setLevel(log_level)


def setup_extensions(personal_info_api: Flask) -> None:
    """
    Sets up extensions for the Flask application.

    This function initializes the database and JWT extensions for the Flask
    application, and registers JWT error handlers. It also creates all
    database tables.

    :param personal_info_api: The Flask application.
    """

    database.init_app(personal_info_api)
    jwt.init_app(personal_info_api)
    jwt_handlers.register_jwt_handlers(jwt)

    with personal_info_api.app_context():
        database.create_all()


def register_blueprints(personal_info_api: Flask) -> None:
    """
    Registers blueprints for the Flask application.

    This function registers blueprints for the Flask application. Each
    blueprint corresponds to a different part of the application.

    :param personal_info_api: The Flask application.
    """

    personal_info_api.register_blueprint(
            personal_info_bp, url_prefix='/api/applicant/personal-info')


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
