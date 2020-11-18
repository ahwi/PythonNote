from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sbu')
def sub():
    return render_template('sub.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.route('/user2/<name>')
def user2(name):
    return render_template('user2.html', name=name)

if __name__ == '__main__':
    app.run()
