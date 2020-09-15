from socket import *
from collections import deque
from select import select

SOCKET_SERVER_PORT = 25000

tasks = deque()
recv_wait = {}
send_wait = {}


def fib(n):
    """
    Just an example worker, could be anything CPU and time consuming
    :param n:
    :return: recursive fibonacci value
    """
    if n <= 2:
        return 1
    else:
        return fib(n-1) + fib(n-2)


def run():
    """
    runner for tasks based on select, should run infinitely
    :return: None
    """
    while any([tasks, recv_wait, send_wait]):
        while not tasks:
            # awaiting for I/O
            can_recv, can_send, [] = select(recv_wait, send_wait, [])
            for s in can_recv:
                tasks.append(recv_wait.pop(s))
            for s in can_send:
                tasks.append(send_wait.pop(s))

        task = tasks.popleft()
        try:
            why, what = next(task) # run to yield
            if why == 'recv':
                recv_wait[what] = task
            elif why == 'send':
                send_wait[what] = task
            else:
                raise RuntimeError('Brraaah!')
        except StopIteration:
            print('task done')


def fib_server(address):
    """
    Simple socket server
    :param address: listening address
    :return: None
    """
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    print(f"Socket server started at {SOCKET_SERVER_PORT}")
    while True:
        yield 'recv', sock
        client, addr = sock.accept()
        print("Connected {}".format(addr))
        tasks.append(fib_handler(client))


def fib_handler(client):
    """
    Simple handler of tasks, uses simple function and generator based.
    :param client:
    :return: None
    """
    while True:
        yield 'recv', client
        req = client.recv(100)
        if not req:
            break
        n = int(req)
        result = fib(n)
        resp = str(result).encode('ascii') + b'\n'
        yield 'send', client
        client.send(resp)
    print("Closed")


tasks.append(fib_server(('', SOCKET_SERVER_PORT)))
run()
