from application import app, db
from models import Product, Transaction
from validation import NewTransactionValidator, EditTransactionValidator
from response import fail, success
from helpers import add_transaction_row, transaction_as_dict

from dateutil import parser


@app.route('/transaction', methods=['POST'])
def create_transaction():
    data = request.json
    try:
        NewTransactionValidator(data)
    except error:
        return fail("JsonException: Incorrect dataformat: "+error.message, 400)
    
    try:
        eventdate = dateutil.parser.parse(data["eventdate"]).date()
    except:
        return fail("JsonException: Incorrect eventdate", 400)
    
    transaction = Transaction(data["eventname"], eventdate, data["eventcontact"])
    
    for row in data["rows"]:
        added, msg = add_transaction_row(transaction, row)
        
        if not added:
            return fail(msg, 400)
    
    db.session.add(transaction)
    db.session.commit()
    return success(transaction_as_dict(transaction))
    
    
@app.route('/transaction', methods=['PUT'])
def update_transaction():
    data = request.json
    try:
        EditTransactionValidator(data)
    except error:
        return fail("JsonException: Incorrect dataformat: "+error.message, 400)
    
    transaction = Transaction.query.get(data['index'])
    
    if (transaction == None):
        return fail("JsonException: Unknown transaction: "+data['index'], 404)
    
    if ("eventdate" in data):
        try:
            eventdate = dateutil.parser.parse(data["eventdate"]).date()
        except:
            return fail("JsonException: Incorrect eventdate", 400)
        transaction.eventdate = eventdate
        
    if ("eventname" in data):
        transaction.eventname = data["eventname"]
    
    if ("eventcontact" in data):
        transaction.eventname = data["eventcontact"]
        
    if ("eventnotes" in data):
        transaction.eventname = data["eventnotes"]

    if ("rows" in data):
        for row in data["rows"]:
            success, msg = add_transaction_row(transaction, row)
            
            if not success:
                return fail(msg, 400)
            
    db.session.add(transaction)
    db.session.commit()
    return success()
    
@app.route('/transaction/{id}', methods=["GET"])
def get_transaction(id):
    transaction = Transaction.query.get(data['index'])
    
    if (transaction == None):
        return fail("JsonException: Unknown transaction: "+id, 404)
        
    return succes(transaction_as_dict(transaction))
    
    
@app.route('/product', methods=["POST"])
def create_product():
    pass
    
@app.route('/product', methods=["PUT"])
def update_product():
    pass
    
@app.route('/product/{id}', methods=["GET"])
def get_product(id):
    pass
    
    
    
          
    
