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
        self.elements = self.sys_req()
        self.router = self.router_req()
         
    def sys_req(self): #Get a list with all the System elements
        try:
            req = self.erp.search('altatec.elemento', 'sistema_id', self.id)
            req_read = self.erp.read(req)
            return(req_read)
        except Exception as e:
            return(str(e))

    def cam_qty(self): #Return all element with the property 'product_id' = 'CVCCV'

        cam = []
        for ids in self.elements:
            cam.append(ids['product_id'])

        while False in cam:
            cam.remove(False)

        for q in cam:
            if q[0] == 3552 or q[0] == 8257 or q[0] == 8256:
                return(cam.count(q))

    def router_req(self): #Return the system router
        try:
            req = self.erp.search('altatec.router', 'sistema_id', self.id)
            req_read = self.erp.read(req)
            return(req_read)
        except Exception as e:
            return(str(e))

    def network(self): #Search and return the IP of the system router
        for router in self.router:
            router_ip = router['ip_cctv']
        ip = router_ip.split('.')
        net = str(ip[0] + '.' + ip[1] + '.' + ip[2] + '.') 
        return(net)

    def camera_ip(self): #Set host IP deppending on the camera cuantity
        qty = self.cam_qty()
        cam_ip_final = qty + 16 -1

        cam_list = [16]
        cam_ip_inicio = 16

        if cam_ip_final == 16:
            return(cam_list)
        elif cam_ip_final > 16 and cam_ip_final < 120:
            while cam_ip_inicio < cam_ip_final: 
                cam_ip_inicio += 1
                cam_list.append(cam_ip_inicio)
            return(cam_list)
        elif cam_ip_final == 120:
            while cam_ip_inicio < cam_ip_final: 
                cam_ip_inicio += 1
                cam_list.append(cam_ip_inicio)
            return(cam_list)
        else:
            return("Cantidad no soportada")

    def getpass(self): #Get system Password
        for key in self.router:
            password = key['router_password']
        return(password)

    def getsysname(self): #Get system name
        for name in self.router:
            n_filter = name['sistema_id']
            return(n_filter[1])

    def camera_name(self): #Search all camera names
        
        elements_name = []

        for elems in self.elements:
            if elems['product_id'] == False:
                continue
            if elems['product_id'][0] == 3552 or elems['product_id'][0] == 8257 or elems['product_id'][0] == 8256:
                elements_name.append(elems['name'])

        return(elements_name)

    def running_orders(self):
        try:
            #req = self.erp.search('mrp.workorder', 'z_project_id', 378)
            #req = self.erp.search('mrp.workorder', 'z_project_sistema_id', True)
            req = self.erp.search('mrp.workorder', 'z_user_working', True)
            red = self.erp.read(req)
            return(red)
        except Exception as e:
            return(e)
    #def camera_port(self): #Search for camera HTTP Port