import socket
def sync_way():
    for i in range(100):
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
        print('done!!')

from time import time
start = time()

sync_way()  #Cost 47.757508993148804 seconds

end = time()
print ('Cost {} seconds'.format(end - start))
