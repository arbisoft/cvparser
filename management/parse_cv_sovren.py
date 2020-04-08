import json
from base64 import b64encode
from requests import request
from glob import glob
from pathlib import Path
from flask_script import Command, Option

from constants import StatusCode


class ParseCvSovren(Command):
    """Make calls to sovren and save parsed result."""

    def run(self):
        for cv_file_name in glob('cvs/*'):
            base64doc = ''
            with open(cv_file_name, 'rb') as input_file:
                base64doc = b64encode(input_file.read()).decode('UTF-8')

            url = "https://rest.resumeparsing.com/v9/parser/resume"
            payload = {
                'DocumentAsBase64String': base64doc
                #other options here (see http://documentation.sovren.com/API/Rest/Parsing)
            }

            headers = {
                'accept': "application/json",
                'content-type': "application/json",
                'sovren-accountid': "",
                'sovren-servicekey': "",
            }

            response = request("POST", url, data=json.dumps(payload), headers=headers)
            #for response properties and types, see http://documentation.sovren.com/API/Rest/Parsing

            if response.status_code == StatusCode.HTTP_200_OK.value:
                output_file_name = 'sovren_processed_{}.json'.format(cv_file_name.replace('pdf', ''))
                with open(output_file_name, 'w') as output_file:
                    json.dump(response.json(), output_file)
            else:
                result = response.json().get('Info', {
                    'Code': StatusCode.HTTP_400_BAD_REQUEST.value,
                    'Message': StatusCode.HTTP_400_BAD_REQUEST.name
                })
                print('{} - {}: {}'.format(cv_file_name, result['Code'], result['Message']))
