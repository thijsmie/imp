import requests
import xmltodict


class ConscriboRelation(dict):
    pass
    
class ConscriboTransaction(dict):
    pass
    
class ConscriboTransactionRow(dict):
    pass

class ConscriboAccount(dict):
    pass

class ConscriboException(Exception):
    pass
    

class Conscribo:
    LIVE_URL = 'https://secure.conscribo.nl/'
    TEST_URL = 'https://secure.conscribo.nl/'
    API_VERSION = '0.20110602'
    
    def __init__(self, domain, identifier, passphrase, debug=False):
        self.domain = domain
        self.identifier = identifier
        self.passphrase = passphrase
        
        if (debug):
            self.url = self.TEST_URL + domain + '/request.xml'
        else:
            self.url = self.LIVE_URL + domain + '/request.xml'
        
        self.authenticate()
    
    def do_request(self, command, **kwargs):
        xmldata = xmltodict.unparse({'request': kwargs})
        
        response = self.session.post(self.url, data=xmldata)
        
        if (response.status_code != 200):
            raise ConscriboException("API endpoint returned statuscode " + str(response.status_code) + " on submitting " + str(kwargs))
        
        try:
            data = xmltodict.parse(response.text)
            data = data['result']                
        except:
            raise ConscriboException("API endpoint returned invalid xml: \"" + response.text + "\"")
        
        return data 
        
    def authenticate(self):
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/xml', 'X-Conscribo-API-Version': self.API_VERSION})
        self.session.encoding = 'utf-8'
        data = self.do_request('authenticate', apiIdentifierKey=self.identifier, passphrase=self.passphrase)
        # test success here or throw auth error
        
    def relationfields(self):
        pass # command: listFieldDefinitions

	def relations(limit=0, offset=0):
	    pass

	def updaterelation(relation):
	    pass
	    
	def createrelation(relation):
	    pass
	    
	def deleterelation(relation):
	    pass

    def transactions(filters=None, limit=0, offset=0):
        pass
        
    def updatetransaction(transaction):
        pass
        
    def createtransaction(transaction):
        pass
        
    def deletetransaction(transaction):
        pass
        
    def accounts(date=None):
        pass
        
    def updateaccount(account):
        pass
        
    def createaccount(account):
        pass
        
    def deleteaccount(account):
        pass
        
        
conscribo = Conscribo("olympusvoorraadapitest", "blabla", "blabla")
        
        
        
