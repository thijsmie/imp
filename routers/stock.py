from models import db, Stock
from flask import request, Blueprint
from flask.json import jsonify

def stckToJson(stck):
    return {"id": stck.id, "number": stck.number, "price": stck.price, "priceFractionNumerator": stck.priceFractionNumerator,
            "priceFractionDenominator": stck.priceFractionDenominator, "product/": "/product/"+str(stck.productID), "owner/": "/relation/"+str(stck.ownerID),
            "transactions~":"/transactions"}

StockRouter = Blueprint('StockRouter', __name__)
#@auth.token_required
@StockRouter.route('/')
def stocks():
    resp = []
    for stck in Stock.query.all():
        resp.append(stckToJson(stck)) 
    return jsonify(resp)
    

#@auth.token_required
@StockRouter.route('/<int:stock_id>', methods=["GET"])
def stock_get(stock_id):
    stock = Stock.query.get(stock_id)
    if (stock == None):
        return jsonify({"error":404,"id":stock_id})
    return jsonify(stckToJson(stock))

    
#@auth.token_required
@StockRouter.route('/', methods=["POST"])
def stock_add():
    product = Product()
    if not ("name" in request.json and
            "isPhysical" in request.json and
            "correctionRelationID" in request.json):
        resp = jsonify({"error":422, "request": request.json})
        resp.status_code = 422
        return resp
    product.name = request.json["name"]
    product.isPhysical = request.json["isPhysical"]
    product.correctionRelationID = request.json["correctionRelationID"]
    db.session.add(product)
    db.session.commit()
    return jsonify(prdToJson(product))


