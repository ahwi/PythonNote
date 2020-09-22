# Flask-Web开发：基于Python的Web应用开发实战

## 第二章 程序的基本结构

初始化:

* 必须创建一个程序实例

* web服务器-使用->web服务器网关接口(web server gateway Interface, WSGI)协议--(接收自客户端的所有请求)-->程序实例对象处理

* 创建代码:

  ```python
  from flask import Flask
  app = Flask(__name__)
  ```

* Flask使用构造函数的name参数决定程序的根目录

路由和视图函数:

客户端 --(请求)--> web服务器 --(请求)--> Flask程序实例

路由: 处理URL和函数之间关系的程序

* `app.route`装饰器把函数注册为路由

  ```python
  @app.rout('/')
  def index():
      return '<h1>Hello World</h1>'
  ```

* `route`装饰器使用动态名字

  ```python
  @app.route('/user/<name>')
  def user(name):
      return '<h1>Hello, %s!</h1>'
  ```

* 动态部分默认使用字符串，可以使用类型定义`/user/<int:id>`

  * 支持的类型：int、float、path(也是字符串)

启动服务器：

```python
if __name__ == '__main__':
    app.run(debug=True)
```



**请求-响应循环**

**1. 程序和请求上下文**

flask使用上下文，让视图函数可以访问请求对象和其他对象

如:

```python
from flask import request

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is %s</p>' % user_agent
```

在这个视图函数中，我们把request当做全局变量使用，事实上，request不是全局变量，在多线程服务中，Flask使用上下文让特定的变量在一个线程中全局可访问，与此同时却不会干扰其他线程。

flask中有两种上下文:

* 程序上下文
* 请求上下文



| 变量名      | 上下文     | 说明                                                   |
| ----------- | ---------- | ------------------------------------------------------ |
| current_app | 程序上下文 | 当前激活程序的程序实例                                 |
| g           | 程序上下文 | 处理请求时用作临时存储的对象。每次请求都会重设这个变量 |
| request     | 请求上下文 | 请求对象，封装了客户端发出的HTTP请求中的内容           |
| session     | 请求上下文 | 用户会话，用于存储请求之间需要“记住”的值的词典         |

Flask在分发请求之前激活（或推送）程序和请求上下文，请求处理完成后再将其删除



例子：程序上下文的使用方法：

```python
>>> from hello import app
>>> from flask import current_app
>>> current_app.name
程序的基本结构 ｜ 13
Traceback (most recent call last):
...
RuntimeError: working outside of application context
>>> app_ctx = app.app_context()
>>> app_ctx.push()
>>> current_app.name
'hello'
>>> app_ctx.pop()
```



**2. 请求调度**

Flask通过URL映射(URL和视图函数之间的对应关系)查找请求的URL

添加映射的方法:

* app.rout装饰器
* app.add_url_rule()

查看映射的方法：

```python
>>> from hello import app
>>> app.url_map
Map([<Rule '/' (HEAD, OPTIONS, GET) -> index>,
 <Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>,
 <Rule '/user/<name>' (HEAD, OPTIONS, GET) -> user>])
```

**3. 请求钩子**

有时在处理请求之前或之后执行代码会很有用，flask使用请求钩子来实现

请求钩子使用装饰器实现，Flask支持以下4中钩子：

* before_first_request：注册一个函数，在处理第一个请求之前运行。
*  before_request：注册一个函数，在每次请求之前运行。
*  after_request：注册一个函数，如果没有未处理的异常抛出，在每次请求之后运行。
*  teardown_request：注册一个函数，即使有未处理的异常抛出，也在每次请求之后运行。

在请求钩子函数和视图函数之间共享数据一般使用上下文全局变量 g。

**4. 响应**

HTTP协议需要的不仅仅只有作为请求响应的字符串，还有一个很重要的部分是状态码

如下：返回一个400状态码，表示请求无效

```python
@app.route('/')
def index():
 return '<h1>Bad Request</h1>', 400
```

视图函数返回的响应还可接受第三个参数，这是一个由首部（header）组成的字典，可以
添加到 HTTP 响应中。

* Flask视图函数还可以返回Response对象

```python
from flask import make_response
@app.route('/')
def index():
 response = make_response('<h1>This document carries a cookie!</h1>')
 response.set_cookie('answer', '42')
 return response
```

* 重定向的特殊响应类型：

  重定向响应可以使用3 个值形式的返回值生成，也可在 Response 对象中设定。不过，由于使用频繁，Flask 提供了 redirect() 辅助函数，用于生成这种响应

  ```python
  from flask import redirect
  @app.route('/')
  def index():
   return redirect('http://www.example.com')
  ```

* 处理错误的特殊响应类型abort

  ```python
  from flask import abort
  @app.route('/user/<id>')
  def get_user(id):
   user = load_user(id)
   if not user:
   abort(404)
   return '<h1>Hello, %s</h1>' % user.name
  ```

  abort 不会把控制权交还给调用它的函数，而是抛出异常把控制权交给 Web 服务器。



## 备注

* flask是如何使用上下文在多线程的环境中，让某个变量成为某一线程的全局可访问变量





















