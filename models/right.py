from models import db

class Right(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.String(db.String)