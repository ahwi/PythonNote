# UTILS-----常用工具

##  SMTP--邮件发送

SMTP（Simple Mail Transfer Protocol, SMTP）是发送邮件的协议，Python内置对SMTP的支持，可以发送纯文本邮件、HTML邮件以及带附件的邮件

Python对SMTP支持有<font color=red>smtplib</font>和<font color=red>smtplib</font>两个模块：

*  **email** 负责构造邮件

* **smtplib**负责发送邮件

### 1. 构造一个简单的纯文本邮件：

```python
from email.mime.text import MIMEText
msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
```

* 构造`MIMEText`对象时：

  第一个参数就是邮件正文

  第二个参数是MIME的subtype，传入`'plain'`表示纯文本，最终的MIME就`'text/plain'`

  第三个参数表示编码，用`utf-8`编码保证多语言兼容性



### 2. 发送代码(这里以新浪为例)：

```python 
from email.mime.text import MIMEText
from email.header import Header
import smtplib

msg = MIMEText('hello, send by python...', 'plain', 'utf-8')

print(msg)
# 发件人的地址和口令
from_add = "xxx@sina.com"
password = "xxx"


# 收件人的地址：
to_add = "xxx@qq.com"
# SMTP服务器地址(新浪)：
smtp_server_sina = "smtp.sina.com"


server = smtplib.SMTP(smtp_server_sina, 25) # SMTP协议的默认端口是25
server.set_debuglevel(1)
server.login(from_add, password)
msg['From'] = Header(from_add)  # 新浪邮箱限制客户设置的邮件地址与实际发件人地址
server.sendmail(from_add, [to_add], msg.as_string())
server.quit()
```

* 说明：

  <font color=red>set_debuglevel(1)：</font> 可以打印出和SMTP服务器交互的所有信息。

  <font color=red>SMTP协议：</font>就是简单的文本命令和响应。

  <font color=red>login()：</font> 用来登录SMTP服务器

  <font color=red>sendmail()：</font> 用来发邮件，由于可以一次发给多个人，所以传入一个list

  <font color=red>as_string()：</font>邮件正文是一个str，把MIMEText对象变成str

### 3. 添加邮件主题等信息

```python
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr

import smtplib


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


# 发件人的地址和口令
from_add = "xxx"
password = "xxx"

# 收件人的地址：
to_add = "xxx"
# SMTP服务器地址(新浪)：
smtp_server_sina = "smtp.sina.com"

# 添加邮件主题等信息
msg = MIMEText('hello, send by python...', 'plain', 'utf-8')
msg['From'] = Header(from_add)  # 新浪邮箱限制客户设置的邮件地址与实际发件人地址
# msg['From'] = _format_addr('Python 爱好者 <%s>' % from_add)  # 可能是新浪的限制，添加格式邮件发送不了
msg['To'] = _format_addr('管理员 <%s>' % to_add)  # 接收的是字符串而不是list，如果有多个邮件地址，用,分隔即可
msg['Subject'] = Header('来自SMTP的问候......', 'utf-8').encode()


try:
    server = smtplib.SMTP(smtp_server_sina, 25) # SMTP协议的默认端口是25
    server.set_debuglevel(1)  # 打印出和SMTP服务器交互的所有信息
    server.login(from_add, password)
    server.sendmail(from_add, [to_add], msg.as_string())
    server.quit()
except Exception as e:
    print(e)
```

* 说明：

  我们编写了一个函数`_format_addr()`来格式化一个邮件地址。注意不能简单地传入`name <addr@example.com>`，因为如果包含中文，需要通过`Header`对象进行编码



### 4. 发送附件

要发送附件主要是定义一个MIMEMultipart对象，将原来的MIMEText附加到MIMEMultipart对象上并且附加上一个用来表示附件内容的MIMEBase对象

```python
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
from email.utils import parseaddr, formataddr

import smtplib


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


# 发件人的地址和口令
from_add = "xxx@sina.com"
password = "xxx"

# 收件人的地址：
to_add = "xxx"
# SMTP服务器地址(新浪)：
smtp_server_sina = "smtp.sina.com"

# 发送附件
msg = MIMEMultipart()
msg['From'] = Header(from_add)  # 新浪邮箱限制客户设置的邮件地址与实际发件人地址
# msg['From'] = _format_addr('Python 爱好者 <%s>' % from_add)  # 新浪邮箱限制客户设置的邮件地址与实际发件人地址
msg['To'] = _format_addr('管理员 <%s>' % to_add)  # 接收的是字符串而不是list，如果有多个邮件地址，用,分隔即可
msg['Subject'] = Header('来自SMTP的问候......', 'utf-8').encode()


# 邮件正文是MIMEText:
msg.attach(MIMEText('hello, send by python...', 'plain', 'utf-8'))

# 添加附件就是加上一个MIMEBase,从本地读取一个图片：
with open('C:\\Users\\ahwi\\Pictures\\Saved Pictures\\6e85b344ad345982c02535e501f431adcaef84f7.jpg', 'rb') as f:
    #  设置附件的MIME和文件名，这里是png类型：
    mime = MIMEBase('image', 'jpg', filename='6e85b344ad345982c02535e501f431adcaef84f7.jpg')
    # 加上必要头信息
    mime.add_header('Content-Disposition', 'attachment', filename='6e85b344ad345982c02535e501f431adcaef84f7.jpg')
    mime.add_header('Content-ID', '<0>')
    mime.add_header('X-Attachment-Id', '0')
    # 把附件的内容读进来:
    mime.set_payload(f.read())
    # 用Base64编码:
    encoders.encode_base64(mime)
    # 添加到MIMEMultipart:
    msg.attach(mime)
    try:
        server = smtplib.SMTP(smtp_server_sina, 25)  # SMTP协议的默认端口是25
        server.set_debuglevel(1)  # 打印出和SMTP服务器交互的所有信息
        server.login(from_add, password)
        server.sendmail(from_add, [to_add], msg.as_string())
        server.quit()
    except Exception as e:
        print(e)
```

### 5. 发送图片

需要将图片嵌入到正文中，可以在HTML中利用src="cid:0"引用附件就可以了。将原来的正文代码替换成如下类似代码即可

```python
msg.attach(MIMEText('<html><body><h1>Hello</h1>' +
    '<p><img src="cid:0"></p>' +
    '</body></html>', 'html', 'utf-8'))

#----------------完整代码---------------------
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
from email.utils import parseaddr, formataddr

import smtplib


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


# 发件人的地址和口令
from_add = "xxx"
password = "xxx"

# 收件人的地址：
to_add = "xxx"
# SMTP服务器地址(新浪)：
smtp_server_sina = "smtp.sina.com"


# 发送附件
msg = MIMEMultipart()
msg['From'] = Header(from_add)  # 新浪邮箱限制客户设置的邮件地址与实际发件人地址
# msg['From'] = _format_addr('Python 爱好者 <%s>' % from_add)  # 新浪邮箱限制客户设置的邮件地址与实际发件人地址
msg['To'] = _format_addr('管理员 <%s>' % to_add)  # 接收的是字符串而不是list，如果有多个邮件地址，用,分隔即可
msg['Subject'] = Header('来自SMTP的问候......', 'utf-8').encode()


# 邮件正文是MIMEText:
# msg.attach(MIMEText('hello, send by python...', 'plain', 'utf-8'))
msg.attach(MIMEText('<html><body><h1>Hello</h1>' +
    '<p><img src="cid:0"></p>' +
    '</body></html>', 'html', 'utf-8'))  # 将图片加到正文中

# 添加附件就是加上一个MIMEBase,从本地读取一个图片：
with open('C:\\Users\\ahwi\\Pictures\\Saved Pictures\\6e85b344ad345982c02535e501f431adcaef84f7.jpg', 'rb') as f:
    #  设置附件的MIME和文件名，这里是png类型：
    mime = MIMEBase('image', 'jpg', filename='6e85b344ad345982c02535e501f431adcaef84f7.jpg')
    # 加上必要头信息
    mime.add_header('Content-Disposition', 'attachment', filename='6e85b344ad345982c02535e501f431adcaef84f7.jpg')
    mime.add_header('Content-ID', '<0>')
    mime.add_header('X-Attachment-Id', '0')
    # 把附件的内容读进来:
    mime.set_payload(f.read())
    # 用Base64编码:
    encoders.encode_base64(mime)
    # 添加到MIMEMultipart:
    msg.attach(mime)
    try:
        server = smtplib.SMTP(smtp_server_sina, 25)  # SMTP协议的默认端口是25
        server.set_debuglevel(1)  # 打印出和SMTP服务器交互的所有信息
        server.login(from_add, password)
        server.sendmail(from_add, [to_add], msg.as_string())
        server.quit()
    except Exception as e:
        print(e)
```



### 6. 加密传输

使用标准的25端口连接SMTP服务器时，使用的是明文传输，发送邮件的整个过程可能会被窃听。要更安全地发送邮件，可以加密SMTP会话，实际上就是先创建SSL安全连接，然后再使用SMTP协议发送邮件。

某些邮件服务商，例如Gmail，提供的SMTP服务必须要加密传输。我们来看看如何通过Gmail提供的安全SMTP发送邮件。

必须知道，Gmail的SMTP端口是587，因此，修改代码如下：

```python
smtp_server = 'smtp.gmail.com'
smtp_port = 587
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
# 剩下的代码和前面的一模一样:
server.set_debuglevel(1)
...
```

只需要在创建`SMTP`对象后，立刻调用`starttls()`方法，就创建了安全连接。后面的代码和前面的发送邮件代码完全一样。

如果因为网络问题无法连接Gmail的SMTP服务器，请相信我们的代码是没有问题的，你需要对你的网络设置做必要的调整。



### 7. 总结

构造一个邮件对象就是一个`Messag`对象，如果构造一个`MIMEText`对象，就表示一个文本邮件对象，如果构造一个`MIMEImage`对象，就表示一个作为附件的图片，要把多个对象组合起来，就用`MIMEMultipart`对象，而`MIMEBase`可以表示任何对象。它们的继承关系如下：

```python
Message
+- MIMEBase
   +- MIMEMultipart
   +- MIMENonMultipart
      +- MIMEMessage
      +- MIMEText
      +- MIMEImage
```

这种嵌套关系就可以构造出任意复杂的邮件。你可以通过[email.mime文档](https://docs.python.org/3/library/email.mime.html)查看它们所在的包以及详细的用法。



注：本文参考廖雪峰老师的网站



##  线程池

### 1. 等待所有线程结束

```python
# -*- coding: UTF-8 -*-
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


# 模拟获取网页
def get_html(times):
    time.sleep(times)
    print(f'get page {times}s finish.')
    return times


def test_thread_pool():
    executor = ThreadPoolExecutor(max_workers=2)
    urls = [3, 2, 4, 6, 7, 8]  # 模拟数据
    i = 0
    all_task = [executor.submit(get_html, (url,)) for url in urls]

    for future in as_completed(all_task):
        data = future.result()
        print("in main: get page {}s success".format(data))


if __name__ == '__main__':
    test_thread_pool()
```

<font color=red>as_completed()</font>方法是一个生成器，在没有任务完成的时候，会阻塞，在有某个任务完成的时候，会<font color=red>yield</font>这个任务，就能执行for循环下面的语句，然后继续阻塞住，循环到所有的任务结束。从结果也可以看出，**先完成的任务会先通知主线程**。



## Paramiko(ssh2协议的实现库)

概念:

* SSHClient
* Transport
* start_server
* start_client
* channels





## 用法：

### typing 类型标注

#### Callable

 `Callable[[Arg1Type, Arg2Type], ReturnType]`





### 导入系统库（当前代码与系统的包名冲突时）

```
from __future__ import 
```



### 在多线程中，利用队列传递对象,对象是同一个吗？

思考：在c++中将对象存入到队列中，存的是一个拷贝，在python中存的是对象本身（通过打印地址得知），在两个线程（线程A和线程B）中，两个线程通过队列通讯，在线程A产生对象并通过队列传递给线程B，通过打印对象的地址得知，两个对象是同一个。

测试代码:

```python
import time
from threading import Thread
from queue import Queue

class Result:
    def __init__(self, 
            flag, pos, 
            end_pos,total, 
            percent,status):
        self.flag = flag
        self.pos = pos
        self.count = 0
        self.total = total
        self.percent = percent
        self.status = status

    def update_progress(self, pos, step):
        self.pos = pos
        self.count += step

    def progress(self):
        return self.count / self.total

    def info(self):
        ret = "flag:{flag} pos:{pos} "\
              "total:{total} percent:"\
              "{percent} status:{status}".format(
                      flag=self.flag, pos=self.pos,
                      total=self.total, percent=self.percent,
                      status=self.status)
        return ret


class Cook:
    def __init__(self):
        self.stopped = False
        self.data_q = None
        self.result_q = None

    def run(self, data_q, result_q):
        self.data_q = data_q
        self.result_q = result_q
        while not self.stopped:
            #print('running')
            item = self.data_q.get()
            print(f"cook: flag{item.flag} {item}")
            time.sleep(1)
        print('cook quit...')

    def cook_data(self):
        pass

    def save_result(self):
        pass

    def stop(self):
        self.stopped = True

class Make():
    def __init__(self):
        self.stopped = False
        self.data_q = None
        self.result_q = None

    def run(self, data_q, result_q):
        self.data_q = data_q
        self.result_q = result_q
        i = 0
        while not self.stopped:
            flag = 'task_' + str(i)
            pos = 0
            count = 0
            total = 100
            status = 0
            end_pos = 100
            percent = 0
            r = Result(flag=flag, pos=pos, 
                     end_pos=end_pos,
                     total=total, 
                     percent=percent,
                     status=status)
            print(f"make:{r.flag} address:{r}")
            self.data_q.put(r)
            time.sleep(10)
            i += 1
        print('make quit...')

    def stop(self):
        self.stopped = True



if __name__ == '__main__':
    data_q = Queue()
    result_q = Queue()
    
    # 线程B：获取数据
    cook = Cook()
    t = Thread(target=cook.run, 
            args=(data_q, result_q))
    t.start()
    
    # 线程A：产生数据
    make = Make()
    t2 = Thread(target=make.run, 
            args=(data_q, result_q))
    t2.start()

    t.join()
    t2.join()
```

运行结果:

```
make:task_0 address:<Result.Result object at 0x0000000002B3CE10>
cook: flagtask_0 <Result.Result object at 0x0000000002B3CE10>
make:task_1 address:<Result.Result object at 0x0000000002B3CE80>
cook: flagtask_1 <Result.Result object at 0x0000000002B3CE80>
```





### 回调函数

参考博客：<https://www.cnblogs.com/surehunter/p/7896298.html>

**需要回调函数的场景：** 进程池中任何一个任务一旦处理完了，就立即告知主进程：我好了额，你可以处理我的结果了。主进程则调用一个函数去处理该结果，该函数即回调函数

我们可以把耗时间（阻塞）的任务放到进程池中，然后指定回调函数（主进程负责执行），这样主进程在执行回调函数时就省去了I/O的过程，直接拿到的是任务的结果。

```python
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
import requests
import os
import time

def get(url):
    print('%s GET %s' %(os.getpid(),url))
    response=requests.get(url)
    if response.status_code == 200:
        return {'url':url,'text':response.text}

def parse(res):
    res=res.result()
    url=res['url']
    text=res['text']
    print('%s parse %s res:%s' %(os.getpid(),url,len(text)))

if __name__ == '__main__':
    urls = [
        'https://www.baidu.com',
        'https://www.python.org',
        'https://www.openstack.org',
        'https://help.github.com/',
        'http://www.sina.com.cn/'
    ]

    p=ProcessPoolExecutor()
    start=time.time()
    for url in urls:
        future=p.submit(get, url)
        future.add_done_callback(parse) #parse(futrue)
    p.shutdown(wait=True)
    print(time.time()-start) #3.1761815547943115
    print(os.getpid())
```





## 将py文件编译成exe

```
# 1. 安装pyinstaller:
	python3 -m pip install pyinstaller
# 2. 切换到代码路径下，运行命令:
$ pyinstaller -F xxx.py(xxx.py, 打包的文件)

# 3. 打包成功后新增一个dist文件，里面会有编译好的exe
```

<font color=red>注：需要把一些\_\_file\_\_的东西注释掉，如：</font>

```
        #libpath = os.path.join(os.path.dirname(__file__), libname)
        libpath = os.getcwd() + os.sep + libname
```

多进程代码需要多加:

```
if __name__=='__main__':
	# 在此处添加 支持Pyinstaller3.3以上   Pyinstaller版本低于3.3版本的话，还需要额外添加一个模块（百度）
	multiprocessing.freeze_support()
	# 这里是你的代码
	# ......
```



## 将py文件编译成so

**1. 方式1：**

参考：

`https://www.jb51.net/article/177030.htm`

代码:

```python

```

**2. 方式2**

使用`py2sec`编译脚本

参考：`https://github.com/cckuailong/py2sec`

**3. 编译遇到的问题：**

* 有个md5函数编译之前执行不会报错，编译之后报错

  ```txt
  Traceback (most recent call last):
  File "testCode.py", line 10, in <module>
    main()
  File "testCode.py", line 7, in main
    print(get_str_md5(s))
  File "testCode/testBase.py", line 6, in testCode.testBase.get_str_md5
  TypeError: Expected unicode, got bytes  
  ```

  代码:

  ```python
  import hashlib
  
  def get_str_md5(data: str):
      if isinstance(data, str):
          data = data.encode("utf-8") 
      m = hashlib.md5()
      m.update(data)
      return m.hexdigest()
  
  def get_str_md5(data: str):
      bdata = data.encode("utf-8") if isinstance(data, str) else data
      m = hashlib.md5()
      m.update(bdata)
      return m.hexdigest()
  
  ```

  第一个函数会报错，后改写成第二个使用的方式就正常了，可能原因是变量的引用导致的

## python程序在windows后台运行

参考：`https://www.jianshu.com/p/a4ed789b1a34`

* 将Python脚本打包成exe可执行文件

* cmd执行

  ```bash
  sc create MyPythonServer binPath= d:\dir\MyScript.exe
  
  sc start MyPythonServer
  ```

注：没有实际操作过，不确定实际效果。

