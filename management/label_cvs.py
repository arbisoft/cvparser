import json
from glob import glob
from enum import Enum
from pathlib import Path
from flask_script import Command, Option


class ResponseCode(Enum):
    SUCCESS = 'Success'


class LabelCVs(Command):
    """Make calls to sovren and save parsed result."""

    option_list = (
        Option('--input_folder', '-i', dest='input_folder'),
        Option('--output_folder', '-o', dest='output_folder')
    )

    @staticmethod
    def parse_cv_info(cv):
        json_cv = json.loads(cv.get('Value', {}).get('ParsedDocument', '{}').replace('\r\n', ''))
        structured_resume = json_cv.get('Resume', {}).get('StructuredXMLResume', {})
        contact_info = structured_resume.get('ContactInfo', {})
        education_history = structured_resume.get('EducationHistory', {})
        employment_history = structured_resume.get('EmploymentHistory', {})

        return contact_info, education_history, employment_history

    def run(self, input_folder, output_folder):
        for input_file in glob('{}/*.json'.format(input_folder)):
            data = {
                'contact_info': {}, 'education': {}, 'employment': {}
            }
            with open(input_file) as json_file:
                cv_data = json.load(json_file)
                # if cv_data['Info']['Code'] == ResponseCode.SUCCESS.value:
                contact_info, education_history, employment_history = self.parse_cv_info(cv_data)
                data['education'] = education_history
                data['employment'] = employment_history
                data['contact_info'] = contact_info

                with open('{}/{}'.format(output_folder, input_file.split('/')[1]), 'w') as output_file:
                    json.dump(data, output_file)
                # else:
                #     print(f'Error occured while processing {input_file}')
