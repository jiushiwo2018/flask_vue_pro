from flask import Flask, abort, redirect, render_template, make_response, request, url_for, flash, session
from werkzeug.routing import BaseConverter

from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,PasswordField
from wtforms.validators import DataRequired,EqualTo

from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

class Regex_url(BaseConverter):
    def __init__(self, url_map, *args):
        super(Regex_url, self).__init__(url_map)
        self.regex = args[0]


app = Flask(__name__)

app.url_map.converters['re'] = Regex_url
app.config['SECRET_KEY']='1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1:3306/flasktest'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True


toolbar = DebugToolbarExtension(app)


db = SQLAlchemy(app)


@app.route('/user/<int:id>')
def hello_itcast(id):
    return 'hello itcast {}'.format(id)


@app.route('/user2/<re("[a-z]{3}"):id>')
def hello_itcast2(id):
    return 'hello {}'.format(id)


@app.route('/abort')
def hello():
    abort(404)
    return 'hello itcast', 999   # return value, status code


@app.route('/it')
def hello_it():
    return redirect('http://www.baidu.com')


# to return error message/html by status code(abort()by other views)
@app.errorhandler(404)
def error(e):
    return ('page not found{}'.format(e))


@app.route('/hello')
@app.route('/hello/<name>/<int:age>/')
def hello_user(name=None, age=None):
    return render_template('index.html', name=name, age=age)


@app.route('/cookie')
def set_cookie():
    resp = make_response('this is to set cookie')
    resp.set_cookie('username', 'itcast')
    return resp


@app.route('/request')
def resp_cookie():
    resp = request.cookies.get('username')
    return resp


@app.route('/dict')
def dict():
    mydict = {'key': 'silence is gold'}
    mylist = ['Speech', 'is', 'silver']
    myintvar = 0

    return render_template(
        'vars.html',
        mydict=mydict,
        mylist=mylist,
        myintvar=myintvar)


# get url path by view fun name.
@app.route('/urlfor')
def myredirect():
    return url_for('hello_user', name="HAHAHA")
    # return url_for('index', _external=True)


class Login(FlaskForm):
    us = StringField(label=u'user',validators=[DataRequired()])
    ps = PasswordField(label=u'password',validators=[DataRequired(),EqualTo('ps2','err')])
    ps2 = PasswordField(label=u'confirm password',validators=[DataRequired()])
    submit = SubmitField(u'submit')


@app.route('/log',methods=['GET','POST'])
def login():
    form = Login()
    return render_template('login.html',form=form)


@app.route('/index',methods=['GET','POST'])
def index():
    form = Login()
    if form.validate_on_submit():
        name = form.us.data
        pswd = form.ps.data
        pswd2 = form.ps2.data
        print(name,pswd,pswd2)
        return redirect(url_for('login'))
    else:
        if request.method=='POST':
            flash(u'Error message, enter anain!')
        print(form.validate_on_submit())

    return render_template('login.html',form=form)





class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    us = db.relationship('User', backref='role')

    def __repr__(self):
        return 'Role:%s' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64),unique=True)
    pswd = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return 'User:%s' % self.name


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
