#!/usr/bin/env python3

from package.SocketServer.Request.Request import Request
from package.SocketServer.ServerError import ServerError
from package.SocketServer.Status import Status


class ReloadRequest(Request):
    api = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def solve(self):
        if not ReloadRequest.api:
            raise ServerError(Status.INTERNAL_ERROR)
        ReloadRequest.api(self.container_id)

    @staticmethod
    def bind(api):
        ReloadRequest.api = api

    def __str__(self):
        return super().__str__("Reload")
