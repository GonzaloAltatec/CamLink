import requests
from requests.auth import HTTPDigestAuth
import xmlrpc.client

class API:
    def __init__(self, url, key):
        self.url = url
        self.key = key

class ISAPI(API):
    def __init__(self, url, key):
        super().__init__(url, key)

    def getapi(self): #Operaciones GET para API Hikvision
        try:
            req = requests.get(self.url, auth=HTTPDigestAuth('admin', self.key))

            if req.status_code == 200:
                return(req.text)
            else:
                return(req)
        
        #EXCEPCIONES
        except ConnectionError:
            return('[-] Error de Conexión')
        except KeyboardInterrupt:
            return('\n[-] Interrumpiendo Programa...')
        except Exception as e:
            return(f'Error: [{e}]')

    def putapi(self, c_data): #Operaciones GET para API Hikvision
        try:
            req = requests.put(self.url, data = c_data, headers = {'Content-Type': 'application/xml'}, auth=HTTPDigestAuth('admin', self.key))

            if req.status_code == 200:
                return(req)
            else:
                return(req)
            
        #EXCEPCIOENS
        except Exception as e:
            return(f'Error: [{e}]')
        
class OdooAPI:
    def __init__(self, url, db, username, password):
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        #Data from the class
        self.uid = self.login()
        self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')
        self.search_table = None
        self.req_data = None

    def login(self):
        try:
            common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
            uid = common.authenticate(self.db, self.username, self.password, {})
            return(uid)
        except Exception as e:
            return(f'Login Error: {e}')

    def search(self, table, element, operator):
        try:
            request = self.models.execute_kw(self.db, self.uid, self.password, table, 'search', [[[element, '=', operator]]])
            self.search_table = table
            self.req_data = request
            return(request)
        except Exception as e:
            return(f'Error in Search Function: {e}')

    def read(self, request):
        try:
            read_req = self.models.execute_kw(self.db, self.uid, self.password, self.search_table, 'read', [request])
            return(read_req)
        except Exception as e:
            return(f'Error in Read Function: {e}')
