#!/usr/bin/env python3

from package.SocketServer.Request.Request import Request
from package.SocketServer.ServerError import ServerError
from package.SocketServer.Status import Status


class ReturnRequest(Request):
    api = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def solve(self):
        if not ReturnRequest.api:
            raise ServerError(
                Status.INTERNAL_ERROR,
                self.request_id,
                self.container_id,
                "API not bound",
            )
        return ReturnRequest.api(self.container_id)

    @staticmethod
    def bind(api):
        if ReturnRequest.api == None:
            ReturnRequest.api = api
        else
            raise Exception("[ReturnRequest] API is bound already")

    def __str__(self):
        return super().__str__("Return")
