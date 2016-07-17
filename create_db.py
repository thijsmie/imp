from flask import Flask
import models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foo.db'
models.db.init_app(app)

with app.app_context():
    models.db.create_all()