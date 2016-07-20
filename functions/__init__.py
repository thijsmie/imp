from . import encode as e, decode as d
from models import Transaction, Stock, Product, Relation, Margin, Right, Note

encode = e.encode
decode = d.decode

__all__ = ['encode', 'decode', 'rTypes', 'rReverseTypes', 'rTransaction', 'rTransactionNotes', 'rTransactionViewRights', 'rStock', 'rProduct', 'rRelation', 'rMargin', 'rNote', 'rReference']

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
rReverseTypes = {v: k for k,v in rTypes.items()}

# Required dict structure on creation:
rTransactionMain = {
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
rTransaction = [rTransactionMain, rTransactionNotes, rTransactionViewRights]

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

# Map from type to verification dict
# TODO: refactor dict specifications to model? Generate dict specification from model?
rTypeDict = {
    "Transaction": rTransaction,
    "Stock": rStock,
    "Product": rProduct,
    "Relation": rRelation,
    "Margin": rMargin,
    "Right": rRight,
    "Note": rNote
}
