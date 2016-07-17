from models import db

relationbuymargins = db.Table('relationbuymargins',
    db.Column('relation_id', db.Integer, db.ForeignKey('relation.id')),
    db.Column('margin_id', db.Integer, db.ForeignKey('margin.id'))
)
relationsellmargins = db.Table('relationsellmargins',
    db.Column('relation_id', db.Integer, db.ForeignKey('relation.id')),
    db.Column('margin_id', db.Integer, db.ForeignKey('margin.id'))
)
relationrights = db.Table('relationrights',
    db.Column('relation_id', db.Integer, db.ForeignKey('relation.id')),
    db.Column('right_id', db.Integer, db.ForeignKey('right.id'))
)

class Relation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    owned = db.Column(db.Boolean)
    name  = db.Column(db.String(200))
    email = db.Column(db.String(200))
    phash = db.Column(db.String(512))
    token = db.Column(db.String(128))
    
    balance = db.Column(db.Integer)
    
    # Default margins to be applied on buying from and selling to this party
    buyDefaultMargins = db.relationship('Margin', secondary=relationbuymargins, uselist=True)
    sellDefaultMargins = db.relationship('Margin', secondary=relationsellmargins, uselist=True)
    
    rights = db.relationship('Right', secondary=relationrights, uselist=True)
    
    def __init__(self, name):
        self.name = name
        self.balance = 0
        self.owned = False
    
    def register(self, email, phash):
        self.owned = True
        self.email = email
        self.phash = phash