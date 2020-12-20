# Flask-Web开发：基于Python的Web应用开发实战

###  第1章 安装

**有两个主要依赖**

* 路由、调试、web服务器网关接口子系统 -- 由 Werkzeug提供
* 模板系统  -- 由Jinja2提供

**扩展形式实现**

* 数据库访问
* web表单验证
* 用户认证
* 等等

**使用虚拟环境**

* linux

  ```bash
  python -m venv ./venv
  source venv/bin/activate
  ```

* windows

  ```cmd
  python -m venv ./venv
  venv/Scripts/activate
  ```

###  第2章 程序的基本结构

#### 2.1 初始化

* 必须创建一个程序实例

* web服务器-使用->web服务器网关接口(web server gateway Interface, WSGI)协议--(接收自客户端的所有请求)-->程序实例对象处理

* 创建代码:

  ```python
  from flask import Flask
  app = Flask(__name__)
  ```

* Flask使用构造函数的name参数决定程序的根目录

#### 2.2 路由和视图函数:

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

#### 2.3 启动服务器：

```python
if __name__ == '__main__':
    app.run(debug=True)
```

Flask提供的Web服务器不适合在生成环境中使用。第17章会介绍生产环境Web服务器。



#### 2.5 请求-响应循环

##### 2.5.1 程序和请求上下文

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
Traceback (most recent call last):
...
RuntimeError: working outside of application context
>>> app_ctx = app.app_context()
>>> app_ctx.push()
>>> current_app.name
'hello'
>>> app_ctx.pop()
```



##### 2.5.2 请求调度

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

##### 2.5.3 请求钩子

有时在处理请求之前或之后执行代码会很有用，flask使用请求钩子来实现

请求钩子使用装饰器实现，Flask支持以下4中钩子：

* before_first_request：注册一个函数，在处理第一个请求之前运行。
*  before_request：注册一个函数，在每次请求之前运行。
*  after_request：注册一个函数，如果没有未处理的异常抛出，在每次请求之后运行。
*  teardown_request：注册一个函数，即使有未处理的异常抛出，也在每次请求之后运行。

在请求钩子函数和视图函数之间共享数据一般使用上下文全局变量 g。

##### 2.5.4 响应

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

#### 2.6 Flask扩展

Flask被设计为可扩展形式，如数据库和用户认证

##### 使用Flask-Script支持命令行选项

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

#### 3.1 Jinja2模板引擎

新式最简单的`Jinja2`模板就是一个包含响应文本的文件

如:

`templates/index.html`

```html
<h1>Hello, {{name}}!</h1>
```

`templates/user.html`

```html
<h1>Hello, {{ name }}!</h1>
```

##### 3.1.1 渲染模板

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
* Flask提供`render_template`函数把`Jinja2`模板引擎集成到程序中

##### 3.1.2 变量

* 模板中使用的`{{ name }}`结构表示一个变量，告诉模板引擎这个位置的值从渲染模板时使用的数据中获取

* Jinja2能识别所有类型的变量，甚至是列表、字典和对象等，如：

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

#### 3.2 使用Flask-Bootstrap集成Twitter Bootstrap

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

#### 3.3 自定义错误页面

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

#### 3.4 链接

flask提供`url_for()`辅助函数，使用程序URL映射中保存的信息生成URL，生成某个视图对应的url链接

如：

* `url_for('index')`得到的结果是`/`
* `url_for('index', _external=True)`返回绝对地址`http://localhost:5000/`
* 使用 url_for() 生成动态地址，`url_for
  ('user', name='john', _external=True)` 的返回结果是`http://localhost:5000/user/john`
* `url_for()` 能将任何额外参数添加到查询字符串中。例如，`url_for('index', page=2)` 的返回结果是 `/?page=2`

#### 3.5 静态文件

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

#### 3.6 使用Flask-Moment本地化日期和时间

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

* 请求对象包含客户端发出的所有请求信息，`request.form`能获取`POST`请求中提交的表单数据

* `Flask-WTF`扩展优化处理web表单的过程，这个扩展对独立的`WTForms`包进行了包装

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

`pip install flask-sqlalchemy`

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

* 最常用的`SQLAlchemy`类型

  见P48表5-2

* 最常使用的SQLAlchemy列选项

  见P48表5-3

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

常用的SQLAlchemy关系选项

​	P49  表5-4

#### 5.8 数据库操作

增删改查的操作

#### 5.9 在视图函数中操作数据库

将用户名写入到数据库中

`hello.py`

```python
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        # form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))
```

对应的模板新版本

`templates/index.html`

```html
{% extends "base.html" %}
{% import "bootstrap/wtf.html" as wtf %}

{% block title %}Flasky{% endblock %}

{% block page_content %}
    <div class="page-header">
        <h1>Hello, {% if name %}{{ name }}{% else %}Stranger{% endif %}!</h1>
        {% if not known %}
        <p>Pleased to meet you!</p>
        {% else %}
        <p>Heppy to see you again!</p>
        {% endif %}
    </div>
    {{ wtf.quick_form(form) }}
{% endblock %}
```

#### 5.10 集成Python shell

启动shell命令行模式时，自动导入需要导入的模块

示例：为shell命令添加一个上下文

```python
from flask.ext.script import Shell

def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role) 
manager.add_command("shell", Shell(make_context=make_shell_context))
```

操作:

```bash
$ python hello.py shell
>>> app
<Flask 'app'>
>>> db
<SQLAlchemy engine='sqlite:////home/flask/flasky/data.sqlite'>
>>> User
<class 'app.User'>
```

#### 5.11 使用Flask-Migrate实现数据库迁移

`Alembic`数据库迁移框架

##### 5.11.1 创建迁移仓库

* 安装

  `pip install flask-migrate`

* 配置`Flask-Migrate`

  `hello.py`

  ```python
  from flask.ext.migrate import Migrate, MigrateCommand
  # ...
  migrate = Migrate(app, db)
  manager.add_command('db', MigrateCommand)
  ```

  为了导出数据库迁移命令，Flask-Migrate 提供了一个 MigrateCommand 类，可附加到FlaskScript 的 manager 对象上。

* 使用init子命令创建迁移仓库

  ```bash
  (venv) $ python hello.py db init
   Creating directory /home/flask/flasky/migrations...done
   Creating directory /home/flask/flasky/migrations/versions...done
   Generating /home/flask/flasky/migrations/alembic.ini...done
   Generating /home/flask/flasky/migrations/env.py...done
   Generating /home/flask/flasky/migrations/env.pyc...done
   Generating /home/flask/flasky/migrations/README...done
   Generating /home/flask/flasky/migrations/script.py.mako...done
   Please edit configuration/connection/logging settings in
   '/home/flask/flasky/migrations/alembic.ini' before proceeding.
  ```

##### 5.11.2 创建迁移脚本

* `Alembic`中，数据迁移用迁移脚本表示，脚本中有两个函数
  * `upgrade()`：把迁移的改动应用到数据库中
  * `downgrade()`：将改动删除
* Alembic 具有添加和删除改动的能力，因此数据库可重设到修改历史的任意一点。
* 可以使用 revision 命令手动创建 Alembic 迁移，也可使用 migrate 命令自动创建
  * 手动创建的迁移只是一个骨架，upgrade() 和 downgrade() 函数都是空的
  * 自动创建的迁移会根据模型定义和数据库当前状态之间的差异生成 upgrade() 和 downgrade() 函数的内容，但自动创建的迁移不一定总是正确的，需要进行检查

示例：

使用`migrate`子命令来自动创建迁移脚本

```bash
(venv) $ python hello.py db migrate -m "initial migration"
INFO [alembic.migration] Context impl SQLiteImpl.
INFO [alembic.migration] Will assume non-transactional DDL.
INFO [alembic.autogenerate] Detected added table 'roles'
INFO [alembic.autogenerate] Detected added table 'users'
INFO [alembic.autogenerate.compare] Detected added index
'ix_users_username' on '['username']'
 Generating /home/flask/flasky/migrations/versions/1bc
 594146bb5_initial_migration.py...done
```

注：猜测：`ablembic`首次是根据代码中的表数据库模型进行创建迁移脚本，需要先删除已有的数据库，不然没有初始脚本和已有数据库的变化不会产生迁移脚本

##### 5.11.3 更新数据库

使用`db upgrade`命令把迁移应用到数据库中

```base
(venv) $ python hello.py db upgrade
INFO [alembic.migration] Context impl SQLiteImpl.
INFO [alembic.migration] Will assume non-transactional DDL.
INFO [alembic.migration] Running upgrade None -> 1bc594146bb5, initial migration
```

对第一个迁移来说，其作用和调用 db.create_all() 方法一样。但在后续的迁移中，upgrade 命令能把改动应用到数据库中，且不影响其中保存的数据。





### 第7章 大型程序的结构

本章介绍一种使用包和模块组织大型程序的方式

#### 7.1 项目结构

多文件Flask程序的基本结构

```shell
|-flasky
 |-app/
 |-templates/
 |-static/
 |-main/
 |-__init__.py
 |-errors.py
 |-forms.py
 |-views.py
 |-__init__.py
 |-email.py
 |-models.py
 |-migrations/
 |-tests/
 |-__init__.py
 |-test*.py
 |-venv/
 |-requirements.txt
 |-config.py
 |-manage.py
```

这种结构有 4 个顶级文件夹：

*  app

  Flask 程序一般都保存在这个文件夹中

* migrations 

  包含数据库迁移脚本

*  tests 

  单元测试

*  venv 

  包含 Python 虚拟环境。

#### 7.2 配置选项

程序经常需要设定多个配置，比如开发、测试和生成环境要使用不同的数据库，这样才不会互相影响。

#### 7.3 程序包

**1. 使用程序工程函数**

**2. 在蓝本中实现程序功能**

## 第二部分 实例：社交博客程序

### 第8章 用户认证

#### 8.1 Flask的认证扩展

* Flask-Login：管理已登录用户的用户会话。
* Werkzeug：计算密码散列值并进行核对。
* itsdangerous：生成并核对加密安全令牌。
* Flask-Mail：发送与认证相关的电子邮件。
* Flask-Bootstrap：HTML 模板。
* Flask-WTF：Web 表单。 

#### 8.2 密码安全性

`werkzeug`实现密码散列

* `generate_password_hash(password, method=pbkdf2:sha1, salt_length=8)`
* `check_password_hash(hash, password)`

#### 8.3 创建蓝本

不同功能 --创建--> 不同蓝本

认证蓝本 auth --> 用户认证相关的路由

注册蓝本函数：

`app/__init__.py`

```python
def create_app(config_name):
 # ...
 from .auth import auth as auth_blueprint
 app.register_blueprint(auth_blueprint, url_prefix='/auth')
 return app
```

url_prefix参数 --> 蓝本中定义的路由都会加上指定前缀

示例：

* 创建蓝本
* 蓝本中的路由和视图函数
* 附加蓝本

#### 8.4 使用Flask-Login认证用户

`Flask-Login`:管理用户的认证状态

* 必须实现的方法：

  * is_authenticated()
  * is_active()
  * is_anonymous()
  * get_id()

* 实现

  * 模型类中直接实现方法
  * 使用UserMixim类   -->  包含这些方法的默认实现

* 示例：

  * 修改User模型

  * 初始化Flask-Login

  * 加载用户的回调函数

  * 保护路由

    * `login_required`修饰器

      * 如果未认证的用户访问这个路由，`Flask-Login`会拦截请求，把用户发往登录页面

##### 8.4.3 添加登录表单

呈现给用户的登陆表单包含一个用于输入电子邮件地址的文本字段、一个密码字段、一个"记住我"复选框和提交按钮。

**登陆表单类：**

```python
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(Form):
    email = StringField('Email',
                        validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')
```

**`auth/login.html`模板**

使用`wtf.quick_form()`宏渲染表单

```html
{% extends "base.html" %}
{% import "bootstrap/wtf.html" as wtf %}

{% block title %}Flasky - Login{% endblock %}

{% block page_content %}
<div class="page-header">
    <h1>Login</h1>
</div>
    {{ wtf.quick_form(form) }}
{% endblock %}
```

**添加登入登出导航条**

在`base.html`模板中的导航条中添加登入登出状态

```html
        <ul class="nav navbar-nav navbar-right">
            {% if current_user.is_authenticated() %}
            <li><a href="{{ url_for('auth.logout') }}">Sign Out</a></li>
            {% else %}
            <li><a href="{{ url_for('auth.login') }}">Sign In</a></li>
            {% endif %}
        </ul>
```

判断条件中的变量`current_user`由`Flask-Login`定义，且在视图函数和模板中自动可用。

##### 8.4.4 登入用户

**添加登陆路由**

`app/auth/view.py`登陆路由

```python
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user
from . import auth
from ..models import User
from .forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)
```

* `login_user()`函数的参数是要登陆的用户，以及可选的"记住我"布尔值，如果值为False，那么关闭浏览器后用户会话就国企，如果为True会在浏览器中写一个长期有效的cookie，使用这个cookie可用复现用户会话。

**渲染登陆表单**

```html
{% extends "base.html" %}
{% import "bootstrap/wtf.html" as wtf %}

{% block title %}Flasky - Login{% endblock %}

{% block page_content %}
<div class="page-header">
    <h1>Login</h1>
</div>
<div class="col-md-4">
    {{ wtf.quick_form(form) }}
</div>
{% endblock %}
```

##### 8.4.5 登出用户

退出路由的实现

`app/auth/view.py`

```python
from flask.ext.login import logout_user, login_required 

@auth.route('/logout')
@login_required
def logout():
    login_user()
    flash('You have benn logged out')
    return redirect(url_for('main.index'))
```

##### 8.4.6 测试登陆

为已登陆的用户显示一个欢迎消息

`app/templates/index.html`

```python
    <h1>Hello,
        {% if current_user.is_authenticated() %}
            {{ current_user.username }}
        {% else %}
            Stranger
        {% endif %}!
    </h1>
```





#### 8.5 注册新用户

##### 1. 添加用户表单

`app/auth/forms.py`

````python
class RegistrationForm(Form):
    email = StringField('Email',
                        validators=[Required(), Length(1, 64), Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Username must have only letters'
                                          'numbers, dots or underscores'
                                          )
    ])
    password = PasswordField('Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
````

* 验证函数：

  * Regexp
  * EqualTo

* 自定义验证函数

  `validate_` + 字段名    -->  和常规验证函数一起调用

##### 2. 添加注册模板

`/templates/auth/register.html`

````html
{% extends "base.html" %}
{% import "bootstrap/wtf.html" as wtf %}

{% block title %}Flasky - Register{% endblock %}

{% block page_content %}
<div class="page-header">
    <h1>Register</h1>
</div>
<div class="col-md-4">
    {{ wtf.quick_form(form) }}
</div>
{% endblock %}
````

##### 3. 添加到注册页面的链接

````html
<div class="col-md-4">
    {{ wtf.quick_form(form) }}
    <p>
        New user?
        <a href="{{ url_for('auth.register') }}">
            Click here to register
        </a>
    </p>
</div>
````

##### 4. 添加注册新用户的视图函数

````python
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
````

#### 8.6 确认账户

**1. `使用itsdangerous`生成确认令牌**

* 生成带有用户id加密签名的链接
* 用户点击链接解出id，确认id后进行认证

示例：

使用 itsdangerous 包生成包含用户 id 的安全令牌：

```shell
(venv) $ python manage.py shell
>>> from manage import app
>>> from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
>>> s = Serializer(app.config['SECRET_KEY'], expires_in = 3600)
>>> token = s.dumps({ 'confirm': 23 })
>>> token
'eyJhbGciOiJIUzI1NiIsImV4cCI6MTM4MTcxODU1OCwiaWF0IjoxMzgxNzE0OTU4fQ.ey ...'
>>> data = s.loads(token)
>>> data
{u'confirm': 23}
```

将这种生成和检验令牌的功能可添加到 User 模型中

`app/models.py`:确认用户账户

```python
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from . import db


class User(UserMixin, db.Model):
    # ...
    confirmed = db.Column(db.Boolean, default=False)
    
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True
```

**2. 发送确认邮件**

**在注册路由中添加发送确认邮件的代码：**

`app/auth/views.py`：能发送确认邮件的注册路由

```python
from ..email import send_email

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # ...
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email,
                   'Confirm Yor account',
                   'auth/email/confirm',
                   user=user,
                   token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)
```

**确认账户的视图函数：**

`app/auth/views.py`确认用户的账户

```python
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))
```

* `login_required`修饰器会保护这个路由，用户点击确认邮件中的链接后，要先登录，然后才能执行这个视图函数

**添加对未确认用户的处理：**

每个程序都可用决定用户确认账户之前可用做哪些操作，比如，允许未确认的用户登录，但只显示一个页面，在这个页面要求用户在获取权限之前先确认账户。可用使用`before_app_request`修饰器来解决这个问题。

`app/auth/views.py`在before_app_request处理程序中过滤未确认的账户

```python
@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))
```

同时满足以下3个条件时，`before_app_request`处理程序才会拦截请求

* 用户已登录（current_user.is_authenticated()必须返回True）
* 用户的账户还未确认
* 请求的端点（使用request.endpoint获取）不在认证蓝本中。访问认证路由要获取权限，因为这些路由的作用时让用户确认账户或执行其他账户管理操作

显示给未确认用户的页面需要提供一个重新发送账户确认邮件的链接

`app/auth/views.py`重新发送账户确认邮件

```python
@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))
```

#### 8.7 管理账户

可以添加一些扩展功能

* 修改密码
* 重设密码
* 修改电子邮件地址

### 第9章 用户角色

本章介绍用户角色的实现方式，赋予用户分立的角色，但角色使用权限定义

#### 9.1 角色在数据库中的表示

**改进Role模型**

```python
class Role(db.Model):
 __tablename__ = 'roles'
 id = db.Column(db.Integer, primary_key=True)
 name = db.Column(db.String(64), unique=True)
 default = db.Column(db.Boolean, default=False, index=True)
 permissions = db.Column(db.Integer)
 users = db.relationship('User', backref='role', lazy='dynamic')
```

添加两个字段：

* default：只有默认角色的default字段要设置为True，其他都设置为Flase。用户注册时，其角色会被设置为默认角色。

* permissions: 权限，值是一个整数，各个操作都对应一个标志位

  ![1603789360424](assets/1603789360424.png)

**权限与角色**

表9-1的权限可以使用下面的代码表示：

`app/models.py`:权限常量

```python
class Permission:
    FOLLOW = 0X01
    COMMENT = 0X02
    WRITE_ARTICLES = 0X04
    MODERATE_COMMENTS = 0X08
    ADMINISTER = 0X80
```

表 9-2列出了要支持的用户角色以及定义角色使用的权限位

![1607830344781](assets/1607830344781.png)

将角色添加到代码中：

在`Role`类中添加一个类方法，实现在数据库中创建角色：

```python
class Role(db.Model):
    # ...
    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
            db.session.commit()
```

`insert_roles()`函数，数据库有该账户则更新，没有则插入

#### 9.2 赋予用户角色

用户在程序注册账户时，会被赋予适当的角色，大多数用户注册的角色是`User`。管理员的注册流程是：在配置`FLASKY_ADMIN`字段的值中设置管理员的邮箱，注册时会判断，如果是管理员的邮箱注册就会设置为管理员权限

```python
class User(UserMixin, db.Model):
    # ...
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
    # ...
```



#### 9.3 角色验证

在`User`模型和`AnonymousUser`模型中添加一个辅助方法，检查是否有指定的权限

`app/models.py`

```python
from flask.ext.login import UserMixin, AnonymousUserMixin
class User(UserMixin, db.Model):
    # ...
    def can(self, permissions):
        return self.role is not None and \
    (self.role.permissions & permissions) == permissions
    def is_administrator(self):
        return self.can(Permission.ADMINISTER)
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    def is_administrator(self):
        return False
login_manager.anonymous_user = AnonymousUser
```

* 使用`can()`方法来判断角色的权限
* 定义了`AnonymousUser`类，用来保持一致性，将其设置为用户未登录时的`current_user`的值，这样程序不用先检查用户是否登录，就能自由的调用`current_user.can()`和`current_user.is_admnistrator()`

自定义装饰器，让视图函数只对具有特定权限的用户开放

`app/decorators.py`:检查用户权限的自定义修饰器

```python
from functools import wraps
from flask import abort
from flask.ext.login import current_user
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
                return f(*args, **kwargs)
            return decorated_function
        return decorator
def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)
```

如何使用这些装饰器

```python
from decorators import admin_required, permission_required
from .models import Permission
@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"

@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
    return "For comment moderators!"

```

`Permission`类为所有权限位定义了常量以便于获取

使用上下文管理器让变量在所有模板中全局可访问

`app/main/__init__.py`

```python
@main.app_context_processor
def inject_permissions():
 	return dict(Permission=Permission)
```

### 第10章 用户资料

实现Flasky的用户资料页面

#### 10.1 资料信息

添加一些关于用户的其他信息，扩充`User`模型

`app/models.py`：用户信息字段

```python
class User(UserMixin, db.Model):
    # ...
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
```

刷新用户的最后访问时间

`app/models.py`

```python
class User(UserMixin, db.Model):
    # ...
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
```

在每次请求前运行`ping`, 使用`auth`蓝本中的`before_app_request`进行修饰

`app/auth/views.py`：更新已登录用户的访问时间

```python
@auth.before_app_request
def before_request():
    if current_user.is_authenticated():
        current_user.ping()
        if not current_user.confirmed \
        and request.endpoint[:5] != 'auth.':
            return redirect(url_for('auth.unconfirmed'))
```

#### 10.2 用户资料页面

添加用户资料页面

* 添加资料页面的路由

  `app/main/views.py`

  ```python
  @main.route('/user/<username>')
  def user(username):
      user = User.query.filter_by(username=username).first()
      if user is None:
          abort(404)
          return render_template('user.html', user=user)
  ```

* 添加用户资料页面的模板

  `app/templates/user.html`

  ```html
  {% block page_content %}
  <div class="page-header">
      <h1>{{ user.username }}</h1>
      {% if user.name or user.location %}
      <p>
          {% if user.name %}{{ user.name }}{% endif %}
          {% if user.location %}
          From <a href="http://maps.google.com/?q={{ user.location }}">
          {{ user.location }}
          </a>
          {% endif %}
      </p>
      {% endif %}
      {% if current_user.is_administrator() %}
      <p><a href="mailto:{{ user.email }}">{{ user.email }}</a></p>
      {% endif %}
      {% if user.about_me %}<p>{{ user.about_me }}</p>{% endif %}
      <p>
          Member since {{ moment(user.member_since).format('L') }}.
          Last seen {{ moment(user.last_seen).fromNow() }}.
      </p>
  </div>
  {% endblock %}
  ```

* 添加快捷访问链接

  `app/templates/base.html`

  ```html
  {% if current_user.is_authenticated() %}
  <li>
      <a href="{{ url_for('main.user', username=current_user.username) }}">
          Profile
      </a>
  </li>
  {% endif %}
  ```


#### 10.3 资料编辑器

##### 10.3.1 用户级别的资料编辑器

* 资料编辑表单

  `app/main/forms.py`：资料编辑表单

  ```python
  class EditProfileForm(Form):
      name = StringField('Real name', validators=[Length(0, 64)])
      location = StringField('Location', validators=[Length(0, 64)])
      about_me = TextAreaField('About me')
      submit = SubmitField('Submit')
  ```

* 资料编辑路由

  `app/main/views.py`：资料编辑路由

  ```python
  @main.route('/edit-profile', methods=['GET', 'POST'])
  @login_required
  def edit_profile():
      form = EditProfileForm()
      if form.validate_on_submit():
          current_user.name = form.name.data
          current_user.location = form.location.data
          current_user.about_me = form.about_me.data
          db.session.add(current_user)
          flash('Your profile has been updated.')
          return redirect(url_for('.user', username=current_user.username))
      form.name.data = current_user.name
      form.location.data = current_user.location
      form.about_me.data = current_user.about_me
      return render_template('edit_profile.html', form=form)
  ```

* 在用户资料页面中添加一个编辑页面的链接

  `app/templates/user.html`：资料编辑的链接

  ```html
  {% if user == current_user %}
  <a class="btn btn-default" href="{{ url_for('.edit_profile') }}">
      Edit Profile
  </a>
  {% endif %}
  ```

##### 10.3.2 管理员级别的资料编辑器

管理员处理普通用户的基本编辑功能，还需要能编辑用户的电子邮件、用户名、确认状态和角色

* 管理员使用的资料编辑表单

  `app/main/forms.py`：管理员使用的资料编辑表单

  ```python
  class EditProfileAdminForm(Form):
      email = StringField('Email', validators=[Required(), Length(1, 64),
                                               Email()])
      username = StringField('Username', validators=[
          Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                            'Usernames must have only letters, '
                                            'numbers, dots or underscores')])
      confirmed = BooleanField('Confirmed')
      role = SelectField('Role', coerce=int)
      name = StringField('Real name', validators=[Length(0, 64)])
      location = StringField('Location', validators=[Length(0, 64)])
      about_me = TextAreaField('About me')
      submit = SubmitField('Submit')
      def __init__(self, user, *args, **kwargs):
          super(EditProfileAdminForm, self).__init__(*args, **kwargs)
          self.role.choices = [(role.id, role.name)
                               for role in Role.query.order_by(Role.name).all()]
          self.user = user
          def validate_email(self, field):
              if field.data != self.user.email and \
              User.query.filter_by(email=field.data).first():
                  raise ValidationError('Email already registered.')
                  def validate_username(self, field):
                      if field.data != self.user.username and \
                      User.query.filter_by(username=field.data).first():
                          raise ValidationError('Username already in use.')
  ```

* 管理员的资料编辑路由

  `app/main/views.py`：管理员的资料编辑路由

  ```python
  @main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
  @login_required
  @admin_required
  def edit_profile_admin(id):
      user = User.query.get_or_404(id)
      form = EditProfileAdminForm(user=user)
      if form.validate_on_submit():
          user.email = form.email.data
          user.username = form.username.data
          user.confirmed = form.confirmed.data
          user.role = Role.query.get(form.role.data)
          user.name = form.name.data
          user.location = form.location.data
          user.about_me = form.about_me.data
          db.session.add(user)
          flash('The profile has been updated.')
          return redirect(url_for('.user', username=user.username))
      form.email.data = user.email
      form.username.data = user.username
      form.confirmed.data = user.confirmed
      form.role.data = user.role_id
      form.name.data = user.name
      form.location.data = user.location
      form.about_me.data = user.about_me
      return render_template('edit_profile.html', form=form, user=user)
  ```

* 在用户资料页面添加链接按钮

  `app/templates/user.html`：管理员是哦那个的资料编辑链接

  ```html
  {% if current_user.is_administrator() %}
  <a class="btn btn-danger"
     href="{{ url_for('.edit_profile_admin', id=user.id) }}">
      Edit Profile [Admin]
  </a>
  {% endif %}
  ```

#### 10.4 用户头像

使用`Gravatar`提供的用户头像服务

* 生成`Gravatar URL`

  ```python
  import hashlib
  from flask import request
  
  class User(UserMixin, db.Model):
      # ...
      def gravatar(self, size=100, default='identicon', rating='g'):
          if request.is_secure:
              url = 'https://secure.gravatar.com/avatar'
              else:
                  url = 'http://www.gravatar.com/avatar'
                  hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
                  return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
                      url=url, hash=hash, size=size, default=default, rating=rating)
  ```

* 在资料页面中添加头像的链接

  ```html
  <img class="img-rounded profile-thumbnail" src="{{ user.gravatar(size=256) }}">
  ```



### 第11章 博客文章

本章实现的主要功能：

* 允许用户阅读、撰写博客文章

学到的技术：

* 重用模板
* 分页显示长列表
* 处理富文本

#### 11.1 提交和显示博客文章

**1. 为支持博客文章，创建`文章模型`**

`app/models.py`：文章模型

```python
class Post(db.Modle):
    __tablename__ = 'Post'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=detetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    
class User(UserMixin, db.Model):
    # ...
    posts = db.relationship('Post', backref='author', lazy='dynamic')
```

**2. 在程序的首页要显示一个表单，以便让用户写博客**

`app/main/forms.py`：博客文章表单

```python
class PostForm(Form):
    body = TextAreaField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')
```

**3. `index()`是视图函数处理表单并把一起发布的博客文章列表传递给模板**

`app/main/views.py`：处理博客文章的首页路由

```python
@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    post = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', form=form, posts=posts)
```

**4. 显示博客文章的首页模板**

`app/templates/index.html`：显示博客文章的首页模板

```html
{% extends "base.html" %}

...

<div>
    {% if current_user.can(Permission.WRITE) %}
    {{ wtf.quick_form(form) }}
    {% endif %}
</div>
<ul class="posts">
    {% for post in posts %}
    <li class="post">
        <div class="post-thumbnail">
            <a href="{{ url_for('.user', username=post.author.username) }}">
                <img class="img-rounded profile-thumbnail" src="{{ post.author.gravatar(size=40) }}">
            </a>
        </div>
        <div class="post-content">
            <div class="post-date">{{ moment(post.timestamp).fromNow() }}</div>
            <div class="post-author"><a href="{{ url_for('.user', username=post.author.username) }}">{{ post.author.username }}</a></div>
            <div class="post-body">{{ post.body }}</div>
        </div>
    </li>
    {% endfor %}
</ul>

{% endblock %}
```

* 博客文章列表通过HTML无序列表实现，并指定了一个CSS类，从而让格式更精美（不过我测试保存了style.css文件，没有看到格式变化的效果）

#### 11.2 在资料页中显示博客文章

改进用户资料页，在上面显示该用户发布的博客文章列表

`app/main/views.py`：获取博客文章的资料页路由

```python
@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)
```

和`index.html`模板一样，`user.html`模板页要使用一个博客文章列表的HTML片段，为了避免维护两个相同的HTML片段，将该片段保存到`_post.html`中，配合`Jinja2`提供的`include()`指令来使用：

`app/templates/user.html`：显示有博客文章的资料页模板

```html
    <h3>Posts by {{ user.username }}<h3>
    {% include '_posts.html' %}
```

#### 11.3 分页显示长博客文章列表

##### 11.3.1 创建虚拟博客文章数据

**1. 生成虚拟数据的库`ForgeryPy`**

* 利用`ForgeryPy`库生成虚拟信息

* `ForgeryPy` 库并不是这个程序的依赖，只是在开发过程中使用，为了区分生产环境的依赖和开发环境的依赖，我们可以把文件`requirements.txt`换成`requirements`文件夹，里面依次存放：

  * `dev.txt`列出开发过程中所需的依赖

  * `prod.txt`列出生产生产环境所需的依赖

  * `common.txt`列出两个环境所需的相同依赖，在`dev.txt`和`prod.txt`中使用`-r`参数导入

    * 如`dev.txt`:

      ```txt
      -r common.txt
      ForgeryPy==0.1
      ```

**2. 在`User`和`Post`模型中添加生成虚拟数据的类方法**

`app/models.py`：生成虚拟用户和博客文章

```python
class User(UserMixin, db.Model):
	# ...
        @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(True),
                     password=forgery_py.lorem_ipsum.word(),
                     confirmed=True,
                     name=forgery_py.name.full_name(),
                     location=forgery_py.address.city(),
                     about_me=forgery_py.lorem_ipsum.sentence(),
                     member_since=forgery_py.date.date(True))
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                

class Post(db.Model):
    # ...
    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            p = Post(body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                    timestamp=forgery_py.date.date(True),
                    author=u)
            db.session.add(p)
            db.session.commit()

```

* 使用`ForgeryPy`随机生成这些信息会有重复的风险，提交数据库会话时会抛出`IntegrityError`异常，这个异常的处理方式时，在继续操作之前回滚会话，重复的数据不会提交数据库，因此虚拟的数据可能会比预期的少。

**3. 在Python shell 中生成虚拟数据**

```
(venv) $ python manage.py shell
>>> User.generate_fake(100)
>>> Post.generate_fake(100)
```

##### 11.3.2 在页面中渲染数据

修改首页路由，支持分页功能

`app/main/views.py`：分页显示博客文章列表

```python
@main.route('/', methods=['GET', 'POST'])
def index():
    # ...
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
    return render_template('index.html', form=form, posts=posts,
                            paginate=pagination)
```

##### 11.3.3 添加分页导航

**1. 分页对象`Pagination`**

`paginate()`方法的返回值是个`Pagination`类对象，这个对象包含很对属性

分页对象的属性简介在表11-1中（详见P121页）

**2. 构建模板宏**

```html
{% macro pagination_widget(pagination, endpoint) %}
<ul class="pagination">
    <li{% if not pagination.has_prev %} class="disabled"{% endif %}>
        <a href="{% if pagination.has_prev %}{{ url_for(endpoint, page=pagination.prev_num, **kwargs) }}{% else %}#{% endif %}">
            &laquo;
        </a>
    </li>
    {% for p in pagination.iter_pages() %}
        {% if p %}
            {% if p == pagination.page %}
            <li class="active">
                <a href="{{ url_for(endpoint, page = p, **kwargs) }}">{{ p }}</a>
            </li>
            {% else %}
            <li>
                <a href="{{ url_for(endpoint, page = p, **kwargs) }}">{{ p }}</a>
            </li>
            {% endif %}
        {% else %}
        <li class="disabled"><a href="#">&hellip;</a></li>
        {% endif %}
    {% endfor %}
    <li{% if not pagination.has_next %} class="disabled"{% endif %}>
        <a href="{% if pagination.has_next %}{{ url_for(endpoint, page=pagination.next_num, **kwargs) }}{% else %}#{% endif %}">
            &raquo;
        </a>
    </li>
</ul>
{% endmacro %}

```

**3. `index.html`和`user.html`中添加`pagination_widget`**

```html
{% extends "base.html" %}
{% import "bootstrap/wtf.html" as wtf %}
{% import "_macros.html" as macros %}
...
{% include '_posts.html' %}
<div class="pagination">
 {{ macros.pagination_widget(pagination, '.index') }}
</div>
{% endif %}
```



##### 11.4 使用Markdown和Flask-PageDown支持富文本文章

对输入文章的多行文本输入框升级，让其支持`Markdown`语法，并且添加富文本文章的预览功能

实现这个功能用到的一些新包:

* PageDown: 使用JavaScript实现的客户端Markdown到HTML的转换程序
* Flask-PageDown:为 Flask 包装的 PageDown，把 PageDown 集成到 Flask-WTF 表单中
* Markdown：使用 Python 实现的服务器端 Markdown 到 HTML 的转换程序
* Bleach：使用 Python 实现的 HTML 清理器

安装:

` pip install flask-pagedown markdown bleach`

###### 11.4.1 使用Flask-PageDown

Flask-PageDown扩展了一个`PageDownField`类，和WTForms中的`TextAreaField`接口一致

使用`PageDownField`字段之前，先要初始化扩展

`app/__init__.py`：初始化Flask-PageDown

```python
from flask.ext.pagedown import PageDown
# ...
pagedown = PageDown()
# ...
def create_app(config_name):
    # ...
    pagedown.init_app(app)
    # ...
```

修改`PostForm`表单中的`body`字段，支持`Markdown`富文本编辑器

`app/main/forms.py`：启用Markdown的文章表单

```python
from flask.ext.pagedown.fields import PageDownField

class PostForm(Form):
    body = PageDownField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')
```

`Flask-PageDown`提供了一个模板宏，从CDN中加载所需文件。修改模板，支持Markdown预览

`app/templates/index.html`：Flask-PageDown模板声明

```html
{% block scripts %}
{{ super() }}
{{ pagedown.include_pagedown() }}
{% endblock %}
```

###### 11.4.2 在服务器上处理富文本

为了安全起见，只提交Markdown源文本，在服务器上使用Markdown（使用Python编写的Markdown到HTML转换程序）将其转换成HTML。得到HTML后，再使用Bleach进行清理，确保其中只包含几个允许使用的HTML标签。

修改Post模型

`app/models.py`：在Post模型中处理Markdown文本

```python
class Post(db.Model):
		#...        
    	@staticmethod
        def on_changed_body(target, value, oldvalue, initiator):
            allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                            'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                            'h1', 'h2', 'h3', 'p']
            target.body_html = bleach.linkify(bleach.clean(
                                    markdown(value, output_format='html'),
                                    tags=allowed_tags, strip=True))

db.event.listen(Post.body, 'set', Post.on_changed_body)


```

* on_changed_body 函数注册在 body 字段上，是 SQLAlchemy“set”事件的监听程序，这意味着只要这个类实例的 body 字段设了新值，函数就会自动被调用
* on_changed_body 函数把 body 字段中的文本渲染成 HTML 格式，结果保存在 body_html 中，自动且高效地完成Markdown 文本到 HTML 的转换。

在模板中使用文章内容的HTML格式

`app/templates/_posts.html`

```html
...
            <div class="post-body">
                {% if post.body_html %}
                    {{ post.body_html | safe }}
                {{% else %}}
                    {{ post.body }}
                {% endif %}
            </div>
...
```

注：测试修改之后，头像会消失掉，暂时不知道原因

##### 11.5 博客文章的固定链接

支持能在社交网络中分享某篇博客文章的链接，为此，每篇文章都要有一个专页，使用唯一的URL引用。

支持固定链接功能的路由和视图函数

`app/main/views.py`：文章的固定链接

```python
@man.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post]
```

* 这里必须传入一个列表作为参数，这个列表就是要渲染的文章。这里必须传入列表，因为只有这样，`index.html`和`user.html0`引用的`_posts.html`模板才能在这个页面中使用

固定链接添加到通用模板_posts.html中

`app/templates/_posts.html`：文章的固定链接

```html
<ul class="posts">
 {% for post in posts %}
 <li class="post">
 ...
 <div class="post-content">
 ...
 <div class="post-footer">
 <a href="{{ url_for('.post', id=post.id) }}">
 <span class="label label-default">Permalink</span>
 </a>
 </div>
 </div>
 </li>
 {% endfor %}
</ul>
```

渲染固定链接页面的post.html模板

`app/templates/post.html`：固定链接模板

```html
{% extends "base.html" %}
{% block title %}Flasky - Post{% endblock %}
{% block page_content %}
{% include '_posts.html' %}
{% endblock %}
```

##### 11.6 博客文章编辑器

实现一个文章编辑器，允许用户编辑自己的文章。博客文章编辑器显示在单独的页面中。

`app/templates/edit_post.html`：编辑博客文章的模板

```html

```

编辑博客文章的路由：

`app/main/views.py`

```html

```

为了功能完整，可以在每篇博客文章的下面、固定链接的旁边添加一个指向编辑页面的链接

`app/templates/_posts.html`：编辑博客文章的链接

```html

```




## 备注

* github链接地址:

  ```
  https://github.com/miguelgrinberg/flasky.git
  ```

* flask是web框架，如果不用web服务器直接部署和配合web服务器（如Nginx）部署，有什么区别？

  * 在2.4有个提示：Flask提供的Web服务器不适合在生成环境中使用。第17章会介绍生产环境Web服务器。

* flask是如何使用上下文在多线程的环境中，让某个变量成为某一线程的全局可访问变量

* 使用缓冲的MD5值生成Gravatar URL

  ```python
  class User(UserMixin, db.Model):
      # ...
      avatar_hash = db.Column(db.String(32))
      def __init__(self, **kwargs):
          # ...
          if self.email is not None and self.avatar_hash is None:
              self.avatar_hash = hashlib.md5(
                  self.email.encode('utf-8')).hexdigest()
              def change_email(self, token):
                  # ...
                  self.email = new_email
                  self.avatar_hash = hashlib.md5(
                      self.email.encode('utf-8')).hexdigest()
                  db.session.add(self)
                  return True
              def gravatar(self, size=100, default='identicon', rating='g'):
                  if request.is_secure:
                      url = 'https://secure.gravatar.com/avatar'
                      else:
                          url = 'http://www.gravatar.com/avatar'
                          hash = self.avatar_hash or hashlib.md5(
                              self.email.encode('utf-8')).hexdigest()
                          return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
                              url=url, hash=hash, size=size, default=default, rating=rating)
  ```




















