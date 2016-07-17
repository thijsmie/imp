from models import db

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))
    transactionID = db.Column(db.Integer, db.ForeignKey("transaction.id"))