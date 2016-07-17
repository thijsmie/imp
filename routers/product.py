from models import db, Product
from flask import request, Blueprint
from flask.json import jsonify

def prdToJson(prd):
    return {"id": prd.id, "name": prd.name, "correctionRelation~": "/correctionRelation",
            "stocks~": "/stocks", "buyDefaultMargins~": "/buyDefaultMargins", "sellDefaultMargins~": "/sellDefaultMargins"}   

ProductRouter = Blueprint('ProductRouter', __name__)
#@auth.token_required
@ProductRouter.route('/')
def products():
    resp = []
    for prd in Product.query.all():
        resp.append(prdToJson(prd)) 
    return jsonify(resp)
    

#@auth.token_required
@ProductRouter.route('/<int:product_id>', methods=["GET"])
def product_get(product_id):
    product = Product.query.get(product_id)
    if (product == None):
        return jsonify({"error":404,"id":product_id})
    return jsonify(prdToJson(product))

    
#@auth.token_required
@ProductRouter.route('/', methods=["POST"])
def product_add():
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


