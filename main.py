import json
import re
import sys
from collections import OrderedDict
from itertools import tee
from pathlib import Path

import spacy
import textract
import tika
from spacy.lang.en import English
from spacy.pipeline import EntityRuler, merge_entities
from spacy.tokens import Span
from tika import parser

import patterns
from constants import EntityType, Tag
from utils import get_education_employment_keys, tag_entity, get_logger

tika.initVM()
logger = get_logger()


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def extract_name(text, output={}):
    lines = text.split('\n')
    ignorelist = ['resume']
    output['name'] = [[l for l in lines
                       if l.strip() and l.strip().lower() not in ignorelist][0]]
    return output


def update_output(doc, output):
    for ent in doc.ents:
        if not output.get(ent.label_.lower(), None):
            output[ent.label_.lower()] = []
        output[ent.label_.lower()] += [t for t in ent.text.splitlines() if t.strip()]
    for ent in doc.ents:
        # removing duplicate skills
        if ent.label_.lower() == 'skill':
            output[ent.label_.lower()] = list(set(output[ent.label_.lower()]))
    return output


def expand_sections(doc):
    new_ents = []
    ent = next_ent = None
    for ent, next_ent in pairwise(doc.ents):
        label = ent.text.strip()
        if ent.label_ == "SECTIONS" and ent.start != 0:
            try:
                new_ent = Span(doc, ent.end, next_ent.start - 1, label=label)
                new_ents.append(new_ent)
            except:
                new_ents.append(ent)
        else:
            new_ents.append(ent)

    # last item doesnt get processed when iterating pairwise
    # so we need additional code to process it
    if len(doc.ents) == 1:
        next_ent = doc.ents[0]
    if next_ent and next_ent.label_ == "SECTIONS" and next_ent.start != 0:
        try:
            new_ent = Span(doc, next_ent.end, len(doc), label=next_ent.text.strip())
            new_ents.append(new_ent)
        except:
            new_ents.append(next_ent)

    doc.ents = new_ents
    return doc


def extract_entities(text, output={}):
    nlp = English()
    ruler = EntityRuler(nlp)
    ruler.add_patterns(patterns.patterns + patterns.section_patterns)
    nlp.add_pipe(ruler)
    doc = nlp(text)

    logger.debug('TOKENS: {}'.format('\n'.join(['{} {}'.format(i, t.text) for i, t in enumerate(doc)])))
    logger.debug('ENTITIES: {}'.format('\n'.join(['{}:{}'.format(ent.label_, ent.text) for ent in doc.ents])))

    return update_output(doc, output)


def extract_sections(text, output={}):
    nlp = English()
    ruler = EntityRuler(nlp)
    ruler.add_patterns(patterns.section_patterns)
    nlp.add_pipe(ruler)
    nlp.add_pipe(expand_sections)
    doc = nlp(text)

    logger.debug('SESSION TOKENS: {}'.format(
        '\n'.join(['{} {}'.format(i, t.text) for i, t in enumerate(doc)])))
    logger.debug('SESSION ENTITIES: {}'.format(
        '\n'.join(['{}:{}:{}:{}'.format(ent.label_, ent.text.strip(), ent.start, ent.end) for ent in doc.ents])))

    return update_output(doc, output)


def filter_employments_educations(cv_data):
    tagged_education = []
    tagged_employment = []

    def extract_degree_orgs(doc):
        entities = [ent for ent in doc.ents if ent.label_ == Tag.ORGANIZATION.value]
        tag_entity(EntityType.EDUCATION, entities, tagged_education)
        return doc

    def extract_position_employments(doc):
        entities = [ent for ent in doc.ents if ent.label_ == Tag.ORGANIZATION.value]
        tag_entity(EntityType.EMPLOYMENT, entities, tagged_education)
        return doc

    model = 'education'
    model_dir = Path(model)
    if model and model_dir.exists():
        nlp = spacy.load(model)
        logger.info("Loaded model '%s'" % model)
    else:
        nlp = spacy.load('en_core_web_sm')
        logger.info("Created new model")

    nlp.add_pipe(merge_entities)
    nlp.add_pipe(extract_degree_orgs)
    nlp.add_pipe(extract_position_employments)

    education_key, employment_key = get_education_employment_keys(cv_data)

    education_text = re.sub(r'[\s]', ' ', '\n'.join(cv_data.get(education_key, '')))
    education_text = education_text.encode('ascii', 'ignore').decode()
    with nlp.disable_pipes('extract_position_employments'):
        nlp(education_text)

    cv_data['tagged_education'] = tagged_education

    employment_text = re.sub(r'[\s]', ' ', '\n'.join(cv_data.get(employment_key, '')))
    employment_text = employment_text.encode('ascii', 'ignore').decode()
    with nlp.disable_pipes('extract_degree_orgs'):
        nlp(employment_text)

    cv_data['tagged_employment'] = tagged_employment


def process_file(filepath):
    text1 = textract.process(filepath).decode('utf-8')
    text2 = parser.from_file(filepath)['content']

    logger.debug('Raw Text Textract: {}'.format(text1))
    logger.debug('Raw Test Tika: {}'.format(text2))

    raw_output = text1
    if len(text2) > len(text1):
        raw_output = text2

    output = OrderedDict()

    for k in ['name', 'cell', 'email', 'nic', 'skills']:
        output[k] = []
    output = extract_name(text1, output)
    output = extract_entities(text1, output)
    sections1 = extract_sections(text1, {})
    sections2 = extract_sections(text2, {})

    if len(sections2) >= len(sections1):
        output = extract_sections(text2, output)
    else:
        output = extract_sections(text1, output)

    filter_employments_educations(output)

    return output, raw_output
