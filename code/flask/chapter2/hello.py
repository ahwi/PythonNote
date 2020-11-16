from flask import Flask
from flask import make_response
from flask import redirect
from flask import abort
app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


# # 返回400的状态码，表示请求无效
# @app.route('/')
# def index():
#     return '<h1>Bad Request</h1>', 400


# # 使用make_response()创建一个响应对象并设置cookies
# @app.route('/')
# def index():
#     response = make_response('<h1>This document carries a cookie</h1>')
#     response.set_cookie('answer', '42')
#     return response

# # 使用redirect()函数进行重定向
# @app.route('/')
# def index():
#     return redirect('http://www.example.com')


@app.route("/user/<name>")
def user(name):
    return '<h1>Hello, %s</h1>' % name


# # 使用abort()函数处理错误的异常情况
# @app.route("/user/<id>")
# def get_user(id):
#     abort(404)
#     return '<h1>Hello</h1>'


if __name__ == "__main__":
    app.run(debug=True)
