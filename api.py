import json
import os

from flask import Flask, jsonify, request
from flask_caching import Cache

from constants import CACHE_CONFIG, StatusCode
from main import process_file, process_job_description

app = Flask(__name__, static_folder='static')
app.config["DEBUG"] = False

SRCDIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(SRCDIR, 'static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

cache = Cache(app, config=CACHE_CONFIG)

@app.route('/parse', methods=['POST'])
def upload():
    file = request.files['file']

    filename = '{}.pdf'.format(file.filename) if "." not in file.filename else file.filename

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    try:
        output, raw_output = process_file(file_path)

        response = app.response_class(
            response=json.dumps({'data': output, 'raw_output': raw_output}),
            status=StatusCode.HTTP_200_OK.value,
            mimetype='application/json'
        )
        os.remove(file_path)
        return response
    except Exception as e:
        os.remove(file_path)
        return app.response_class(
            response=json.dumps({'error': str(e)}),
            status=StatusCode.HTTP_400_BAD_REQUEST.value,
            mimetype='application/json'
        )


@app.route('/retrieve_skills', methods=['POST'])
def retrieve_skills():
    try:
        job_description = request.values.get('job_description', '')

        output = process_job_description(job_description)

        return app.response_class(
            response=json.dumps({ 'skills': output }),
            status=StatusCode.HTTP_200_OK.value,
            mimetype='application/json'
        )
    except Exception as e:
        return app.response_class(
            response=json.dumps({'error': str(e)}),
            status=StatusCode.HTTP_400_BAD_REQUEST.value,
            mimetype='application/json'
        )
