from application import db, many_to_many, Base

sign = lambda x: math.copysign(1, x)


# Convention: the sign of a number in the database 
# is always relative to the owner of this program
# So a negative amount and value is a sell (and denoted with 'lose')
# and a positive amount and value is a buy (and denoted with 'gain')
# From outside, you call 'lose' or 'gain' with a positive number always.

class IllegalProductAdaption(Exception):
    pass
    
class Product(Base):
    name = db.Column(db.String(80))
    amount = db.Column(db.Integer)
    value = db.Column(db.Integer)
    
    allow_negative = db.Column(db.Boolean)
    value_constant = db.Column(db.Boolean)
    hidden = db.Column(db.Boolean)
    
    losemods = many_to_many('losemods','Product', 'Mod')
    gainmods = many_to_many('gainmods','Product', 'Mod')
    
    group = db.Column(db.String(80))
    
    def __init__(self):
        pass
        
    def lose(self, amount, value=None):
        if amount <= 0:
            raise IllegalProductAdaption("Incorrect call of function 'lose', amount cannot be zero/negative.")
            
        if amount > self.amount and not allow_negative:
            raise IllegalProductAdaption(str(self) + " would have negative stock.")
            
        if self.value_constant:
            dvalue = amount * self.value
        elif value != None:
            if value > self.value:
                raise IllegalProductAdaption(str(self) + "would have negative value.")
            dvalue = value
        else:
            dvalue = round(amount / self.amount * self.value)
        
        self.value -= dvalue
        self.amount -= amount
        return dvalue
        
    def gain(self, amount, value):
        if amount <= 0 or value < 0:
            raise IllegalProductAdaption("Incorrect call of function 'gain', amount cannot be zero/negative.")
            
        if self.value_constant:
            if value != amount * self.value:
                raise IllegalProductAdaption(str(self) + " has a constant price that is not matched.")
            self.amount += amount
        else:
            self.value += value
            self.amount += amount
        return value
               
    def change_value(self, dvalue):
        if self.value_constant:
            return self.value * self.amount
        if sign(self.value + dvalue) != sign(self.value) or self.value + dvalue == 0:
            raise IllegalRowAdaption("The value of " + str(self) + " would change sign.")
        self.value += dvalue
        return self.value
        
    def change_amount(self, damount):
        if sign(self.amount + damount) != sign(self.amount) or self.amount + damount == 0:
            if not (self.allow_negative and self.value_constant):
                raise IllegalRowAdaption("The value of " + str(self) + " would change sign.")
        self.amount += damount
        return self.amount
        
        
class Transaction(Base):
    eventname = db.Column(db.String(80))
    eventnumber = db.Column(db.Integer)
    eventdate = db.Column(db.DateTime)
    eventcontact = db.Column(db.String(80))
    eventnotes = db.Column(db.Text)
    
    relation_id = db.Column(db.ForeignKey('relation.id'))
    rows = db.relationship('TransactionRow', backref='transaction', lazy='dynamic')
    
    def __init__(self, eventname, eventdate, eventcontact, relation):
        self.eventname = eventname
        self.eventdate = eventdate
        self.eventcontact = eventcontact
        self.eventnotes = ""
        self.relation = relation
        previous = Transaction.query.filter_by(relation=self.relation, eventnumber=db.func.max(Transaction.eventnumber))
        if previous == None:
            self.eventnumber = 1
        else:
            self.eventnumber = previous.eventnumber + 1
        
    def lose(self, product, amount, value=None):
        for row in rows:
            if row.product == product:
                value = row.lose(amount, value)
                break
        else:       
            value = TransactionRow(self, product).lose(amount, value)
        
        return value
        
    def gain(self, product, amount, value):
        for row in rows:
            if row.product == product:
                value = row.gain(amount, value)
                break
        else:      
            value = TransactionRow(self, product).gain(amount, value)
        
        return value            
            
        
class IllegalRowAdaption(Exception):
    pass
    
    
class TransactionRow(Base):
    transaction_id = db.Column(db.ForeignKey('transaction.id'))
    
    product = db.relationship('Product', lazy='joined')
    product_id = db.Column(db.ForeignKey('product.id'))
    
    amount = db.Column(db.Integer)
    value = db.Column(db.Integer)
    
    exclude_mods = many_to_many('excludemods','TransactionRow', 'Mod')
    
    def __init__(self, transaction, product):
        self.transaction = transaction
        self.product = product
        self.value = 0
        self.amount = 0
    
    def lose(self, amount, value=None): # selling more, buying less
        dvalue = product.lose(amount, value)
        self.value -= dvalue
        self.amount -= amount
        return dvalue
        
    def gain(self, amount, value): # selling less, buying more
        self.amount += amount
        self.value += value
        product.gain(amount, value)
        return value
        
    def change_value(self, value):
        dvalue = self.value - value
        product.change_value(dvalue)
        self.value = value
        return dvalue

    def change_amount(self, amount):
        if sign(amount) != sign(self.amount) or amount == 0:
            raise IllegalRowAdaption("The amount of " + str(self) + " would change sign.")
        damount = self.amount - amount
        product.change_amount(damount)
        self.amount = amount
        return damount
        
    def delete(self):
        if self.value < 0:
            product.gain(-self.amount, -self.value)
        elif self.value > 0:
            product.change_amount(-self.amount)
            product.change_value(-self.value)
        elif self.amount != 0:
            product.change_amount(-self.amount)
    
    
class Mod(Base):
    # nvalue = (ovalue + pre_add * amount)*multiplier + post_add * amount
    name = db.Column(db.String)
    pre_add = db.Column(db.Integer)
    multiplier = db.Column(db.Float)
    post_add = db.Column(db.Integer)
    included = db.Column(db.Boolean)
    
    def __init__(self, name, pre_add, multiplier, post_add, included):
        self.name = name
        self.pre_add = pre_add
        self.multiplier = multiplier
        self.post_add = post_add
        self.included = included
    
    def apply(self, amount, value):
        if (included):
            return apply_included(amount, value)
        else:
            return apply_excluded(amount, value)
            
    def apply_included(self, amount, value):
        # The mod is already included in the value, we would just like to know it's total
        # Note: this is inexact science, since value might be rounded, so the error
        # scales with the multiplier and possible decimals in post and pre-add
        ovalue = value - self.post_add * amount
        ovalue /= self.multiplier
        ovalue -= self.pre_add * amount
        dvalue = value - ovalue
        return value, dvalue
        
    def apply_excluded(self, amount, value):
        nvalue = (value + self.pre_add * amount) * multiplier + self.post_add * amount
        dvalue = nvalue - value
        return nvalue, dvalue
        
    
class Relation(Base):
    name = db.Column(db.String(80))
    budget = db.Column(db.Integer)
    email = db.Column(db.String(200))
    
    send_transaction = db.Column(db.Boolean)
    send_transaction_updates = db.Column(db.Boolean)
    send_budget_warnings = db.Column(db.Boolean)    
    
    transactions = db.relationship('Transaction', backref='relation', lazy='dynamic')
    
    def __init__(name, email):
        self.name = name
        self.email = email
        self.budget = 0.
        self.send_transaction = True
        self.send_transaction_updates = True
        self.send_budget_warnings = True
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
