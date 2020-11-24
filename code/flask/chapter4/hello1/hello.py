from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
# from flask_bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask import session, redirect, url_for, flash


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('submit')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     name = None
#     form = NameForm()
#     if form.validate_on_submit():
#         name = form.name.data
#         form.name.data = ''
#     return render_template('index.html', form=form, name=name)

# # Post/重定向/Get模式; 会话
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     form = NameForm()
#     if form.validate_on_submit():
#         session["name"] = form.name.data
#         return redirect(url_for('index'))
#     return render_template('index.html', form=form, name=session.get('name'))


# Flask消息
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name')
        session["name"] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
