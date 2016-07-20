from models import Transaction, Stock, Product, Relation, Margin, Right, Note
import datetime

# String type matching:
rTypes = {
    "Transaction": Transaction,
    "Stock": Stock,
    "Product": Product,
    "Relation": Relation,
    "Margin": Margin,
    "Right": Right,
    "Note": Note
}

# Required dict structure on creation:
rTransaction = {
    "eventname": str, 
    "eventdate": "Date",
    "contact": str,
    "relationTo": "Relation", 
    "relationFrom": "Relation",
    "stocks": list("Stock")
}
rTransactionNotes = {
    "notes": list("Note")
}
rTransactionViewRights = {
    "viewRights": list("Right")
}

rStock = {
    "product": "Product",
    "number": int,
    "owner": "Relation",
    "price": int
}

rProduct = {
    "name": str,
    "isPhysical": bool,
    "buyDefaultMargins": list("Margin"),
    "sellDefaultMargins": list("Margin"),
    "correctionRelation": "Relation"
}

rRelation = {
    "name": str,
    "email": str
}

rMargin = {
    "name": str,
    "isPercentage": bool,
    "amountNumerator": int,
    "amountDenominator": int
}

rRight = {
    "name": str
}

rNote = {
    "text": str
}


# Required dict structure on reference:
rReference = {
    "type": str,
    "id": int
}

# Generic database object retriever:
def GetDbObject(reference):
    objtype = rTypes[reference["type"]]
    obj = objtype.query.get(reference["id"])
    if (obj == 0):
        return False, None
    return True, obj
    
# Function for parsing date strings of form yyyy-mm-dd
def DateValidator(date):
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
    

# Generic dict validator function:
def DictValidator(Dict, rDict):
    for Key, Type in rDict.items():
        if not Key in Dict:
            return False, Key
        if type(Type) == type:
            if not type(Dict[Key]) == Type:
                return False, Key
        if type(Type) == list:
            if not type(Dict[Key]) == list:
                return False, Key
            for Index in range(len(Dict[Key])):
                Item = Dict[Key][Index]
                if not type(Item) == dict or 
                   not DictValidator(Item, rReference)[0] or
                   not Item["type"] == Type[0]:
                    return False, Key + ':' + str(Index)
                Succes, ReferencedObject = GetDbObject(Item)
                if not Succes:
                    return False, Key + ':' + str(Index)
                Dict[Key][Index] = ReferencedObject
        if type(Type) == str:
            if Type == "Date":
                # This is an exception case for dates
                if not type(Dict[Key]) == str:
                    return False, Key
                Success, Date = DateValidator(Dict[Key])
                if not Succes:
                    return False, Key
                Dict[Key] = Date
                continue
            if not type(Dict[Key]) == dict or
               not DictValidator(Dict[Key], rReference)[0] or
               not Dict[Key]["type"] == Type:
                return False, Key
            Succes, ReferencedObject = getDbObject(Dict[Key])
            if not Succes:
                return False, Key + ':' + str(Index)
            Dict[Key] = ReferencedObject
    return True, Dict
