from flask import Flask, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.session import Session

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
