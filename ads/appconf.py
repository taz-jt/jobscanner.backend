import os
from ads import settings
import logging.config
import os

file_dir = os.path.split(os.path.realpath(__file__))[0]
logging.config.fileConfig(os.path.join(file_dir, 'logging.conf'),
                          disable_existing_loggers=False)

def configure_app(flask_app):
    flask_app.config.SWAGGER_UI_DOC_EXPANSION = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config.RESTPLUS_VALIDATE = settings.RESTPLUS_VALIDATE
    flask_app.config.RESTPLUS_MASK_SWAGGER = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config.ERROR_404_HELP = settings.RESTPLUS_ERROR_404_HELP

def initialize_app(flask_app, api):
    configure_app(flask_app)
    api.init_app(flask_app)