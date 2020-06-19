import socket
import sys
from threading import *


def threadWork(client):
    while True:
        msg = client.recv(1024)
        if not msg:
            pass
        else:
            print("Client send: " + msg)
            client.send("You say: " + msg + "\r\n")
    client.close()


try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
    sys.stderr.write("[ERROR] %s\n" % msg)
    sys.exit(1)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', 54321))
sock.listen(5)

while True:
    (csock, adr) = sock.accept()
    print("Client Info: ", csock, adr)
    threadWork(csock)
    # start_new_thread(threadWork, (csock,))

sock.close()
