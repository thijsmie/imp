from functions import rTypes, rReference
import datetime

# Generic database object retriever:
def getDbObject(reference):
    objmatchtype = rTypes[reference["matchtype"]]
    obj = objmatchtype.query.get(reference["id"])
    if (obj == 0):
        return False, None
    return True, obj
    
# Function for parsing date strings of form yyyy-mm-dd
def parseDate(date):
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
def decode(request, model):
    for key, matchtype in model.items():
        if not key in request:
            return False, key
        if matchtype(matchtype) == matchtype:
            if not matchtype(request[key]) == matchtype:
                return False, key
        if matchtype(matchtype) == list:
            if not matchtype(request[key]) == list:
                return False, key
            for i in range(len(request[key])):
                item = request[key][i]
                if not matchtype(item) == dict or not decode(item, rReference)[0] or not item["matchtype"] == matchtype[0]:
                    return False, key + ':' + str(i)
                succes, refobj = getDbObject(item)
                if not succes:
                    return False, key + ':' + str(i)
                request[key][i] = refobj
        if matchtype(matchtype) == str:
            if matchtype == "Date":
                # This is an exception case for dates
                if not matchtype(request[key]) == str:
                    return False, key
                Success, Date = parseDate(request[key])
                if not succes:
                    return False, key
                request[key] = Date
                continue
            if not matchtype(request[key]) == dict or not decode(request[key], rReference)[0] or not request[key]["matchtype"] == matchtype:
                return False, key
            succes, refobj = getDbObject(request[key])
            if not succes:
                return False, key + ':' + str(i)
            request[key] = refobj
    return True, request
