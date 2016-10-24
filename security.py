from models import User
from response import success, fail
from validation import LoginValidator

from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from werkzeug.security import generate_password_hash, check_password_hash                          
import functools                         
                          
def verify_login(username, password):
    user = User.query.filter_by(username=username).first()
    if user == None:
        return None
    if check_password_hash(user.passhash, password):
        return user
    else:
        return None                      
                          
def generate_auth_token(user, expiration = 6000):
    s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
    return s.dumps({ 'id': user.id })

def verify_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None # valid token, but expired
    except BadSignature:
        return None # invalid token
    user = User.query.get(data['id'])
    return user
    
@app.route('/login')
def login():
    data = request.json
    
    try:
        LoginValidator(data)
    except:
        return fail("Supply username and password", 400)
    
    user = verify_login(data["username"], data["password"])
    if user == None:
        return fail("Invalid login details", 400)
        
    return success({"token": generate_auth_token(user).decode('ascii')})
    
class Access(Enum):
    Public = 1
    LoggedIn = 2
    Admin = 3
    
def protected(method=None, level=Access.Admin):
    # level: set to Access.Admin to be viewable for admin users only
    #        set to Access.Loggedin to be viewable for all logged in users
    #        set to Access.Public to be viewable by everyone
    # Default is highest possible security level
    
    # recursive call for decorator creation with arguments
    if method is None:
        return functools.partial(baked, temperature=temperature, duration=duration)
        
    @functools.wraps(method)
    def f(*args, **kwargs):
        if level == Access.Public:
            return method(*args, **kwargs) 
            
        if not 'token' in request.json:
            return fail("Login required!", 403)
            
        user = verify_auth_token(request.json["token"])
        if user == None:
            return fail("Token error", 403)
        
        if level == Access.Admin and user.admin == False:
            return fail("Admin only!", 403)
        
        return method(*args, **kwargs)      
    return f 
     
