from .comunication import OdooAPI
from dotenv import load_dotenv
import os
load_dotenv(override=True)

class Odoo:
    def __init__(self, id):
        self.id = id
        self.url = os.getenv('URL')
        self.db = os.getenv('DB')
        self.user = os.getenv('USERNAME')
        self.key = os.getenv('PASSWORD')
        self.erp = OdooAPI(self.url, self.db, self.user, self.key)         

    def element_ids(self): #Recive element ID and read the 'propiedad_ids' field
        req = self.erp.search('altatec.elemento', 'id', self.id)
        req_read = self.erp.read(req)

        fields = []
        for field in req_read:
            fields.append(field['propiedad_ids'])

        return(fields)

    def element_data(self, id): #Revice 'propiedad_ids' ID and read content
        req = self.erp.search('altatec.elemento.propiedad', 'id', id)
        req_read = self.erp.read(req)

        return(req_read)
