
### AegeanOpenLab-website

#### Description

A basic and fairly simple website, powered by [Flask](http://flask.pocoo.org/) and using the following extensions:

1. [Flask-Bootstrap](https://pythonhosted.org/Flask-Bootstrap/)
2. [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/)
3. [Flask-Login](https://flask-login.readthedocs.org/en/latest/)

#### Commit List (Tutorial Guide)

1. [Initial Commit](https://github.com/kickapoo/openlab-website/commit/8895c9346d739cf3464dbddd053d9a498d413c92)
    Nothing fancy. Just initialize repo with README.md, Licence and .gitignore.
2. [Update README] (https://github.com/kickapoo/openlab-website/commit/e335d3f57ae4918edec2a6cbf712fd807f9dcd09) Nothing fancy. Just a minor example in classroom on how git push works.
3. [Initial Setup - "Hello from index"]() Expanding Flask 'Hello World' example with `render_template`.
4. [Add flask-bootstrap extension](https://github.com/kickapoo/openlab-website/commit/31d183f32141ca193eaca0c4ae0f9c279dee4347)  Exploring templates with bootstrap. `base.html` is our layout basic file. Every templates `html` file `extends` from `base.html`.
5. [Add SQAlchemy extension - database](https://github.com/kickapoo/openlab-website/commit/f1a968039dfa1e129b632ad1055d75644eb09d8a) Adding a database (sqlite3) and using `SQLAlchemy` as our [ORM](https://en.wikipedia.org/wiki/Object-relational_mapping). A simple 'Title/Body' Post model is used as an example.
6. [Add WTF forms](https://github.com/kickapoo/openlab-website/commit/1d0967f02e3b8d79dbf60baa2df4d7a190537f7f) Adding basic database CRUD jobs [UI](https://en.wikipedia.org/wiki/User_interface) for Post model.
7. [Add Flask-Login](https://github.com/kickapoo/openlab-website/commit/2482c1082e364d3faa1aafd34b8dfce061f93773) Only registered user can perform database interaction with Post model.

#### Run a local instance

Pre-requirements: [Python 2.7](http://docs.python-guide.org/en/latest/), [Python-virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/), [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

Steps:

1. `git clone https://github.com/AegeanOpenLab/openlab-website.git`
2. `cd openlab-website`
3. `$ virtualenv openlab-venv`
4. `$ source opelab-venv/bin/activate` or (Windows) `opelab-venv\Scripts\activate\`
5. `$ pip install -r requirements.txt`
6. `$ python app.py`

### Enjoy ... FLASK is Awesome !!!

[Anastasiadis Stavros] (http://fuzzyelements.com/)
