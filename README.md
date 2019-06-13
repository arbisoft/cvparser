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


3. Invoke the script from command line:

    `python main.py /path/to/pdfordoc [debug]`
