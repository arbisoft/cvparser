import json
import os
from tkinter.constants import FALSE

from flask import Flask, jsonify, request
from flask_caching import Cache

from constants import CacheDuration, CACHE_CONFIG
from main import process_file
from workstream.utils import get_employment_education_suggestions

app = Flask(__name__, static_folder='static')
app.config["DEBUG"] = FALSE

SRCDIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(SRCDIR, 'static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

cache = Cache(app, config=CACHE_CONFIG)

get_cached_employment_educations = cache.cached(timeout=CacheDuration.one_day.value)(get_employment_education_suggestions)

@app.route('/parse', methods=['post'])
def upload():
    if request.method == 'POST':
        try:
            file = request.files['file']
            # right now existing cvs contains no ext so we have to add ext here.
            filename = file.filename

            if "." not in filename:
                filename = filename + ".pdf"

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            output, raw_output = process_file(file_path, debug=True)

            response = app.response_class(
                response=json.dumps({'data': output, 'raw_output': raw_output}),
                status=200,
                mimetype='application/json'
            )
            os.remove(file_path)
            return response
        except Exception as e:
            return jsonify({'error': str(e)})
