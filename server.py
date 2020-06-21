import socket
import sys
from threading import *


def threadWork(client):
    while True:
        try:
            req = client.recv(1024)
            if len(req) is 0:
                break
            else:
                msg = req.decode("utf8")
                print("Client send: " + msg)
                reply = "You say: " + msg
                client.send(reply.encode("utf8"))
        except UnicodeDecodeError:
            print("Unsupported encoding")
            reply = "Only support 'utf8' encoding bytes\r\n"
            client.send(reply.encode("utf8"))
        except KeyboardInterrupt:
            break
    client.close()


try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
    sys.stderr.write("[ERROR] %s\n" % msg)
    sys.exit(1)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', 7000))
sock.listen(5)

while True:
    try:
        (csock, adr) = sock.accept()
        print("Client Info: ", csock, adr)
        threadWork(csock)
        # start_new_thread(threadWork, (csock,))
    except (SystemExit, KeyboardInterrupt):
        print("Exiting....")
        break
    except Exception as ex:
        print("======> Fatal Error....\n" + str(ex))
        raise

sock.close()
