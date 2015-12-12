from datetime import datetime
from flask import Flask, render_template

from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy

# Configurations
app = Flask(__name__)
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


# views (routes)
@app.route('/')
@app.route('/index')
def index():
    now = datetime.now()
    posts = Post.query.all()
    return render_template('index.html', now=now, posts=posts)

@app.route('/post/<int:id>')
def single_post(id):
    post = Post.query.get(id)
    return render_template('single-post.html', post=post)

# add post
@app.route('/post/add/')
def add_post():
    return "add post"

# edit post
@app.route('/post/edit/<int:id>')
def edit_post(id):
    return "edit post"

# delete post
@app.route('/post/delect/<int:id>')
def delete_post(id):
    return "delete post"

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
