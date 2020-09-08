from socket import *
from threading import Thread

SOCKET_SERVER_PORT = 25000


def fib(n):
    if n <= 2:
        return 1
    else:
        return fib(n-1) + fib(n-2)


def fib_handler(client):
    while True:
        req = client.recv(100)
        if not req:
            break
        n = int(req)
        try:
            result = fib(n)
        except RecursionError:
            result = 0
        resp = str(result).encode('ascii') + b'\n'
        client.send(resp)
        print("Closed")


def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    print(f"Socket server started at {SOCKET_SERVER_PORT}")

    while True:
        try:
            client, addr = sock.accept()
            print("Connected {}".format(addr))
            Thread(target=fib_handler, args=(client, ), daemon=True).start()
        except KeyboardInterrupt:
            print('Goodbye')
            break


fib_server(('', SOCKET_SERVER_PORT))
