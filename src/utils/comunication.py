from fastapi import HTTPException
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException
from requests.auth import HTTPDigestAuth
import xmlrpc.client
from .exceptions import DeviceRequestError, DeviceConnectionError, DeviceTimeoutError

class ISAPI:
    def __init__(self, url, key):
        self.url = url
        self.key = key

    def getapi(self): #GET operations for HikvisionAPI
        try:
            req = requests.get(self.url, auth=HTTPDigestAuth('admin', self.key), timeout=1)
            req.raise_for_status()

            if req.status_code == 200:
                return(req.text)
            else:
                return(req)

        #EXCEPCIONES
        except ConnectionError:
            raise DeviceConnectionError('Error: Connection Error')
        except Timeout:
            raise DeviceTimeoutError('Error: Timeout')
        except RequestException as e:
            raise DeviceRequestError(f'[!] Request Error: {e}')
        except KeyboardInterrupt:
            print('\n[-] Interrumpiendo Programa...')
            return None

    def putapi(self, c_data): #PUT operations for HikvisionAPI
        try:
            req = requests.put(self.url, data = c_data, headers = {'Content-Type': 'application/xml'}, auth=HTTPDigestAuth('admin', self.key), timeout=3)

            if req.status_code == 200:
                return(req.text)
            else:
                return(req)

            #EXCEPCIONES
        except Exception:
            raise HTTPException(status_code=404)

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
