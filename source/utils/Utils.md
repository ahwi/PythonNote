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
    all_task = [executor.submit(get_html, (url)) for url in urls]

    for future in as_completed(all_task):
        data = future.result()
        print("in main: get page {}s success".format(data))


if __name__ == '__main__':
    test_thread_pool()
```

<font color=red>as_completed()</font>方法是一个生成器，在没有任务完成的时候，会阻塞，在有某个任务完成的时候，会<font color=red>yield</font>这个任务，就能执行for循环下面的语句，然后继续阻塞住，循环到所有的任务结束。从结果也可以看出，**先完成的任务会先通知主线程**。

