from models import db

productbuymargins = db.Table('productbuymargins',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
    db.Column('margin_id', db.Integer, db.ForeignKey('margin.id'))
)
productsellmargins = db.Table('productsellmargins',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
    db.Column('margin_id', db.Integer, db.ForeignKey('margin.id'))
)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    
    # Nonphysical products are allowed to spawn Stocks out of nothing
    isPhysical = db.Column(db.Boolean)
    
    # Default margins to be applied on buying and selling
    buyDefaultMargins = db.relationship('Margin', secondary=productbuymargins, uselist=True)
    sellDefaultMargins = db.relationship('Margin', secondary=productsellmargins, uselist=True)
    
    # The relation that tracks corrections
    correctionRelationID = db.Column(db.Integer, db.ForeignKey('relation.id'))
    correctionRelation = db.relationship('Relation',
        backref=db.backref('correctionproducts', lazy='dynamic', uselist=True),
        uselist=False)