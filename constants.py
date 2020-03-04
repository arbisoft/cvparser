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


CACHE_CONFIG = {
    "DEBUG": False,
    "CACHE_TYPE": "redis",
    "CACHE_DEFAULT_TIMEOUT": CacheDuration.ONE_HOUR
}
