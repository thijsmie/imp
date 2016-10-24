from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


invoice_input_hooks = []
invoice_edit_hooks = []


import plugins
import api


@app.before_first_request
def first_time_setup():
    import models
    db.create_all()


if __name__ == "__main__":
    app.run()

