from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    now = datetime.now()
    return render_template('index.html', now=now)

if __name__ == '__main__':
    app.run(debug=True)