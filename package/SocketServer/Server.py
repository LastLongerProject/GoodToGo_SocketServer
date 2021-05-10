#!/usr/bin/env python3

import socket
import ssl
import select
import sys
from threading import *

from package.SocketServer.Request import RequestFactory, RequestError
from package.SocketServer.Response import ServerErrorParser
from package.SocketServer.ServerError import ServerError
from package.SocketServer.Status import Status
from package.RequestHandler import RequestHandler


def logHeaderGenerater(connection_id):
    return {
        "ERR": "[ERR_{connection_id}] ".format(connection_id=connection_id),
        "LOG": "[LOG_{connection_id}] ".format(connection_id=connection_id),
        "STR": "[STR_{connection_id}] ".format(connection_id=connection_id),
        "REQ": "[REQ_{connection_id}] ".format(connection_id=connection_id),
        "RES": "[RES_{connection_id}] ".format(connection_id=connection_id),
        "END": "[END_{connection_id}] ".format(connection_id=connection_id),
    }


class SocketServer:
    def __init__(self, cert, recv=1024, port=7000, listen=5):
        self.recv = recv
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert[0], cert[1])
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setblocking(0)
        sock.bind(("", port))
        sock.listen(listen)
        ssock = context.wrap_socket(sock, server_side=True)
        print("[STR_SOC] Socket server Listening on port " + str(port))
        self.sock = ssock
        self.input = [ssock]
        self.logHeaderPool = {}

    def start(self):
        while True:
            try:
                readable, _, exceptional = select.select(self.input, [], self.input)
                for sck in readable:
                    if sck is self.sock:
                        (connection, address) = sck.accept()
                        print("[SOC_SOC] ", connection, address)
                        connection_id = connection.fileno()
                        log_header = logHeaderGenerater(connection_id)
                        self.logHeaderPool[connection] = log_header
                        print(log_header["STR"] + "Connection created by client")
                        connection.setblocking(0)
                        self.input.append(connection)
                    else:
                        self.handle(sck)
                for sck in exceptional:
                    log_header = self.logHeaderPool[sck]
                    print(log_header["END"] + "Connection closed by Error")
                    self.closeConnection(sck)
            except ssl.SSLError:
                print("[END_???] Connection closed by NoneSSL")
            except ConnectionResetError:
                print("[END_???] Connection reset by peer")
            except (SystemExit, KeyboardInterrupt):
                self.close()
                break
        raise SystemExit

    def close(self):
        if self.sock:
            print("[END_SOC] Server closed")
            self.sock.close()
            self.sock = None

    def closeConnection(self, connection):
        self.input.remove(connection)
        connection.close()
        del self.logHeaderPool[connection]

    def handle(self, connection):
        log_header = self.logHeaderPool[connection]
        try:
            req = connection.recv(self.recv)
            if len(req) == 0:
                print(log_header["END"] + "Connection closed by client")
                self.closeConnection(connection)
            elif str.strip(req.decode("utf8")) == "PING":
                connection.send("PONG\r\n".encode("utf8"))
            else:
                msg = str.strip(req.decode("utf8"))
                print(log_header["REQ"] + msg)
                request = RequestFactory.create(msg)
                decoded = str(request)
                print(log_header["LOG"] + decoded)

                def doneRequest(response):
                    decoded = str(response)
                    print(log_header["LOG"] + decoded)
                    reply = response.end() + "\r\n"
                    print(log_header["RES"] + str.strip(reply))
                    connection.send(reply.encode("utf8"))

                RequestHandler.solve(request, doneRequest)
        except ServerError as error:
            print(log_header["ERR"] + error.message)
            response = ServerErrorParser(error)
            reply = response.end() + "\r\n"
            print(log_header["RES"] + str.strip(reply))
            connection.send(reply.encode("utf8"))
        except UnicodeDecodeError:
            print(log_header["ERR"] + "Unsupported encoding")
            error = ServerError(Status.REQ_FORMAT_INVALID)
            response = ServerErrorParser(error)
            reply = response.end() + "\r\n"
            print(log_header["RES"] + str.strip(reply))
            connection.send(reply.encode("utf8"))
        except ConnectionResetError:
            print(log_header["END"] + "Connection closed by client")
            self.closeConnection(connection)
