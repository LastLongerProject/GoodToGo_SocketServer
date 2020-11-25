#!/usr/bin/env python3

import socket
import ssl
import sys
from threading import *

from package.SocketServer.Request import RequestFactory, RequestError
from package.SocketServer.Response import ServerErrorParser
from package.SocketServer.ServerError import ServerError
from package.SocketServer.Status import Status


class SocketServer:
    def __init__(self, cert, recv=1024, port=7000, listen=5):
        self.recv = recv
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert[0], cert[1])
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("", port))
        sock.listen(listen)
        ssock = context.wrap_socket(sock, server_side=True)
        print("[STR] Socket server Listening on port " + str(port))
        self.sock = ssock

    def start(self, proxy):
        self.proxy = proxy
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
                elif str.strip(req.decode("utf8")) == "PING":
                    connection.send("PONG".encode("utf8"))
                else:
                    msg = str.strip(req.decode("utf8"))
                    print("[REQ] " + msg)
                    request = RequestFactory.create(msg)
                    decoded = str(request)
                    print("[LOG] " + decoded)
                    response = self.proxy.solve(request)
                    reply = response.end() + "\r\n"
                    print("[RES] " + str.strip(reply))
                    connection.send(reply.encode("utf8"))
            except ServerError as error:
                print("[ERR] " + error.message)
                response = ServerErrorParser(error)
                reply = response.end() + "\r\n"
                print("[RES] " + str.strip(reply))
                connection.send(reply.encode("utf8"))
            except UnicodeDecodeError:
                print("[ERR] Unsupported encoding")
                reply = "Only support 'utf8' encoding bytes\r\n"  # TODO
                error = ServerError(Status.REQ_FORMAT_INVALID)
                response = ServerErrorParser(error)
                reply = response.end() + "\r\n"
                print("[RES] " + str.strip(reply))
                connection.send(reply.encode("utf8"))
            except ConnectionResetError:
                break
        print("[END] Connection closed by client")
        connection.close()
