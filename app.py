from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, url_for, redirect

from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

from flask.ext.wtf import Form
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask.ext.login import login_user, logout_user, login_required

# Configurations
app = Flask(__name__)
# secret key (dummy random generator)
import os
app.config['SECRET_KEY'] = os.urandom(24)
# db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///openlab-dev.db'
db = SQLAlchemy(app)
# bootstrap
bootstrap = Bootstrap(app)
# login_manager
lm = LoginManager(app)
lm.login_view = 'login'

# models (database tables)
# Note: Next line import is not PEP8,exists only to denote class inheritance
from flask.ext.login import UserMixin
# User Model is just a python class that includes ext.login UserMixin
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # Note: username index=True optimize db search matching, use it with caution
    username = db.Column(db.String(16), index=True, unique=True)
    password_hash = db.Column(db.String(64))

    def set_password(self, password):
        # Encrypt user password
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        # Decrypt user password
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def register(username, password):
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    body = db.Column(db.String(300))

    def __repr__(self):
        return '<Post: id:{}>'.format(self.id)

# Form
class PostForm(Form):
    title = StringField('Enter Title: ', validators=[DataRequired()])
    body = StringField('Enter Body: ', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired(), Length(1, 16)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
# load_user for: from flask.ext.login import current_user

# views (routes)
# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            return redirect(url_for('login', **request.args))
        login_user(user, form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

# logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# index
@app.route('/')
@app.route('/index')
def index():
    now = datetime.now()
    posts = Post.query.all()
    return render_template('index.html', now=now, posts=posts)

# single-post view
@app.route('/post/<int:id>')
@login_required
def single_post(id):
    post = Post.query.get(id)
    return render_template('single-post.html', post=post)

# add post
@app.route('/post/add/', methods=['POST', 'GET'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        p = Post(title=form.title.data, body=form.body.data)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('post-form.html', form=form)

# edit post
@app.route('/post/edit/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_post(id):
    post = Post.query.get(id)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('post-form.html', form=form)

# delete post
@app.route('/post/delect/<int:id>')
@login_required
def delete_post(id):
    p = Post.query.get(id)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('index'))

# run app
if __name__ == '__main__':
    # create db if not exists
    db.create_all()
    # add dummy user with credentials - (username) goofy | super ( password).
    if User.query.filter_by(username='goofy').first() is None:
        User.register('goofy', 'super')
    # populate db with dummy data is None Post record exists.
    if Post.query.count() == 0:
        post1 = Post(title="Openlab code page",
                     body="https://github.com/AegeanOpenLab/")
        post2 = Post(title="Flask Sqlachemy Docs link",
                     body="http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#a-minimal-application.")
        db.session.add(post1)
        db.session.add(post2)
        db.session.commit()
    app.run(debug=True)
