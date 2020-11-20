#!/usr/bin/env python3

from enum import Enum


class Request:

    def __init__(self, req_id, container_id):
        self.req_id = req_id
        self.container_id = container_id

    def solve(self):
        raise NotImplementedError

    def bind(self):
        raise NotImplementedError

    def __str__(self, action):
        return "REQ#{req_id}: {action} Container #{container_id}".format(action=action, req_id=self.req_id, container_id=self.container_id)


class RequestError(Exception):
    def __init__(self, error_code, message="Unknown Request Error"):
        self.error_code = error_code
        self.message = error_code.name
        super().__init__(self.message)


class RequestType(Enum):
    RETURN = "RTN"
    RELOAD = "RLD"


class RequestErrorType(Enum):
    FORMAT_INVALID = 101
    CONTAINER_NOT_FOUND = 201
    CONTAINER_STATE_ERROR = 202
