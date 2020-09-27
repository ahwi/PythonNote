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



**Flask扩展**

Flask被设计为可扩展形式，如数据库和用户认证

**1. 使用Flask-Script支持命令行选项**

flask支持很多启动设置选项，但只能在脚本中作为参数传给`app.run()`函数，使用`Flask-Script`可以为flask添加一个命令行解析器的扩展。

* 安装：

  ```python
  pip install flask-script
  ```

* 使用：

  ```python
  from flask.ext.script import Manager
  manager = Manager(app)
  
  if __name__ == "__main__":
      manager.run()
  ```

  为flask开发的扩展都暴露在flask.ext命名空间下，`Flask-Script`输出一个名为Manager的类。该扩展的初始化方法也适用于其他很多扩展：程序实例--(作为参数)-->构造函数-->初始化主类的实例-->在其他扩展中使用。



## 第3章 模板

为了方便理解和维护，将视图函数的业务逻辑和表现逻辑分开，将表现逻辑移到模板中。

为了渲染模板，Flask使用`Jinja2`模板引擎

**Jinja2模板引擎**

示例：

```html
<h1>Hello, {{name}}!</h1>
```

**1. 渲染模板**

示例：

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/user/<name>')
def user(name):
    return render_template("user.html", name=name)

if __name__ == '__main__':
    app.run()
```

* 默认情况下，Flask在templates子文件夹中寻找模板
* Flask提供`render_template`函数把`Jinjia2`模板引擎集成到程序中

**2. 变量**

* 模板中使用的`{{ name }}`结构表示一个变量，告诉模板引擎这个位置的值从渲染模板时使用的数据中获取

* Jinja2能失败列表、字典和对象等，如：

  ```html
  <p>A value from a dictionary: {{ mydict['key'] }}.</p>
  <p>A value from a list: {{ mylist[3] }}.</p>
  <p>A value from a list, with a variable index: {{ mylist[myintvar] }}.</p>
  <p>A value from an object's method: {{ myobj.somemethod() }}.</p>
  ```

* 过滤器：用来修饰变量

  如： `Hello, {{ name|capitalize }}`以首字母大写形式显示变量name的值

  | 过滤器名   | 说　　明                                   |
  | ---------- | ------------------------------------------ |
  | safe       | 渲染值时不转义                             |
  | capitalize | 把值的首字母转换成大写，其他字母转换成小写 |
  | lower      | 把值转换成小写形式                         |
  | upper      | 把值转换成大写形式                         |
  | title      | 把值中每个单词的首字母都转换成大写         |
  | trim       | 把值的首尾空格去掉                         |
  | striptags  | 渲染之前把值中所有的 HTML 标签都删掉       |

**3. 控制结构**

Jinja2提供了多种控制结构，可用来改变模板的渲染流程

* 条件控制语句

  ```html
  {% if user %}
   Hello, {{ user }}!
  {% else %}
   Hello, Stranger!
  {% endif %}
  ```

* 使用for循环渲染一组元素

  ```html
  <ul>
   {% for comment in comments %}
   <li>{{ comment }}</li>
   {% endfor %}
  </ul>
  ```

* 支持宏：

  ```html
  {% macro render_comment(comment) %}
   <li>{{ comment }}</li>
  {% endmacro %}
  <ul>
   {% for comment in comments %}
   {{ render_comment(comment) }}
   {% endfor %}
  </ul>
  ```

* 在模板中导入宏

  ```html
  {% import 'macros.html' as macros %}
  <ul>
   {% for comment in comments %}
   {{ macros.render_comment(comment) }}
   {% endfor %}
  </ul>
  ```

* 重复使用的代码单独封装，再引入：

  ```html
  {% include 'common.html' %}
  ```

* 继承：

  base.html

  ```html
  <html>
  <head>
   {% block head %}
   <title>{% block title %}{% endblock %} - My Application</title>
   {% endblock %}
  </head>
  <body>
   {% block body %}
   {% endblock %}
  </body>
  </html>
  ```

  sub.html

  ```html
  {% extends "base.html" %}
  {% block title %}Index{% endblock %}
  {% block head %}
   {{ super() }}
   <style>
   </style>
  {% endblock %}
  {% block body %}
  <h1>Hello, World!</h1>
  {% endblock %}
  ```

**使用Flask-Bootstrap集成Twitter Bootstrap**

Bootstrap介绍:

* Twitter开发的开源框架

* 提供的用户界面组件可用于创建简洁且具有吸引力的网页，这些网页兼容所有现代Web浏览器

* Boostrap是客户端框架，因此不会直接涉及服务器

* 服务器需要做的只是提供引用了Bootstrap 层 叠 样 式 表（CSS） 和 JavaScript 文 件 的 HTML 响 应， 并 在 HTML、CSS 和JavaScript 代码中实例化所需组件。

* 安装:

  ```bash
  python3 -m pip install flask-bootstrap
  ```

* 初始化方法：Flask扩展一般都在创建程序实例时初始化

  ```python
  from flask.ext.bootstrap import Bootstrap
  # ...
  bootstrap = Bootstrap(app)
  ```

* 使用：

  在程序中使用一个包含所有Bootstrap文件的基模板，这个模板利用Jinja2的模板集成机制，让程序扩展一个具有基本页面结构的基模板，其中就有用来引入Bootstrap的元素。示例：把user.html改写为衍生模板后的新版本:

  ```html
  {% extends "bootstrap/base.html" %}
  {% block title %}Flasky{% endblock %}
  {% block navbar %}
  <div class="navbar navbar-inverse" role="navigation">
   <div class="container">
   <div class="navbar-header">
   <button type="button" class="navbar-toggle"
   data-toggle="collapse" data-target=".navbar-collapse">
   <span class="sr-only">Toggle navigation</span>
   <span class="icon-bar"></span>
   <span class="icon-bar"></span>
   <span class="icon-bar"></span>
   </button>
   <a class="navbar-brand" href="/">Flasky</a>
   </div>
   <div class="navbar-collapse collapse">
   <ul class="nav navbar-nav">
   <li><a href="/">Home</a></li>
   </ul>
   </div>
   </div>
  </div>
  {% endblock %}
  {% block content %}
  <div class="container">
   <div class="page-header">
   <h1>Hello, {{ name }}!</h1>
   </div>
  </div>
  {% endblock %}
  ```

  * Jinja2 中的 extends 指令从 Flask-Bootstrap 中导入 bootstrap/base.html，从而实现模板继承。

  * Flask-Bootstrap 中的基模板提供了一个网页框架，引入了 Bootstrap 中的所有 CSS 和JavaScript 文件。

  * 基模板中定义了可在衍生模板中重定义的块。block 和 endblock 指令定义的块中的内容可添加到基模板中。

  * 很多块都是 Flask-Bootstrap 自用的，如果直接重定义可能会导致一些问题。如果程序需要向已经有内容的块中添加新内容，必须使用 Jinja2 提供的 super() 函数。

  * Flask-Bootstrap 的 base.html 模板还定义了很多其他块，都可在衍生模板中使用:

    | 块　　名     | 说　　明                   |
    | ------------ | -------------------------- |
    | doc          | 整个 HTML 文档             |
    | html_attribs | <html>标签的属性           |
    | html         | <html>标签中的内容         |
    | head         | <head>标签中的内容         |
    | title        | <title>标签中的内容        |
    | metas        | 一组<meta>标签             |
    | styles       | 层叠样式表定义             |
    | body_attribs | <body>标签的属性           |
    | body         | <body>标签中的内容         |
    | navbar       | 用户定义的导航条           |
    | content      | 用户定义的页面内容         |
    | scripts      | 文档底部的 JavaScript 声明 |















## 备注

* github链接地址:

  ```
  https://github.com/miguelgrinberg/flasky.git
  ```

* flask是如何使用上下文在多线程的环境中，让某个变量成为某一线程的全局可访问变量





















