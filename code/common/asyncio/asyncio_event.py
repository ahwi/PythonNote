from selectors import DefaultSelector, EVENT_WRITE
import socket

selector = DefaultSelector()

# sock = socket.socket()
# sock.setblocking(False)
# try:
#     sock.connect(('www.baidu.com', 80))
# except BlockingIOError:
#     pass
#
#
# def connected():
#     selector.unregister(sock.fileno())
#     print('connected!')
#
#
# selector.register(sock.fileno(), EVENT_WRITE, connected)



class Future:
    def __init__(self):
        self.result = None
        self._callbacks = []

    def add_done_callback(self, fn):
        self._callbacks.append(fn)

    def set_result(self, result):
        self.result = result
        for callback in self._callbacks:
            callback(self)


class AsyncRequest:
    def __init__(self, host, url, port, timeout=5):
        self.sock = socket.socket()
        self.sock.settimeout(timeout)
        self.sock.setblocking(False)
        self.host = host
        self.url = url
        self.port = port
        self.method = None

    def get(self):
        self.method = 'GET'
        self.request = '{} {} HTTP/1.0\r\nHost: {}\r\n\r\n'.format(self.method, self.url, self.host)
        return self

    def process(self):
        if self.method is None:
            self.get()
        try:
            self.sock.connect((self.host, self.port))
        except BlockingIOError:
            pass
        self.f = Future()
        selector.register(self.sock.fileno(),
                      EVENT_WRITE,
                      self.on_connected)
        yield self.f
        selector.unregister(self.sock.fileno())

        self.sock.send(self.request.encode('ascii'))

        chunk = yield from read_all(self.sock)
        return chunk

    def on_connected(self, key, mask):
        self.f.set_result(None)


class Task(Future):
    def __init__(self, coro):
        super().__init__()
        self.coro = coro
        f = Future()
        f.set_result(None)
        self.step(f)

    def step(self, future):
        try:
            next_future = self.coro.send(future.result)
            if next_future is None:
                return
        except StopIteration as exc:
            self.set_result(exc.value)
            return
        next_future.add_done_callback(self.step)


class EventLoop:
    stopped = False
    select_timeout = 5

    def run_until_complete(self, coros):
        tasks = [Task(coro) for coro in coros]
        try:
            self.run_forever()
        except StopError:
            pass

    def run_forever(self):
        while not self.stopped:
            events = selector.select(self.select_timeout)
            if not events:
                raise SelectTimeout('轮询超时')
            for event_key, event_mask in events:
                callback = event_key.data
                callback(event_key, event_mask)

    def close(self):
        self.stopped = True


def fetch(url):
    request = AsyncRequest('www.baidu.com', url, 80)
    data = yield from request.process()
    return data

def get_page(url):
    page = yield from fetch(url)
    return page

def async_way():
    ev_loop = get_event_loop()
    ev_loop.run_until_complete([
        get_page('/s?wd={}'.format(i)) for i in range(100)
    ])

from time import time
start = time()

async_way() # Cost 3.534296989440918 seconds

end = time()
print ('Cost {} seconds'.format(end - start))