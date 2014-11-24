from flask import Flask
from flask.ext.cors import CORS
from flask import jsonify
from flask import render_template
from flask import Response
from flask import request
from flask.ext.cors import cross_origin
from geobricks_processing.config.rest_config import config
from geobricks_processing.rest import processing_rest
import logging

# Initialize the Flask app
app = Flask(__name__)

# Initialize CORS filters
cors = CORS(app, resources={r'/*': {'origins': '*'}})

# Core services.
app.register_blueprint(processing_rest.app, url_prefix='/geobricks_processing')

# Logging level.
log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)

# Start Flask server
if __name__ == '__main__':
    app.run(host=config['host'], port=config['port'], debug=config['debug'], threaded=True)