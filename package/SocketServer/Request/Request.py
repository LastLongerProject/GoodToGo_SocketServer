#!/usr/bin/env python3

from enum import Enum
from package.SocketServer.ServerError import ServerError


class Request:
    def __init__(self, request_id, container_id):
        self.request_id = request_id
        self.container_id = container_id

    def solve(self):
        raise NotImplementedError

    def bind(self):
        raise NotImplementedError

    def __str__(self, action="Unknown Action"):
        return "REQ#{request_id}: Container #{container_id} - {action}".format(
            action=action, request_id=self.request_id, container_id=self.container_id
        )


class RequestError(ServerError):
    def __init__(
        self,
        status,
        request_id="????",
        container_id="??????",
        message="Unknown Request Error",
    ):
        super().__init__(status, request_id, container_id, message)


class RequestType(Enum):
    RETURN = "RTN"
    RELOAD = "RLD"
