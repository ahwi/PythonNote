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



### 第3章 模板

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

**自定义错误页面**

使用基于模板的自定义错误页面，常见的错误码有：

* 404，客户端请求未知页面或路由时显示
* 500，有未处理的异常时显示

自定义错误页面：

```python
@app.errorhandler(404)
def page_not_found(e):
 return render_template('404.html'), 404
@app.errorhandler(500)
def internal_server_error(e):
 return render_template('500.html'), 500
```

使用`Jinja2`的<font color=red>模板继承机制</font>和`Flask-Boostrap`提供的具有<font color=red>页面基本布局的基模板</font>，自定义一个<font color=red>更完整页面布局的基模板</font>：包含导航条，页面内容（可以到衍生模板中定义）。

继承关系：

* `bootstrap/base.html`
* `templates/base.html`
* `templates/user.html`、`templates/404.html`、`templates/500.html`

base.html:

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
 {% block page_content %}{% endblock %}
</div>
{% endblock %}
```

`templates/404.html`:

```html
{% extends "base.html" %}
{% block title %}Flasky - Page Not Found{% endblock %}
{% block page_content %}
<div class="page-header">
 <h1>Not Found</h1>
</div>
{% endblock %}
```

**链接**

flask提供`url_for()`辅助函数，使用程序URL映射中保存的信息生成URL，生成某个视图对应的url链接

如：

* `url_for('index')`得到的结果是`/`
* `url_for('index', _external=True)`返回绝对地址`http://localhost:5000/`
* 使用 url_for() 生成动态地址，`url_for
  ('user', name='john', _external=True)` 的返回结果是`http://localhost:5000/user/john`
* `url_for()` 能将任何额外参数添加到查询字符串中。例如，`url_for('index', page=2)` 的返回结果是 `/?page=2`

**静态文件**

flask使用static路由来引用静态文件：

* `url_for('static', filename='css/styles.css', _external=True) `得到的结果是`http://localhost:5000/static/css/styles.css`
* 默认情况下flask在程序根目录中static的子目录中寻找静态文件，如果需要可在static文件夹中存放文件

示例：在程序的基模板中放置favicon.ico图标

```html
{% block head %}
{{ super() }}
<link rel="shortcut icon" href="{{ url_for('static', filename = 'favicon.ico') }}"
 type="image/x-icon">
<link rel="icon" href="{{ url_for('static', filename = 'favicon.ico') }}"
 type="image/x-icon">
{% endblock %}
```

**使用Flask-Moment本地化日期和时间**

解决服务器和客户端时间问题的方案：服务器使用UTC时间，然后把时间单位发送给web浏览器，转换成当地时间，然后渲染。

使用JavaScript开发的开源库`moment.js`，可以在浏览器中渲染日期和时间，`Flask-Moment`把`moment.js`集成到`Jinja2`模板中。

安装：`pip install flask-moment`

初始化方法：

```python
from flask.ext.moment import Moment
moment = Moment(app)
```

在html中引入：

除了`moment.js`，Flask-Moment还依赖`jquery.js`，不过`Bootstrap`已经引入了`jquery.js`，如下展示了如何在基模板中引入scripts块中引入这个库：

```html
{% block scripts %}
{{ super() }}
{{ moment.include_moment() }}
{% endblock %}
```

为了处理时间戳，Flask-Moment 向模板开放了 moment 类。示例 3-13 中的代码把变量current_time 传入模板进行渲染:

```python
from datetime import datetime
@app.route('/')
def index():
 return render_template('index.html',
 current_time=datetime.utcnow())
```

在模板中渲染`current_time`

`templates/index.html`

```html
<p>The local date and time is {{ moment(current_time).format('LLL') }}.</p>
<p>That was {{ moment(current_time).fromNow(refresh=True) }}</p>
```

* format('LLL') 根据客户端电脑中的时区和区域设置渲染日期和时间。参数决定了渲染的方
  式，'L' 到 'LLLL' 分别对应不同的复杂度。format() 函数还可接受自定义的格式说明符
* 的 fromNow() 渲染相对时间戳，而且会随着时间的推移自动刷新显示的时间。这个时间戳最开始显示为“a few seconds ago”，但指定 refresh 参数后，其内容会随着时间的推移而更新。
* Flask-Moment 实现了 moment.js 中的 format()、fromNow()、fromTime()、calendar()、valueOf()
  和 unix() 方法。

### 第4章 web表单

`Flask-WTF`扩展优化处理web表单的过程，这个扩展对独立的`WTForms`包进行了包装

使用pip安装：

`pip install flask-wtf`

#### 4.1 跨站请求伪造保护

* `Flask-WTF`使用密钥来保护所有表单免受跨站请求伪造（CSRF）的攻击。

* CSFP攻击：恶意网站把请求发送到被攻击者已登录的其他网站时就会引发CSRF攻击。

* Flask-WTF 使用这个密钥生成加密令牌，再用令牌验证请求中表单数据的真伪

* 设置密钥的方法:

  ```python
  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'hard to guess string
  ```

  app.config 字典可用来存储框架、扩展和程序本身的配置变量

#### 4.2 表单类

使用`Flask-WTF`时：

* web表单由Form类的衍生类表示
* Form的类对象对应表单中的字段
* Form的类对象可附属一个或多个验证函数

示例：一个简单的web表单，包含一个文本字段和一个提交按钮:

```python
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
class NameForm(Form):
 name = StringField('What is your name?', validators=[Required()])
 submit = SubmitField('Submit')
```

* WTForms支持的HTML标准字段，见P35
* WTForms内建的验证函数，见P35

#### 4.3 把表单渲染成HTML

表单字段是可调用的，在模板中调用后渲染成HTML。

示例：视图函数把NameForm实例通过参数form传入模板，在模板中生成一个简单的表单:

```html
<form method="POST">
 {{ form.hidden_tag() }}
 {{ form.name.label }} {{ form.name() }}
 {{ form.submit() }}
</form>
```

使用`Boostrap`中预先定义好的表单样式渲染整个`Flask-WTF`表单。

示例：使用`Flask-Bootstrap`渲染表单：

```html
{% import "boostrap/wtf.html" as wtf %}
{{ wtf.quick_form(form) }}
```

`templates/index.html`:使用Flask-WTF和Flask-Bootstrap渲染表单:

```html
{% extends "base.html" %}
{% import "bootstrap/wtf.html" as wtf %}
{% block title %}Flasky{% endblock %}
{% block page_content %}
<div class="page-header">
 <h1>Hello, {% if name %}{{ name }}{% else %}Stranger{% endif %}!</h1>
</div>
{{ wtf.quick_form(form) }}
{% endblock %}
```

在视图函数中处理表单：

```python
@app.route('', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, name=name)
```

如果数据能被所有验证函数接受，那么`validate_on_submit()`方法的返回值为True，否则返回False。

#### 4.5 重定向和用户会话

在上个版本的程序中存在一个可用性问题，用户输入名字后提交表单，然后点击浏览器的刷新按钮，会看到浏览器的再次提交表单警告，原因是：这个请求是一个包含表单数据的POST请求，刷新页面后会再次提交表单。

处理方法：最好别让Web程序把POST请求作为浏览器发送的最后一个请求，使用重定向作为POST请求的响应。

示例：重定向POST请求

```python
from flask import Flask, render_template, session, redirect, url_for
@app.route('/', methods=['GET', 'POST'])
def index():
 form = NameForm()
 if form.validate_on_submit():
 session['name'] = form.name.data
 return redirect(url_for('index'))
 return render_template('index.html', form=form, name=session.get('name'))
```

#### 4.6 Flash消息

flash消息可以用来确认消息、警告或者错误提醒

示例：

用户提交错误的登录信息，服务器发回的响应重新渲染表单，并在表单上面显示一个消息，提示错误：

* 在代码中调用`flash()`

    ```python
    @app.route('/', methods=['GET', 'POST'])
    def index():
        name = None
        form = NameForm()
        if form.validate_on_submit():
            old_name = session.get("name")
            if old_name is not None and old_name != form.name.data:
                flash('Looks like you have changed your name')
            session['name'] = form.name.data
            return redirect(url_for('index'))
        return render_template("index.html", form=form, name=session.get('name'))
    ```

    如果用户提交的名字和存储再用户会话中的名字不一样，就会调用flash()函数，在发给客户段的一个响应中显示一个消息。

* 渲染消息：

    仅调用`flask()`函数并不能把消息显示出来，程序使用的模板要渲染这些消息。

    Flask把`get_flashed_message()`函数开放给模板，用来获取并渲染消息：

    ```html
    {% block content %}
    <div class="container">
     {% for message in get_flashed_messages() %}
        <div class="alert alert-warning">
         <button type="button" class="close" data-dismiss="alert">&times;</button>
         {{ message }}
        </div>
     {% endfor %}
    ```

### 第5章 数据库

SQL和NoSQL的对比

本书选择的数据库框架是`Flask-SQLAlchemy`，扩展包装了`SQLAlchemy`框架。

#### 5.5 使用Flask-SQLAlchemy管理数据库

**安装:**

```shell
pip install flask-sqlalchemy
```

在`Flask-SQLAlchemy`中，<font color=red>数据库使用URL指定</font>。使用方式如下：

| 数据库引擎        | URL                                              |
| :---------------- | ------------------------------------------------ |
| MySQL             | mysql://username:password@hostname/database      |
| Postgres          | postgresql://username:password@hostname/database |
| SQLite（Unix）    | sqlite:////absolute/path/to/database             |
| SQLite（Windows） | sqlite:///c:/absolute/path/to/database           |

**在代码中使用：**

```python
from flask.ext.sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
```

* 程序使用的数据库URL必须保存到Flask配置对象的SQLALCHEMY_DATABASE_URI键中
* SQLALCHEMY_COMMIT_ON_TEARDOWN键设置为True时，每次请求结束后会自动提交数据库中的变动。

#### 5.6 定义模型

`Flask-SQLAlchemy`创建的数据库实例为模型提供了一个基类已经一系列辅助类和辅助函数，可用于定义模型的结构。

示例：定义了模型`Role`和`User`

```python
class Role(db.Model):
    __table_name_ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), primary_key=True)

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __table_name_ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return '<User %r>' % self.username
```



#### 5.7 关系

关系型数据库使用关系把不同表中的行联系起来。

roles表和users表是一种角色到用户的一对多关系，因为一个角色可属于多个用户，而每个用户都只能有一个角色。

示例：一对多关系在模型类中的表示方法:

```python
class Role(db.Model):
 # ...
 users = db.relationship('User', backref='role')
class User(db.Model):
 # ...
 role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
```

* 关系users表中的外键连接了两行，role_id为外键，传给`db.ForeignKey()`的参数`roles.id`表明，这列的值是roles表中行的id值

* Role模型中的users属性代表这个关系的面向对象视角。

* 对于一个Role类的实例，其users属性将返回与角色相关联的用户组成的列表

* `db.relationship()`：

  * 第一个参数表明这个关系的另一端是哪个模型
  * backref参数向User模型中添加一个role属性，从而定义反向关系。这一属性可替代`role_id`访问Role模型，此时所获取的是模型对象，而不是外键的值




## 备注

* github链接地址:

  ```
  https://github.com/miguelgrinberg/flasky.git
  ```

* flask是如何使用上下文在多线程的环境中，让某个变量成为某一线程的全局可访问变量





















