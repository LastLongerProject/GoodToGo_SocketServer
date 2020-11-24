#!/usr/bin/env python3

from enum import Enum

from package.SocketServer.Status import Status


class Response:
    def __init__(self, request_id, container_id, status):
        self.request_id = request_id
        self.container_id = container_id
        self.status = status

    def __str__(self):
        return "RES#{request_id}: Container #{container_id} - {status}".format(
            status=self.status,
            request_id=self.request_id,
            container_id=self.container_id,
        )

    def end(self):
        return "{response_type}_{status_code}_{request_id}".format(
            response_type=self.getType().value,
            status_code=self.status,
            request_id=self.request_id,
        )

    def getType(self):
        if self.status == Status.SUCCESS:
            return RequestType.SUCCESS
        else:
            return RequestType.ERROR


def ServerErrorParser(error):
    return Response(error.request_id, error.container_id, error.status)


class RequestType(Enum):
    SUCCESS = "SUC"
    ERROR = "ERR"
