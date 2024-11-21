from fastapi import HTTPException
from ..operations import Hikvision as Hik
from ..odoo import Odoo

#Model type created on execution
def device(id:int):
    #Send element ID to Odoo Class
    erp = Odoo(id)
    #Get element properties
    properties_ids = erp.element_ids()

    #Read all property ID's
    for ids in properties_ids:

        data = erp.element_data(ids)
        if data is not None and isinstance(data, list):
            #Read System from element
            sys_name = erp.element_sys()

            #Creating a list for key-value pairs
            key_lst = []
            val_lst = []

            #Reading data and appending 'name' and 'value' field to lists
            for x in data:
                key_lst.append(x['name'])
                val_lst.append(x['valor'])

            #Creating a dictionary using 'zip' with our 2 lists
            device_data = dict(zip(key_lst, val_lst))

            #Conditional to ensure device it's compatible with CamLink operations
            if device_data['product_id'] == 'CVCCV' or 'CVKP1' or 'CVKP2':
                #Requesting device model
                conf = Hik(device_data['DIRECCION IP'], device_data['PASSWORD'])
                device_model = conf.getmodel()
                if device_model is None:
                    raise HTTPException(status_code=404, detail='Device model not found')
                #Give Odoo data to Device Model
                new_device = {'id': id, 
                            'name': device_data['NOMBRE'], 
                            'installation': sys_name, 
                            'user': device_data['USUARIO'], 
                            'password': device_data['PASSWORD'], 
                            'ip': device_data['DIRECCION IP'], 
                            'port': int(device_data['PUERTO HTTP']), 
                            'model': device_model}
                return(new_device)
            else:
                raise HTTPException(status_code=404, detail=f'Error on device: {id} - Device type not accepted {device_data['product_id']}')
