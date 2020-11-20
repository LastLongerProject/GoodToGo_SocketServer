#!/usr/bin/env python3

from package.SocketServer.Status import Status


class ServerError(Exception):
    def __init__(self, error_code=Status.UNKNOWN_ERROR):
        self.error_code = error_code
        self.message = error_code.name
        super().__init__(self.message)
