#!/usr/bin/env python3

from package.SocketServer.Request.ReloadRequest import ReloadRequest
from package.SocketServer.Request.ReturnRequest import ReturnRequest
from package.SocketServer.Response import Response
from package.SocketServer.Status import Status
from package.Throttle import Throttle


class RequestHandler:
    @staticmethod
    def init(apiService):
        ReturnRequest.bind(Throttle(apiService.returnContainer).do)
        ReloadRequest.bind(Throttle(apiService.reloadContainer).do)

    @staticmethod
    def solve(request, done):
        if isinstance(request, ReturnRequest) or isinstance(request, ReloadRequest):
            request.solve(
                lambda response: RequestHandler.responseHandler(request, response, done)
            )
        else:
            done(
                Response(
                    request.request_id,
                    request.container_id,
                    Status.INTERNAL_ERROR,
                )
            )

    @staticmethod
    def responseHandler(request, response, done):
        if response == 200:
            done(Response(request.request_id, request.container_id, Status.SUCCESS))
        else:
            done(Response(request.request_id, request.container_id, Status.API_FAIL))


def serializeCallback(first, last):
    return lambda *args, **kwargs: last(first(*args, **kwargs))