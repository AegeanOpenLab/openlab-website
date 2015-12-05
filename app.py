from datetime import datetime
from flask import Flask, render_template

from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
@app.route('/index')
def index():
    now = datetime.now()
    return render_template('index.html', now=now)

if __name__ == '__main__':
    app.run(debug=True)
