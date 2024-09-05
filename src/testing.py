from utils.comunication import OdooAPI
from dotenv import load_dotenv
import os
load_dotenv(override=True)


class OdooTest:
    def __init__(self, id):
        self.id = id
        self.url = os.getenv('URL')
        self.db = os.getenv('DB')
        self.user = os.getenv('USERNAME')
        self.key = os.getenv('PASSWORD')
        self.erp = OdooAPI(self.url, self.db, self.user, self.key)         

    def sys_read(self):
        req = self.erp.search('altatec.elemento', 'sistema_id', self.id)
        read_req = self.erp.read(req)
        return(read_req)

test = OdooTest(4585)
print(test.sys_read())
