from enum import Enum


class CacheDuration(Enum):
    ONE_HOUR = 3600
    ONE_DAY = 3600 * 24
    ONE_MONTH = 3600 * 24 * 30


class StatusCode(Enum):
    HTTP_200_OK = 200
    HTTP_201_CREATED = 201
    HTTP_400_BAD_REQUEST = 400
    HTTP_404_NOT_FOUND = 404


class EntityType(Enum):
    EDUCATION = 'education'
    EMPLOYMENT = 'employment'


class Tag(Enum):
    DEGREE = 'DEGREE'
    DESIGNATION = 'DESIGNATION'
    START_DATE = 'START_DATE'
    END_DATE = 'END_DATE'
    ORGANIZATION = 'ORG'


CACHE_CONFIG = {
    "DEBUG": False,
    "CACHE_TYPE": "redis",
    "CACHE_DEFAULT_TIMEOUT": CacheDuration.ONE_HOUR
}

LOG_PATH = 'logs/cv_parse.log'
LOGGER_NAME = "Debug Rotating Logs"
MAX_BYTES_LOG = 1024 * 1024 * 10
