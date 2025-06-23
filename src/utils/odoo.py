"""
odoo.py - Cliente para la integración con Odoo ERP

Este módulo proporciona una interfaz para interactuar con el ERP Odoo,
permitiendo la obtención de datos de sistemas y configuraciones.

Funcionalidades principales:
- Obtención de datos de sistemas
- Búsqueda de elementos asociados
- Lectura de propiedades de elementos
- Obtención de configuraciones por modelo
"""

from .comunication import OdooAPI
from dotenv import load_dotenv
import json
import os

# Cargar variables de entorno
load_dotenv(override=True)


class Odoo:
    """
    Cliente para la integración con Odoo ERP

    Args:
        None (usa variables de entorno para la configuración)

    Attributes:
        url (str): URL del servidor Odoo
        db (str): Nombre de la base de datos
        user (str): Usuario de Odoo
        key (str): Contraseña de Odoo
        erp (OdooAPI): Cliente API de Odoo
    """

    def __init__(self):
        """
        Inicializa una nueva instancia del cliente Odoo

        Carga las credenciales desde variables de entorno:
        - URL: URL del servidor Odoo
        - DB: Nombre de la base de datos
        - USERNAME: Usuario de Odoo
        - PASSWORD: Contraseña de Odoo
        """
        self.url = os.getenv("URL")
        self.db = os.getenv("DB")
        self.user = os.getenv("USERNAME")
        self.key = os.getenv("PASSWORD")
        self.erp = OdooAPI(self.url, self.db, self.user, self.key)

    def sys_req(self, sys_id: int) -> list:
        """
        Obtiene el contenido de un sistema específico

        Args:
            sys_id (int): ID del sistema a consultar

        Returns:
            list: Lista de elementos del sistema
        """
        req = self.erp.search("altatec.elemento", "sistema_id", sys_id)
        return self.erp.read(req)

    def element_sys(self, sys_id: int) -> str:
        """
        Obtiene el ID del sistema asociado a un elemento

        Args:
            sys_id (int): ID del elemento

        Returns:
            str: ID del sistema asociado

        Note:
            Para obtener el nombre del sistema en lugar del ID,
            cambiar [0]['sistema_id'][0] por [0]['sistema_id'][1]
        """
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

    def element_data(self, id: int) -> dict:
        """
        Obtiene los datos de una propiedad específica

        Args:
            id (int): ID de la propiedad

        Returns:
            dict: Datos de la propiedad
        """
        req = self.erp.search("altatec.elemento.propiedad", "id", id)
        return self.erp.read(req)

    def model_conf(self, model: str) -> list:
        """
        Obtiene la configuración JSON de un modelo específico

        Args:
            model (str): Nombre del modelo

        Returns:
            list: Lista de configuraciones del modelo
        """
        return self.erp.search("altatec.revisor.template", "name", model)

    def sys_nvr(self, sys_id: int):
        req = self.erp.search("altatec.grabador", "sistema_id", sys_id)
        req_read = self.erp.read(req)
        hosts = []

        if req_read is not None and isinstance(req_read, list):
            for x in req_read:
                data = {"host": "", "user": "", "password": ""}
                for k, v in x.items():
                    if k == "host":
                        data["host"] = v
                    elif k == "usuario":
                        data["user"] = v
                    elif k == "password":
                        data["password"] = v

                hosts.append(data)
        return hosts
