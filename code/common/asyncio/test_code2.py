from selectors import DefaultSelector, EVENT_WRITE
import socket
import select

selector = DefaultSelector()
# selector = select.select()

sock = socket.socket()
sock.setblocking(False)
try:
    sock.connect(('www.baidu.com', 80))
except BlockingIOError as e:
    print(e)


def connected():
    selector.unregister(sock.fileno())
    print('connected!')
    request = 'GET {} HTTP/1.0\r\nHost: www.baidu.com\r\n\r\n'.format('/s?wd={}'.format(0))
    r = sock.send(request.encode('ascii'))
    print(r)


if __name__ == '__main__':
    selector.register(sock.fileno(), EVENT_WRITE, connected)
    while True:
        events = selector.select()
        for event_key, event_mask in events:
            callback = event_key.data
            callback()
