#!/usr/bin/env python3

import package.Api.API
from package.SocketServer.Request.ReloadRequest import ReloadRequest
from package.SocketServer.Request.ReturnRequest import ReturnRequest
from package.SocketServer.Response import Response
from package.SocketServer.Status import Status


class Proxy:
    def __init__(self):
        ReturnRequest.bind(None)
        ReloadRequest.bind(None)

    def solve(self, request):
        if isinstance(request, ReturnRequest) or isinstance(request, ReloadRequest):
            api_result = request.solve()
            return Response(request.req_id, request.container_id, Status.SUCCESS)
        else:
            return Response(request.req_id, request.container_id, Status.INTERNAL_ERROR)
