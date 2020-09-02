import re

from package.Server.Request import ReloadRequest, ReturnRequest, Request


REG = re.compile("^(RTN|RLD)_\w{4}_\d{6}$")

RequestMap = {
    Request.RequestType.RELOAD.value: ReloadRequest.ReloadRequest,
    Request.RequestType.RETURN.value: ReturnRequest.ReturnRequest
}


class RequestFactory:

    @staticmethod
    def create(txt):
        if not REG.match(txt):
            raise Request.RequestError(Request.RequestErrorType.FORMAT_INVALID)
        req_type = txt[:3]
        req_id = txt[4:8]
        container_id = int(txt[9:])
        if not RequestMap[req_type]:
            raise Request.RequestError(Request.RequestErrorType.FORMAT_INVALID)
        return RequestMap[req_type](req_id, container_id)
