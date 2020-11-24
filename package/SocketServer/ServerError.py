#!/usr/bin/env python3

from package.SocketServer.Status import Status


class ServerError(Exception):
    def __init__(
        self,
        status,
        request_id="????",
        container_id="??????",
        message="Unknown Server Error",
    ):
        self.status = status
        self.request_id = request_id
        self.container_id = container_id
        self.message = status.name + " | " + message
        super().__init__(self.message)
