from enum import Enum


class CacheDuration(Enum):
    one_hour = 3600
    one_day = 3600 * 24
    one_month = 3600 * 24 * 30


class StatusCode(Enum):
    HTTP_200_OK = 200
    HTTP_201_CREATED = 201
    HTTP_400_BAD_REQUEST = 400
    HTTP_404_NOT_FOUND = 404

CACHE_CONFIG = {
    "DEBUG": False,
    "CACHE_TYPE": "redis",
    "CACHE_DEFAULT_TIMEOUT": CacheDuration.one_hour
}
