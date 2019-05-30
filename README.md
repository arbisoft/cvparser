# cvparser
Using spacy to extract and parse text from .pdf and .docx resumes


### Instructions

1. Create a python3 virtual env like so: 

`python3 -m venv '/path/to/venv'`
2. `pip install -r requirements.txt` Note that you may run into a problem with textract installation due to pocketsphinx. You can solve that by following the instructions [here](https://github.com/bambocher/pocketsphinx-python/issues/28#issuecomment-334493324)
3. Invoke the script from command line like so: 

`python main.py /path/to/pdfordoc [debug]`
