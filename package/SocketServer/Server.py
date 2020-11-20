#!/usr/bin/env python3

import socket
import sys
from threading import *

from package.SocketServer.Request import RequestFactory, RequestError
from package.SocketServer.ServerError import ServerError


class SocketServer:
    def __init__(self, recv=1024, port=7000, listen=5):
        self.recv = recv
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("", port))
        sock.listen(listen)
        print("[STR] Socket server Listening on port " + str(port))
        self.sock = sock

    def start(self):
        while True:
            connection = None
            try:
                (connection, address) = self.sock.accept()
                print("[SOC] ", connection, address)
                self.handle(connection)
                # start_new_thread(handle, (connection,))
            except (SystemExit, KeyboardInterrupt):
                if connection:
                    print("[END] Connection closed by System")
                    connection.close()
                break
        raise SystemExit

    def close(self):
        print("[END] Server closed")
        self.sock.close()

    def handle(self, connection):
        print("[STR] Connection created by client")
        while True:
            try:
                req = connection.recv(self.recv)
                if len(req) == 0:
                    break
                else:
                    msg = str.strip(req.decode("utf8"))
                    print("[REQ] " + msg)
                    request = RequestFactory.create(msg)
                    reply = str(request) + "\r\n"
                    print("[RES] " + str.strip(reply))
                    connection.send(reply.encode("utf8"))
            except RequestError as error:
                print("[ERR] " + error.message)
                reply = str(error.error_code) + "\r\n"
                # reply = str(error.error_code) + " " + error.message + "\r\n"
                connection.send(reply.encode("utf8"))
            except ServerError:
                print("[ERR] ServerError")
                reply = str(error.error_code) + "\r\n"
                connection.send(reply.encode("utf8"))
            except UnicodeDecodeError:
                print("[ERR] Unsupported encoding")
                reply = "Only support 'utf8' encoding bytes\r\n"
                connection.send(reply.encode("utf8"))
            except ConnectionResetError:
                break
        print("[END] Connection closed by client")
        connection.close()
