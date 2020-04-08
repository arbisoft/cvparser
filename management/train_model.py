import random
import spacy
import json
import re
from glob import glob
from pathlib import Path
from flask_script import Command, Option
from spacy.util import minibatch, compounding

from constants import Tag
from utils import label_entity, get_dates


class TrainModel(Command):
    """Train model based on data provided."""

    option_list = (
        Option('--model', '-m', dest='model'),
        Option('--input_folder', '-i', dest='input_folder')
    )

    def prepare_education_train_data(self, cv_data):
        education = cv_data.get('education', {})
        schools = education.get('SchoolOrInstitution', [])

        educations = []
        for school in schools:
            school_name = school['School'][0].get('SchoolName', '') if school.get('School', []) else ''

            degrees = school.get('Degree', [])
            for degree in degrees:
                degree_name = degree.get('DegreeName', '')
                comment = re.sub(r'[\s]', ' ', degree.get('Comments', ''))

                date_of_attendance = degree['DatesOfAttendance'][0] if degree.get('DatesOfAttendance', []) else {}
                start_date, end_date = get_dates(date_of_attendance)

                entities = []
                label_entity(comment, entities, degree_name, 'DEGREE')
                label_entity(comment, entities, school_name, 'ORG')
                label_entity(comment, entities, start_date, 'START_DATE')
                label_entity(comment, entities, end_date, 'END_DATE')
                educations.append((comment, {'entities': entities}))
        return educations

    def prepare_employment_train_data(self, cv_data):
        employment = cv_data.get('employment', {})
        employers = employment.get('EmployerOrg', [])

        employments = []
        for employer in employers:
            positions = employer.get('PositionHistory', [])
            for position in positions:
                title = position.get('Title', '')
                organization = position.get('OrgName', {}).get('OrganizationName', '')

                date_of_attendance = position['DatesOfAttendance'][0] if position.get('DatesOfAttendance', []) else {}
                start_date, end_date = get_dates(date_of_attendance)

                if title:
                    employments.append((title, {'entities': [(0, len(title), "DESIGNATION")]}))
                if organization:
                    employments.append((organization, {'entities': [(0, len(organization), "ORG")]}))
                if start_date:
                    employments.append((organization, {'entities': [(0, len(start_date), "START_DATE")]}))
                if end_date:
                    employments.append((organization, {'entities': [(0, len(end_date), "END_DATE")]}))
        return employments

    def get_train_data(self, input_folder):
        train_data = []
        for input_file in glob('{}/*.json'.format(input_folder)):
            with open(input_file) as json_file:
                cv_data = json.load(json_file)
                train_data += self.prepare_education_train_data(cv_data)
                train_data += self.prepare_employment_train_data(cv_data)
        return train_data

    def run(self, model, input_folder):
        model = model.strip()
        ADDITIONAL_LABELS = [tag.value for tag in Tag]
        n_iter = 25

        TRAIN_DATA = self.get_train_data(input_folder)

        model_dir = Path(model)
        if model and model_dir.exists():
            nlp = spacy.load(model)
            print("Loaded model '%s'" % model)
        else:
            nlp = spacy.load('en_core_web_sm')
            print("Created new model")

        if "ner" not in nlp.pipe_names:
            ner = nlp.create_pipe("ner")
            nlp.add_pipe(ner)
        else:
            ner = nlp.get_pipe("ner")

        for label in ADDITIONAL_LABELS:
            ner.add_label(label)

        other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
        with nlp.disable_pipes(*other_pipes):  # only train NER
            for _ in range(n_iter):
                random.shuffle(TRAIN_DATA)
                losses = {}
                # batch up the examples using spaCy's minibatch
                batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
                for batch in batches:
                    texts, annotations = zip(*batch)
                    nlp.update(
                        texts,  # batch of texts
                        annotations,  # batch of annotations
                        drop=0.25,  # dropout - make it harder to memorise data
                        losses=losses,
                    )
                print("Losses", losses)

        if not model_dir.exists():
            model_dir.mkdir()
        nlp.to_disk(model_dir)
        print("Saved model to", model_dir)
