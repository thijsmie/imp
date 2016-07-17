from models import db
from fractions import gcd

def simplifyfraction(numerator, denominator):
    wholepartnumerator = (numerator - numerator % denominator)
    numerator -= wholepartnumerator
    numdenomgcd = gcd(numerator, denominator)
    return (wholepartnumerator / denominator, numerator / numdenomgcd, denominator / numdenomgcd)
    
def multiplyfractions(numerator1, denominator1, numerator2, denominator2):
    return simplifyFraction(numerator1 * numerator2, denominator2 * denominator2)
    
    

class IllegalStockSplitException(Exception):
    pass

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    
    # Fancy fraction, actual price cost and fraction for rounding tracking
    price = db.Column(db.Integer)
    priceFractionNumerator = db.Column(db.Integer)
    priceFractionDenominator = db.Column(db.Integer)
    
    # Product type of Stock, immutable
    productID = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product', backref=db.backref('stocks', lazy='dynamic', uselist=True), uselist=False)
        
    # Current owner of Stock, mutable  
    ownerID = db.Column(db.Integer, db.ForeignKey('relation.id'))
    owner = db.relationship('Relation',
        backref=db.backref('stocks', lazy='dynamic', uselist=True),
        uselist=False)
        
    def __init__(self):
        self.priceFractionNumerator = 0
        self.priceFractionDenominator = 0
        
    def splitto(self, amount):
        if (amount >= self.number):
            raise IllegalStockSplitException()
            
        splitstock = Stock()
        splitstock.owner = self.owner
        splitstock.product = self.product
        
        splitstock.number = amount
        
        # Calculate price of new Stocks using fraction calculus
        pricefraction = multiplyfractions(price * priceFractionDenominator + priceFractionNumerator, amount, self.number)
        splitstock.price = pricefraction[0]
        splitstock.priceFractionNumerator = pricefraction[1]
        splitstock.priceFractionDenominator = pricefraction[2]
        
        self.price -= pricefaction[0] + 1
        self.priceFractionNumerator = pricefraction[2] - pricefraction[1]
        self.priceFractionDenominator = pricefaction[2]
        
        return splitstock