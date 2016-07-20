from functions import request
from models import db, Transaction

def performTransaction(req, user):
    validated, result = request.DictValidator(req, request.rTransaction)
    if not validated:
        return (False, 422, "Request had a missing or invalid keyvalue:" + result)
            
    # Create transaction and add parsed properties        
    transaction = Transaction()   
    transaction.eventname = result["eventname"]
    transaction.eventdate = result["eventdate"]
    transaction.contact = result["contact"]
    transaction.relationFrom = result["relationFrom"]
    transaction.relationTo = result["relationTo"]
    
    for stock in result["stocks"]:
        transaction.stocks.append(stock)

    # Check for optional arguments
    if "notes" in req:
        validatednotes, resultnotes = request.DictValidator(req, request.rTransactionNotes)
        if not validatednotes:
            return (False, 422, "Request had a missing or invalid keyvalue:" + resultnotes)
        for note in resultnotes["notes"]:
            transaction.notes.append(note)
            
    if "viewRights" in req:
        validatedviewrights, resultviewrights = request.DictValidator(req, request.rTransactionViewRights)
        if not validatedviewrights:
            return (False, 422, "Request had a missing or invalid keyvalue:" + resultviewrigths)
        for viewRight in resultnotes["viewRights"]:
            transaction.viewRights.append(viewRight)
    
    db.session.add(transaction)
     
                    
            
