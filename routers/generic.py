from models import db
from flask import request, Blueprint
from flask.json import jsonify
from functions import rTypes, encode, decode

def makeGenericObjectRouter(objname):
    GenericRouter = Blueprint(objname, objname)
    
    #@auth.token_required
    @GenericRouter.route('/')
    def objects():
        resp = []
        for obj in rTypes[objtype].query.all():
            resp.append(encode(obj)) 
        return jsonify(resp)
    
    #@auth.token_required
    @GenericRouter.route('/<int:obj_id>', methods=["GET"])
    def object_get(obj_id):
        obj = rTypes[objtype].query.get(obj_id)
        if (obj == None):
            return jsonify({"error":404,"type":,"id":obj_id})
        return jsonify(enocde(obj))

        
    #@auth.token_required
    @GenericRouter.route('/', methods=["POST"])
    def object_add():
        obj_new = rType[objtype]()
        succes, result = decode(request.json, rTypeDict[objtype])
        
        if not succes:
            resp = jsonify({"error":422, "request": request.json, "result": result})
            resp.status_code = 422
            return resp
            
        for k, v in result.items():
            setattr(obj_new, k, v)

        db.session.add(obj_new)
        db.session.commit()
        return jsonify(encode(obj_new))


