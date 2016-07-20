from flask import Response
from functions import rReverseTypes

def encode_recursive(obj):
    if type(obj) == list:
        for i in range(len(obj)):
            obj[i] = encode_recursive(obj[i])
        return obj
    elif type(obj) == dict:
        fields = {}
        for k, v in obj.items():
            fields[k] = encode_recursive(v)
        return fields
    elif type(obj) in rReverseTypes:
        return {'type':rReverseTypes[type(obj)], 'id': obj.id}
    else:
        return obj
        
def encode(obj):
    fields = {}
    for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
        fields[field] = encode_recursive(obj.__getattribute__(field))
    return fields
