import json
import os
from tkinter.constants import FALSE

from flask import Flask, jsonify, request
from flask_caching import Cache
from requests import status_codes

from constants import CACHE_CONFIG, CacheDuration, StatusCode
from main import process_file

app = Flask(__name__, static_folder='static')
app.config["DEBUG"] = False

SRCDIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(SRCDIR, 'static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

cache = Cache(app, config=CACHE_CONFIG)

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
                status=StatusCode.HTTP_200_OK.value,
                mimetype='application/json'
            )
            os.remove(file_path)
            return response
        except Exception as e:
            return app.response_class(
                response=jsonify({'error': str(e)}),
                status=StatusCode.HTTP_400_BAD_REQUEST.value,
                mimetype='application/json'
            )
