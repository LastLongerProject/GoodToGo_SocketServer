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

    def __str__(self, action="Unknown Action"):
        return "REQ#{req_id}: Container #{container_id} - {action}".format(
            action=action, req_id=self.req_id, container_id=self.container_id
        )


class RequestError(Exception):
    def __init__(self, error_code, message="Unknown Request Error"):
        self.error_code = error_code
        self.message = error_code.name
        super().__init__(self.message)


class RequestType(Enum):
    RETURN = "RTN"
    RELOAD = "RLD"
