#!/usr/bin/env python3

import sys

from package.Config import CONFIG
from package.RequestHandler import RequestHandler
from package.Api.API import Api
from package.SocketServer.Server import SocketServer

try:
    api_service = Api()
    api_service.setAuthorization(**CONFIG["api"]["key"])
    api_service.setVersion(CONFIG["api"]["version"])

    RequestHandler.init(api_service)

    socket_server = SocketServer(**CONFIG["server"])
    socket_server.start()
except (SystemExit, KeyboardInterrupt):
    socket_server.close()
    print("[BYE] Exiting....")
    sys.exit(0)
