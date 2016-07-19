from models import db
import datetime

stockrows = db.Table('stockrows',
    db.Column('transaction_id', db.Integer, db.ForeignKey('transaction.id')),
    db.Column('stock_id', db.Integer, db.ForeignKey('stock.id'))
)
transactionrights = db.Table('transactionrights',
    db.Column('transaction_id', db.Integer, db.ForeignKey('transaction.id')),
    db.Column('right_id', db.Integer, db.ForeignKey('right.id'))
)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trackid = db.Column(db.String(80))
    
    eventname = db.Column(db.String(100))
    eventdate = db.Column(db.Date)
    contact = db.Column(db.String(100))
    
    processingdate = db.Column(db.Date)
    viewRights = db.relationship('Right', secondary=transactionrights, uselist=True)
        
    relationFromID = db.Column(db.Integer, db.ForeignKey('relation.id'))
    relationFrom = db.relationship("Relation", foreign_keys=[relationFromID])
    
    relationToID = db.Column(db.Integer, db.ForeignKey('relation.id'))  
    relationTo = db.relationship("Relation", foreign_keys=[relationToID])
    
    stocks = db.relationship('Stock', secondary=stockrows,
        backref=db.backref('transactions', lazy='dynamic', uselist=True),
        uselist=True)
        
    notes = db.relationship('Note',
        backref=db.backref('transaction', lazy='select', uselist=False),
        uselist=True)
        
    def __init__(self):
        self.processingdate = datetime.date.today()
