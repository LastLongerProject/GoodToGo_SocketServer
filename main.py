#!/usr/bin/env python3

import sys

from package.Config import CONFIG
from package.Proxy import Proxy
from package.Api.API import Api
from package.SocketServer.Server import SocketServer


try:
    api_service = Api()
    api_service.setAuthorization(**CONFIG["api"]["key"])
    api_service.setVersion(CONFIG["api"]["version"])

    proxy = Proxy(api_service)

    socket_server = SocketServer(**CONFIG["server"])
    socket_server.start(proxy)
except (SystemExit, KeyboardInterrupt):
    socket_server.close()
    print("[BYE] Exiting....")
    sys.exit(0)
