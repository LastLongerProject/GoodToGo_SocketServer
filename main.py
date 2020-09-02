#!/usr/bin/env python3

import sys

from package.Config import CONFIG
from package.Api.API import Api
from package.Server.Server import SocketServer, socket

# ApiService = Api()
# ApiService.setAuthorization(**CONFIG["api"]["key"])
# ApiService.setVersion(CONFIG["api"]["version"])

try:
    socket_server = SocketServer(**CONFIG["server"])
    socket_server.start()
except (SystemExit, KeyboardInterrupt):
    socket_server.close()
    print("[BYE] Exiting....")
    sys.exit(0)
