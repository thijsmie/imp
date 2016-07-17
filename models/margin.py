from models import db

class Margin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    isPercentage = db.Column(db.Boolean)
    amountNumerator = db.Column(db.Integer)
    amountDenominator = db.Column(db.Integer)