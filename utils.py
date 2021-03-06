import logging
from logging.handlers import RotatingFileHandler

from collections import deque
from constants import EntityType, Tag, LOG_PATH, LOGGER_NAME, MAX_BYTES_LOG


def get_dates(date_of_attendance):
    start_date = date_of_attendance.get('StartDate', {})
    end_date = date_of_attendance.get('EndDate', {})
    return start_date.get('Year', start_date.get('YearMonth')), end_date.get('Year', end_date.get('YearMonth'))


def doEntityOverlap(entities, entity):
    ent_set = set(range(entity[0], entity[1]))
    for ent in entities:
        if (ent_set.intersection(range(ent[0], ent[1]))):
            return True
    return False


def label_entity(comment, entities, field, label):
    if field:
        index = comment.find(field)
        if index != -1:
            entity = (index, index + len(field), label)
            if not doEntityOverlap(entities, entity):
                entities.append(entity)


def merge_education(updated_education, tagged_education):
    updated_education['org'] = updated_education['org'] \
        if updated_education['org'] else ' '.join(tagged_education.get('ORG', []))
    updated_education['start_date'] = ' '.join(tagged_education['START_DATE']) \
        if 'START_DATE' in tagged_education else updated_education.get('start_date', '')
    updated_education['end_date'] = ' '.join(tagged_education['END_DATE']) \
        if 'END_DATE' in tagged_education else updated_education.get('end_date', '')


def get_education_employment_keys(cv_data):
    education_key = EntityType.EDUCATION
    employment_key = EntityType.EMPLOYMENT
    for key, _ in cv_data.items():
        if 'education' in key:
            education_key = key
        if 'employment' in key:
            employment_key = key
    return education_key, employment_key


def get_root(head):
    root = head
    while root.dep_ != 'ROOT':
        root = root.head
    return root


def tag_entity(entity_type, entities, tagged_entities):
    for ent in entities:
        entity = { 'org': ent.text }

        head = get_root(ent.root.head)

        nodes = deque(head.children)
        nodes.appendleft(head)
        while nodes:
            node = nodes.popleft()
            if entity_type == EntityType.EDUCATION and node.ent_type_ == Tag.DEGREE.value:
                entity['degree'] = node.text
            if entity_type == EntityType.EMPLOYMENT and node.ent_type_ == Tag.DESIGNATION.value:
                entity['designation'] = node.text
            if node.ent_type_ in [Tag.START_DATE.value, Tag.END_DATE.value]:
                entity[node.ent_type_.lower()] = node.text

            nodes += node.children
        tagged_entities.append(entity)


def get_logger(debug=False):
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)
    if debug:
        logger.setLevel(logging.DEBUG)

    handler = RotatingFileHandler(LOG_PATH, maxBytes=MAX_BYTES_LOG)
    logger.addHandler(handler)

    return logger
