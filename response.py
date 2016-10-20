from flask.json import jsonify

def success(data=None):
    if data == None:
        data = {}
    response = jsonify(**data)
    response.status = 200
    return response
    
def fail(message, status=400):
    response = jsonify(error=message)
    response.status = status
    return response
