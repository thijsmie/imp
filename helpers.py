from application import db
from models import Product, Transaction


def many_to_many(name, fromtable, totable):
    lfromtable = fromtable.lower()
    ltotable = totable.lower()
    table = db.Table(name,
        db.Column(ltotable + '_id', db.Integer, db.ForeignKey(totable + '.id')),
        db.Column(lfromtable + '_id', db.Integer, db.ForeignKey(fromtable + '.id'))
    )
    
    return db.relationship(totable, secondary=table,
        backref=db.backref(lfromtable+'s', lazy='dynamic'))
    
class Base(db.Model):
    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime,  
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
        
    def __repr__(self):
        return '<'+self.__class__.__name__+': {}>'.format(self.id)



def add_transaction_row(transaction, row):
    product = Product.query.filter_by(id=row['product']).first()

    if product == None:
        return (False, "JsonException: Unknown product: "+str(row['product']))

    try:
        if row["type"] == "gain":
            if not 'value' in row:
                return (False, "JsonException: field 'value' not specified")
            transaction.gain(row['product'], row['amount'], row['value'])
        else:
            if 'value' in row:
                transaction.loss(row['product'], row['amount'], row['value'])
            else:
                transaction.loss(row['product'], row['amount'])
    except e:
        return (False, e)
        
    return (True, "")

def calculate_transaction_totals(transaction):
    producttotals = {}
    _modtotals = {}
    total = 0.
    
    for row in transaction.rows:
        if row.product.group in producttotals:
            producttotals[row.product.group] += row.value
        else:
            producttotals[row.product.group] = row.value
        
        total += row.value
        
        if row.value < 0:
            mods = row.product.losemods
        elif row.value > 0:
            mods = row.product.gainmods
            
        for mod in mods:
            if not mod in row.exclude_mods:
                modvalue = mod.apply(row.amount, row.value)
                if mod.name in modtotals:
                    _modtotals[mod] += modvalue
                else:
                    _modtotals[mod] = modvalue
    
    modtotals = {}
    for k, v in _modtotals.iteritems():
        modtotals[k.name] = round(v)
        if not k.included:
            total += round(v)
            
    return {'total': total, 'producttotals': producttotals, 'modtotals': modtotals}

def transaction_row_as_dict(row):
    retdict = {}
    retdict["index"] = row.id
    retdict["productindex"] = row.product.id
    retdict["productname"] = row.product.name
    retdict["amount"] = row.amount
    retdict["value"] = row.value
    retdict["excludemods"] = [mod.name for mod in row.excludemods]
    
    return retdict
    
def transaction_as_dict(transaction):
    retdict = {}
    retdict["index"] = transaction.id
    retdict["eventname"] = transaction.eventname
    retdict["eventnumber"] = transaction.eventnumber
    retdict["eventdate"] = transaction.eventdate.strftime('%Y-%m-%d')
    retdict["eventcontact"] = transaction.eventcontact
    retdict["eventnotes"] = transaction.eventnotes
    retdict["relation"] = transaction.relation.name
    retdict["rows"] = []
    
    for row in transaction.rows:
        retdict["rows"].append(transaction_row_as_dict(row))
        
    retdict.update(calculate_transaction_totals(transaction))
    
    return retdict
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
