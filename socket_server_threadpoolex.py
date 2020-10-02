from socket import *
from collections import deque
from select import select
#from concurrent.futures import ThreadPoolExecutor as Pool
from concurrent.futures import ProcessPoolExecutor as Pool


SOCKET_SERVER_PORT = 25000

pool = Pool(4)
tasks = deque()
recv_wait = {}
send_wait = {}
future_wait = {}


future_notify, future_event = socketpair()


def future_done(future):
    tasks.append(future_wait.pop(future))
    future_notify.send(b'x')


def future_monitor():
    while True:
        yield 'recv', future_event
        future_event.recv(100)


tasks.append(future_monitor())


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
            can_recv, can_send, _ = select(recv_wait, send_wait, []) # is actually awaiting here
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
            elif why == 'future':
                future_wait[what] = task
                what.add_done_callback(future_done)
            else:
                raise RuntimeError('Brraaah!')
        except StopIteration:
            print('task done')


class AsyncSocket:
    def __init__(self, sock):
        self.sock = sock

    def recv(self, maxsite):
        yield 'recv', self.sock
        return self.sock.recv(maxsite)

    def send(self, data):
        yield 'send', self.sock
        return self.sock.send(data)

    def accept(self):
        yield 'recv', self.sock
        client, addr = self.sock.accept()
        return AsyncSocket(client), addr

    def __getattr__(self, name):
        return getattr(self.sock, name)


def fib_server(address):
    """
    Simple socket server
    :param address: listening address
    :return: None
    """
    sock = AsyncSocket(socket(AF_INET, SOCK_STREAM))
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    print(f"Socket server started at {SOCKET_SERVER_PORT}")
    while True:
        client, addr = yield from sock.accept()
        print("Connected {}".format(addr))
        tasks.append(fib_handler(client))


def fib_handler(client):
    """
    Simple handler of tasks, uses simple function and generator based.
    :param client:
    :return: None
    """
    while True:
        req = yield from client.recv(100)
        if not req:
            break
        n = int(req)
        future = pool.submit(fib, n)
        yield 'future', future
        result = future.result()  # Blocks
        resp = str(result).encode('ascii') + b'\n'
        yield from client.send(resp)
    print("Closed")


tasks.append(fib_server(('', SOCKET_SERVER_PORT)))
run()
