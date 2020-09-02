#!/usr/bin/env python3

from enum import Enum


class ServerErrorType(Enum):
    INTERNAL_ERROR = 998
    UNKNOWN_ERROR = 999


class ServerError(Exception):
    def __init__(self, error_code=ServerErrorType.UNKNOWN_ERROR):
        self.error_code = error_code
        self.message = error_code.name
        super().__init__(self.message)
