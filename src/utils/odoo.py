from .comunication import OdooAPI
from dotenv import load_dotenv
import os

load_dotenv(override=True)


class Odoo:
    def __init__(self):
        self.url = os.getenv("URL")
        self.db = os.getenv("DB")
        self.user = os.getenv("USERNAME")
        self.key = os.getenv("PASSWORD")
        self.erp = OdooAPI(self.url, self.db, self.user, self.key)

    def sys_req(self, sys_id: int):  # List of system content
        req = self.erp.search("altatec.elemento", "sistema_id", sys_id)
        read_req = self.erp.read(req)
        return read_req

    def element_sys(self, sys_id: int):  # Return element asociated System ID
        req = self.erp.search("altatec.elemento", "id", sys_id)
        req_read = self.erp.read(req)
        if req_read is not None and isinstance(req_read, list):
            return str(
                req_read[0]["sistema_id"][0]
            )  # Change [0]['sistema_id'][0] to -> [0]['sistema_id'][1] in order to get systen name istead of ID

    def element_ids(
        self, sys_id: int
    ):  # Recive element ID and read the 'propiedad_ids' field
        req = self.erp.search("altatec.elemento", "id", sys_id)
        req_read = self.erp.read(req)

        fields = []
        if req_read is not None and isinstance(req_read, list):
            for field in req_read:
                fields.append(field["propiedad_ids"])

        return fields

    def element_data(self, id):  # Revice 'propiedad_ids' ID and read content
        req = self.erp.search("altatec.elemento.propiedad", "id", id)
        req_read = self.erp.read(req)

        return req_read

    def model_conf(self, model: str):  # Get model json configuration
        req = self.erp.search("altatec.revisor.template", "name", model)
        read_req = self.erp.read(req)
        if read_req is not None and isinstance(read_req, list):
            return read_req[0]["code"]
