#!/usr/bin/env python3

from package.SocketServer.Request.Request import Request
from package.SocketServer.ServerError import ServerError
from package.SocketServer.Status import Status


class ReloadRequest(Request):
    api = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def solve(self, done):
        if not ReloadRequest.api:
            raise ServerError(
                Status.INTERNAL_ERROR,
                self.request_id,
                self.container_id,
                "API not bound",
            )
        return ReloadRequest.api(self.container_id, done)

    @staticmethod
    def bind(api):
        if ReloadRequest.api == None:
            ReloadRequest.api = api
        else:
            raise Exception("[ReloadRequest] API is bound already")

    def __str__(self):
        return super().__str__("Reload")
