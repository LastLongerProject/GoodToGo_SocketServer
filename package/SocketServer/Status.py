from enum import Enum


class Status(Enum):
    SUCCESS = 1
    REQ_FORMAT_INVALID = 101
    REQ_ENCODING_INVALID = 102
    CONTAINER_NOT_FOUND = 201
    CONTAINER_STATE_ERROR = 202
    API_FAIL = 400
    INTERNAL_ERROR = 998
    UNKNOWN_ERROR = 999

    def __str__(self):
        return format(self.value, "03d")
