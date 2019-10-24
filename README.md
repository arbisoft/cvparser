# cvparser
Using spacy to extract and parse text from .pdf and .docx resumes


### Instructions

1. Create a python3 virtual env and activate it:

   `python3 -m venv '/path/to/venv'`

2. Install requirements:

   If pocketsphinx is not installed then first run:

       `make install_pocketsphinx`

   When pocketsphinx installed, then run:

       `make requirements`

3. Run the flask server:

    `FLASK_APP=api.py flask run`

4. The server runs on port `5000` by default, you can call the api on `http://localhost:5000/parse` with passing the file in body against `file` key.
