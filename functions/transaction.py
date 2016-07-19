from models import db, Transaction, Relation, Stock, Margin, Right, Note
import datetime

transactionDictShouldHave = {"eventname": str, "eventdate": str, "contact": str, 
                "relationFromID": int, "relationToID": int, "stocks": list, "viewRights":list}
stockDictShouldHave = {"productID": int, "number": int}

def validateDict(dictToValidate, validation):
    for k, v in validation.items():
        if not k in dictToValidate:
            return False
        if type(dictToValidate[k]) != v:
            return False 
    return True
    
def validateDate(date):
    date = date.split('-')
    if (len(date) == 3 and len(date[0]) == 4 and len(date[1]) <= 2 and len(date[2]) <= 2):
        try:
            date[0] = int(date[0])
            date[1] = int(date[1])
            date[2] = int(date[2])
            date = datetime.date(date[0], date[1], date[2])
        except:
            return False, 0
        return True, date
    return False, 0
    
    
def performTransaction(transactionDict, relationActor):
    objAddQueue = []

    if not validateDict(transactionDict, transactionDictShouldHave):
        return (False, 422, "Transaction specification incomplete")
    for row in transactionDict["stocks"]:
        if not validateDict(row, stockDictShouldHave):
            return (False, 422, "Stock row specification incomplete")
            
    transaction = Transaction()
    objAddQueue.append(transaction)
    
    transaction.eventname = transactionDict["eventname"]
    gooddate, date = validateDate(transactionDict["date"])
    if not gooddate:
        return (False, 422, "Transaction date invalid")
        
    transaction.eventdate = date
    transaction.contact = transactionDict["contact"]
    
    relationFrom = Relation.query.get(transactionDict["relationFrom"])
    if (relationFrom == 0):
        return (False, 422, "Relation 'From' was invalid")
    relationTo = Relation.query.get(transactionDict["relationTo"])
    if (relationTo == 0):
        return (False, 422, "Relation 'To' was invalid")
    transaction.relationFrom = relationFrom
    transaction.relationTo = relationTo
    
    if "notes" in transactionDict:
        for n in transactionDict["notes"]:
            if not type(n) == str:
                return (False, 422, "Note has incorrect datatype")
            newnote = Note(n)
            transaction.notes.append(newnote)
            objAddQueue.append(newnote)
    
    for v in transactionDict["viewRights"]:
        if not type(v) == int:
            return (False, 422, "Right has incorrect datatype")
        right = Right.query.get(v)
        if (right == 0):
            return (False, 422, "Right was invalid")
        transaction.viewRights.append(right)
        
    for s in transactionDict["stocks"]:
        # Error when number is < 0, should be split into two transactions
        if "price" in s:
            # Spawn stock
        else:
            # Get stock
        # Add stock to transaction    
                    
            
