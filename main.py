import json
import sys
from collections import OrderedDict
from itertools import tee

import spacy
import textract
import tika
from spacy.lang.en import English
from spacy.pipeline import EntityRuler
from spacy.tokens import Span
from tika import parser

import patterns

tika.initVM()


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


def print_debug(title, text):
    print('-' * 80)
    print('{: ^80}'.format(title))
    print('-' * 80)
    print(text)
    print('-' * 80)


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


def extract_entities(text, output={}, debug=False):
    nlp = English()
    ruler = EntityRuler(nlp)
    ruler.add_patterns(patterns.patterns + patterns.section_patterns)
    nlp.add_pipe(ruler)
    doc = nlp(text)
    if debug:
        print_debug('TOKENS', '\n'.join(['{} {}'.format(i, t.text) for i, t in enumerate(doc)]))
        print_debug('ENTITIES', '\n'.join(['{}:{}'.format(ent.label_, ent.text) for ent in doc.ents]))
    return update_output(doc, output)


def extract_sections(text, output={}, debug=False):
    nlp = English()
    ruler = EntityRuler(nlp)
    ruler.add_patterns(patterns.section_patterns)
    nlp.add_pipe(ruler)
    nlp.add_pipe(expand_sections)
    doc = nlp(text)

    if debug:
        print_debug('SESSION TOKENS', '\n'.
                    join(['{} {}'.format(i, t.text) for i, t in enumerate(doc)]))
        print_debug('SESSION ENTITIES', '\n'.
                    join(['{}:{}:{}:{}'.format(ent.label_, ent.text.strip(), ent.start, ent.end)
                        for ent in doc.ents]))
    return update_output(doc, output)


def filter_employments_educations(cv_data):
    nlp = spacy.load('en_core_web_sm')

    for education in cv_data.get('education', []):
        doc = nlp(education)
        for ent in doc.ents:
            print(ent.text, ent.start_char, ent.end_char, ent.label_)

    for experience in cv_data.get('experience', []):
        doc = nlp(experience)
        for ent in doc.ents:
            print(ent.text, ent.start_char, ent.end_char, ent.label_)


def process_file(filepath, educations, companies, debug=False):
    text1 = textract.process(filepath).decode('utf-8')
    text2 = parser.from_file(filepath)['content']

    if debug:
        print_debug('Raw Text Textract', text1)
        print_debug('Raw Test Tika', text2)

    raw_output = text1
    if len(text2) > len(text1):
        raw_output = text2

    output = OrderedDict()

    for k in ['name', 'cell', 'email', 'nic', 'skills']:
        output[k] = []
    output = extract_name(text1, output)
    output = extract_entities(text1, output, debug=debug)
    sections1 = extract_sections(text1, {})
    sections2 = extract_sections(text2, {})

    if len(sections2) >= len(sections1):
        output = extract_sections(text2, output, debug=debug)
    else:
        output = extract_sections(text1, output, debug=debug)

    filter_employments_educations(output)

    return output, raw_output
