#!/usr/bin/env python3

from package.SocketServer.Request.ReloadRequest import ReloadRequest
from package.SocketServer.Request.ReturnRequest import ReturnRequest
from package.SocketServer.Response import Response
from package.SocketServer.Status import Status
from package.Throttle import Throttle
from package.Api.API import ContainerActionReply


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
        if response == ContainerActionReply.SUCCESS:
            done(Response(request.request_id, request.container_id, Status.SUCCESS))
        elif (
            response == ContainerActionReply.CONTAINER_NOT_AVAILABLE
            or response == ContainerActionReply.CONTAINER_NOT_FOUND
        ):
            done(
                Response(
                    request.request_id, request.container_id, Status.CONTAINER_NOT_FOUND
                )
            )
        elif response == ContainerActionReply.CONTAINER_STATE_ERROR:
            done(
                Response(
                    request.request_id,
                    request.container_id,
                    Status.CONTAINER_STATE_ERROR,
                )
            )
        elif response == ContainerActionReply.UNKNOWN_ERROR:
            done(Response(request.request_id, request.container_id, Status.API_FAIL))


def serializeCallback(first, last):
    return lambda *args, **kwargs: last(first(*args, **kwargs))