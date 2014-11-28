import json
from flask import Blueprint
from flask import Response
from flask import request
from flask.ext.cors import cross_origin
from geobricks_processing.config.config import config

from geobricks_processing.core import processing_core as p

app = Blueprint(__name__, __name__)

@app.route('/discovery/')
@cross_origin(origins='*')
def discovery():
    """
    Discovery service available for all Geobricks libraries that describes the plug-in.
    @return: Dictionary containing information about the service.
    """
    out = {
        'name': 'RASTER PROCESSING',
        'description': 'Core functionalities and services to processes raster data.',
        'type': 'RASTER_PROCESSING'
    }
    return Response(json.dumps(out), content_type='application/json; charset=utf-8')


@app.route('/process/', methods=['POST'])
@cross_origin(origins='*', headers=['Content-Type'])
def process_data_obj():
    user_json = request.get_json()
    p.process_data(user_json, config["setting"]["logging"]["level"])
    return Response(json.dumps({}), content_type='application/json; charset=utf-8')