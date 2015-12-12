from datetime import datetime
from flask import Flask, render_template, url_for, redirect

from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

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

# models (database tables)
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

# views (routes)
@app.route('/')
@app.route('/index')
def index():
    now = datetime.now()
    posts = Post.query.all()
    return render_template('index.html', now=now, posts=posts)

# single-post view
@app.route('/post/<int:id>')
def single_post(id):
    post = Post.query.get(id)
    return render_template('single-post.html', post=post)

# add post
@app.route('/post/add/', methods=['POST', 'GET'])
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
def delete_post(id):
    p = Post.query.get(id)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('index'))

# run app
if __name__ == '__main__':
    # create db if not exists
    db.create_all()
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
