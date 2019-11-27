# ftp

## 代码:

myftp.py

```python
# -*- coding : UTF-8 -*-
from ftplib import FTP, error_reply, parse150
import sys
import os
from common.logger import Logger
import socket
from socket import _GLOBAL_DEFAULT_TIMEOUT


class SubFtp(FTP):
    """
    继承FTP类，主要实现:被动模式，服务器发送错误的ip地址的情况下，使用服务器的ip地址来连接
    """
    def ntransfercmd(self, cmd, rest=None):
        """Initiate a transfer over the data connection.

        If the transfer is active, send a port command and the
        transfer command, and accept the connection.  If the server is
        passive, send a pasv command, connect to it, and start the
        transfer command.  Either way, return the socket for the
        connection and the expected size of the transfer.  The
        expected size may be None if it could not be determined.

        Optional `rest' argument can be a string that is sent as the
        argument to a REST command.  This is essentially a server
        marker used to tell the server to skip over any data up to the
        given marker.
        """
        size = None
        if self.passiveserver:
            host, port = self.makepasv()
            try:
                conn = socket.create_connection((host, port), self.timeout,
                                                source_address=self.source_address)
            except Exception as e:
                print(f"[SubFtp]:connect {host} {port} error,"
                      f"use host ip replace {self.host}.exception info:{e}")
                conn = socket.create_connection((self.host, port), self.timeout,
                                                source_address=self.source_address)
            try:
                if rest is not None:
                    self.sendcmd("REST %s" % rest)
                resp = self.sendcmd(cmd)
                # Some servers apparently send a 200 reply to
                # a LIST or STOR command, before the 150 reply
                # (and way before the 226 reply). This seems to
                # be in violation of the protocol (which only allows
                # 1xx or error messages for LIST), so we just discard
                # this response.
                if resp[0] == '2':
                    resp = self.getresp()
                if resp[0] != '1':
                    raise error_reply(resp)
            except:
                conn.close()
                raise
        else:
            with self.makeport() as sock:
                if rest is not None:
                    self.sendcmd("REST %s" % rest)
                resp = self.sendcmd(cmd)
                # See above.
                if resp[0] == '2':
                    resp = self.getresp()
                if resp[0] != '1':
                    raise error_reply(resp)
                conn, sockaddr = sock.accept()
                if self.timeout is not _GLOBAL_DEFAULT_TIMEOUT:
                    conn.settimeout(self.timeout)
        if resp[:3] == '150':
            # this is conditional in case we received a 125
            size = parse150(resp)
        return conn, size



class MyFTP:
    """
    conncet to FTP Server
    """
    def __init__(self):
        self.logger = Logger.get_logger(name="MyFTP")
        self.f = None

    def connect(self, host, port,
            username, passwd, timeout=500):
        try:
            self.logger.debug(
                    f"ftp info:"
                    f"\nhost:{host}"
                    f"\nport:{port}"
                    f"\nusername:{username}"
                    # f"\npassword:{passwd}"
                    )
            # self.f = FTP()
            self.f = SubFtp()
            self.f.connect(host=host, port=port, timeout=500)
            self.f.login(user=username, passwd=passwd)
            self.f.set_debuglevel(1)
            self.f.set_pasv(True)
        except Exception as e:
            raise ValueError(f"connect ftp excepiton:{e}")

    def download(self, local_file, remote_file):
        try:
            # self.set_pasv(0)
            remote = os.path.split(remote_file)
            try:
                self.f.cwd(remote[0])
                remote_file = remote[1]
                fsize = self.f.size(remote_file)
                if fsize == 0:
                    self.logger.info(
                            f"remote file:{remote_file} "
                            f"size is zero")
                    return
            except Exception as e:
                raise ValueError(
                        f"remote file[{remote_file}] "
                        f"is not exist")
            lsize = 0
            if os.path.exists(local_file):
                lsize = os.stat(local_file).st_size

            if lsize == fsize:
                self.logger.debug(
                        f"local filesize is equal remote file")
            elif lsize > fsize:
                raise ValueError(
                        f"local filesize is more "
                        f"than remote file")
            block_size = 1024 * 1024
            cmpsize = lsize
            self.f.voidcmd("TYPE I")
            conn = self.f.transfercmd("RETR " + remote_file, lsize)
            lwrite = open(local_file, 'ab')
            while True:
                data = conn.recv(block_size)
                if not data:
                    break
                lwrite.write(data)
                cmpsize += len(data)
                # self.logger.debug(
                #         "download process:%.2f%%" %
                #         (float(cmpsize) / fsize * 100))
            lwrite.close()
            self.f.voidcmd("NOOP")
            self.f.voidresp()
            conn.close()
            # self.f.quit()
        except Exception as e:
            raise ValueError(
                    f"download:remote[{remote_file}] "
                    f"local_file:{local_file} "
                    f"exception:{e}")

        
    def upload(self, local_file, remote_file, 
            print_process=False, callback=None):
        self.logger.debug(
                f"upload:local file:{local_file}"
                f"remote file:{remote_file}")
        try:
            remote = os.path.split(remote_file)
            self.f.cwd(remote[0])
            
            # determine if the file exists
            try:
                rsize = self.f.size(remote[1])
            except:
                rsize = -1
                pass
            lsize = os.stat(local_file).st_size

            if rsize == lsize:
                self.logger.info(
                        "remote filesize is equal "
                        "with local file")
                return
            if rsize != -1:
                raise ValueError(
                        f"remote file is exists and "
                        f"no equal local file remote "
                        f"file:{remote_file}")

            trfile = remote[1] + ".transfer" # temp transfer file
            rsize = 0
            try:
                # rsize = self.f(remote[1])
                rsize = self.f.size(trfile)
            except:
                pass
            if rsize == None:
                rsize = 0

            if rsize > lsize:
                raise ValueError(
                        "remote filesize is more than "
                        "the local filesize")
            localf = open(local_file, 'rb')
            localf.seek(rsize)
            self.f.voidcmd('TYPE I')
            datasock = ''
            esize = ''
            try:
                # self.logger.debug(f"{remote[1]}")
                # datasock, esize = self.f.ntransfercmd(
                #         "STOR " + remote[1], rsize)
                datasock, esize = self.f.ntransfercmd(
                        "STOR " + trfile, rsize)
            except Exception as e:
                raise ValueError(f"excute ntransfercmd exception:{e}")
            cmpsize = rsize
            block_size = 1024 * 1024
            while True:
                buf = localf.read(block_size)
                if not len(buf):
                    # self.logger(f"no data break")
                    break
                datasock.sendall(buf)
                if callback:
                    callback(buf)
                cmpsize += len(buf)
                if print_process:
                    self.logger.debug(
                            "uploading %.2f%%" % 
                            (float(cmpsize) / lsize * 100))
                if cmpsize == lsize:
                    # self.logger.debug(f"file size equal break")
                    break
            # close data handle
            datasock.close()
            # close local file handle
            localf.close()
            # keep alive cmd success
            self.f.voidcmd("NOOP")
            self.f.voidresp()
            toname = remote_file
            # self.logger.debug(
            #         f"fromname:{trfile} toname:{remote[1]}")
            self.f.rename(fromname=trfile, toname=remote[1])
            # self.f.quit()
        except Exception as e:
            raise ValueError(f"upload file: "
                    f"local:{local_file} remote:{remote_file} "
                    f"exception:{e}")


def test_ftp():
    from ftplib import FTP
    host = "xx.xx.xxx.xx"
    user = "user"
    password = "12345"
    port = 21
    f = FTP()
    f.connect(host=host, port=port, timeout=500)
    f.login(user=user, passwd=password )
    ret = f.cwd('/')
    f.retrlines('LIST')
    # print(str(ret).encode("utf-8"))
    size = f.size("1.txt")
    print(f"size:{size}")


def test_class():
    f = MyFTP()
    host = "xx.xx.xxx.xx"
    user = "user"
    password = "12345"
    port = 21
    f.ConnectFTP(
        remoteip=host, remoteport=port,
        loginname=user, loginpassword=password)


if __name__ == "__main__":
    test_ftp()
    # test_class()
```







## 参考

1. windows开启ftp服务:

   <https://blog.csdn.net/pengpengpeng85/article/details/84977436>

2. ftplib断点续传:

   <https://my.oschina.net/liangzi1210/blog/160151?p=1>

3. ftp被动模式和主动模式测试:

   <https://www.xin3721.com/Python/python15261.html>