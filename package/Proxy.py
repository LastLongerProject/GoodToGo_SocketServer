#!/usr/bin/env python3

from package.SocketServer.Request.ReloadRequest import ReloadRequest
from package.SocketServer.Request.ReturnRequest import ReturnRequest
from package.SocketServer.Response import Response
from package.SocketServer.Status import Status


class Proxy:
    def __init__(self, api):
        ReturnRequest.bind(api.returnContainer)
        ReloadRequest.bind(api.reloadContainer)

    def solve(self, request):
        if isinstance(request, ReturnRequest) or isinstance(request, ReloadRequest):
            api_result = request.solve()
            if api_result == 200:
                return Response(
                    request.request_id, request.container_id, Status.SUCCESS
                )
            else:
                return Response(
                    request.request_id, request.container_id, Status.API_FAIL
                )
        else:
            return Response(
                request.request_id, request.container_id, Status.INTERNAL_ERROR
            )
