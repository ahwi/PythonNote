from time import time
import socket
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ

selector = DefaultSelector()


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

    # def __iter__(self):
    #     """ 让 Future 对象支持 yield from"""
    #     yield self  # 产出自己


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


class StopError(BaseException):
    """Raised to stop the event loop."""


class EventLoop:
    stopped = False
    select_timeout = 5

    def run_until_complete(self, coros):
        tasks = [Task(coro) for coro in coros]
        try:
            self.run_forever()
            pass
        except StopError:
            pass
        except OSError:
            pass

    def run_forever(self):
        while not self.stopped:
            events = selector.select(self.select_timeout)
            if not events:
                # raise SelectTimeout('轮询超时')
                pass
            for event_key, event_mask in events:
                callback = event_key.data
                # print(f"##### {callback}")
                # callback(event_key, event_mask)
                callback()

    def close(self):
        self.stopped = True


def read(sock):
    f = Future()

    def on_readable():
    # def on_readable(key, mask):
        f.set_result(sock.recv(4096))

    selector.register(sock.fileno(), EVENT_READ, on_readable)
    chunk = yield f  # Read one chunk.
    selector.unregister(sock.fileno())
    return chunk


def read_all(sock):
    response = []
    # Read whole response.
    chunk = yield from read(sock)
    while chunk:
        response.append(chunk)
        chunk = yield from read(sock)

    return b''.join(response)


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
        self.method = "GET"
        self.request = '{} {} HTTP/1.0\r\nHost: {}\r\n\r\n'.format(self.method, self.url, self.host)
        return self

    def process(self):
        if self.method is None:
            self.get()

        self.f = Future()
        try:
            self.sock.connect((self.host, self.port))
        except BlockingIOError:
            pass

        # import time
        # time.sleep(10)
        selector.register(self.sock.fileno(),
                          EVENT_WRITE,
                          self.on_connect)

        yield self.f
        selector.unregister(self.sock.fileno())
        self.sock.send(self.request.encode('ascii'))

        chunk = yield from read_all(self.sock)
        return chunk

    # def on_connect(self, key, mask):
    def on_connect(self):
        # selector.unregister(self.sock.fileno())
        self.f.set_result(None)



def fetch(url):
    request = AsyncRequest('www.baidu.com', url, 80)
    data = yield from request.process()
    return data


def get_page(url):
    page = yield from fetch(url)
    # print(f"page:{page}")
    return page


def async_way():
    ev_loop = EventLoop()
    ev_loop.run_until_complete([
        get_page('/s?wd={}'.format(i)) for i in range(100)
        # get_page('/s?wd={0}')
    ])


def main():
    start = time()
    async_way()
    end = time()
    print(f"Cost {end-start} seconds")


if __name__ == '__main__':
    main()