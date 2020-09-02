from package.Server.Request.Request import Request
from package.Server.ServerError import ServerError, ServerErrorType


class ReturnRequest(Request):
    api = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def solve(self):
        if not api:
            raise ServerError(ServerErrorType.INTERNAL_ERROR)
        ReturnRequest.api(self.container_id)

    def bind(self, api):
        ReturnRequest.api = api

    def __str__(self):
        return super().__str__("Return")
