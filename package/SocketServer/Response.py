#!/usr/bin/env python3

from enum import Enum

from package.SocketServer.Status import Status

class Response:
    def __init__(self, req_id, container_id, status):
        self.req_id = req_id
        self.container_id = container_id
        self.status = status

    def __str__(self):
        return "RES#{req_id}: Container #{container_id} - {status}".format(
            status=self.status, req_id=self.req_id, container_id=self.container_id
        )

    def send(self):
        return "{response_type}_{status_code}_{request_id}".format(
            response_type=self.getType(), status_code=self.status, request_id=self.request_id
        )

    def getType(self):
        if (self.status === Status.SUCCESS)
            return RequestType.SUCCESS
        else:
            return RequestType.ERROR


class ResponseError(Exception):
    def __init__(self, error_code, message="Unknown Response Error"):
        self.error_code = error_code
        self.message = error_code.name
        super().__init__(self.message)


class RequestType(Enum):
    SUCCESS = "SUC"
    ERROR = "ERR"
