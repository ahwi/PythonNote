

def get_url():
    data = "bbbb"
    print("url:before")
    import time
    time.sleep(10)
    ret = yield "aaaa"
    print("url:after")
    return data


def get_page():
    print("page:before")
    data = yield from get_url()
    print(f"page:after {data}")
    return data


def sync_way():
    import socket
    for i in range(10):
        sock = socket.socket()
        sock.connect(('www.baidu.com', 80))
        print('connected')
        request = 'GET {} HTTP/1.0\r\nHost: www.baidu.com\r\n\r\n'.format('/s?wd={}'.format(i))
        sock.send(request.encode('ascii'))
        response = b''
        chunk = sock.recv(4096)
        while chunk:
            response += chunk
            chunk = sock.recv(4096)
            print(chunk)
        print('done!!')




def main():
    a = [get_page() for i in range(0, 10)]
    b = [row.send(None) for row in a]
    # c = [row.send(None) for row in a]
    print("aaaa")

    # sync_way()

if __name__ == '__main__':
    main()

