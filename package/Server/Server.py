#!/usr/bin/env python3

import socket
import sys
from threading import *

from package.Server.Request import Factory as RequestFactory, Request
import package.Server.ServerError


class SocketServer:

    def __init__(self, recv=1024, port=7000, listen=5):
        self.recv = recv
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', port))
        sock.listen(listen)
        print("[LOG]_[STR] Socket server Listening on port " + str(port))
        self.sock = sock

    def start(self):
        while True:
            connection = None
            try:
                (connection, address) = self.sock.accept()
                print("[LOG]_[SOC] ", connection, address)
                self.handle(connection)
                # start_new_thread(handle, (connection,))
            except (SystemExit, KeyboardInterrupt):
                if connection:
                    print("[LOG]_[CLS] Connection closed by System")
                    connection.close()
                break
        raise SystemExit

    def close(self):
        print("[LOG]_[CLS] Server closed")
        self.sock.close()

    def handle(self, connection):
        print("[LOG]_[STR] Connection created by client")
        while True:
            try:
                req = connection.recv(self.recv)
                if len(req) is 0:
                    break
                else:
                    msg = str.strip(req.decode("utf8"))
                    print("[LOG]_[REQ] " + msg)
                    request = RequestFactory.RequestFactory.create(msg)
                    reply = str(request) + "\r\n"
                    print("[LOG]_[RES] " + str.strip(reply))
                    connection.send(reply.encode("utf8"))
            except Request.RequestError as error:
                print("[LOG]_[ERR] " + error.message)
                reply = str(error.error_code) + " " + error.message + "\r\n"
                connection.send(reply.encode("utf8"))
            except UnicodeDecodeError:
                print("[LOG]_[ERR] Unsupported encoding")
                reply = "Only support 'utf8' encoding bytes\r\n"
                connection.send(reply.encode("utf8"))
            except ConnectionResetError:
                break
        print("[LOG]_[CLS] Connection closed by client")
        connection.close()
