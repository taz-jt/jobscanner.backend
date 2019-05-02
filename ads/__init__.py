from flask import Flask
from flask_cors import CORS
from ads import appconf
from ads.rest import api
import logging
# Import all Resources that are to be made visible for the app
from ads.rest.endpoint.auranest import AllJobsSearch

app = Flask(__name__)
CORS(app)

log = logging.getLogger(__name__)
log.debug(appconf.logging.getLevelName(log.getEffectiveLevel()) + ' log level activated')
log.info("Starting %s" % __name__)

if __name__ == '__main__':
    # Used only when starting this script directly, i.e. for debugging
    appconf.initialize_app(app, api)
    app.run(debug=True)
else:
    # Main entrypoint
    appconf.initialize_app(app, api)