"""
comunication.py - Módulo para la comunicación con dispositivos Hikvision

Este módulo proporciona clases para la comunicación con dispositivos Hikvision
usando la API ISAPI. Incluye manejo de errores y autenticación.

Clases principales:
- ISAPI: Maneja las operaciones GET y PUT con la API ISAPI
"""

from fastapi import HTTPException
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException
from requests.auth import HTTPDigestAuth
import xmlrpc.client
from .exceptions import DeviceRequestError, DeviceConnectionError, DeviceTimeoutError


class ISAPI:
    """
    Cliente para la comunicación con la API ISAPI de Hikvision

    Args:
        url (str): URL del dispositivo Hikvision
        key (str): Contraseña de acceso

    Attributes:
        url (str): URL del dispositivo
        key (str): Contraseña de acceso
    """

    def __init__(self, url: str, key: str):
        """
        Inicializa una nueva instancia del cliente ISAPI

        Args:
            url (str): URL del dispositivo Hikvision
            key (str): Contraseña de acceso
        """
        self.url = url
        self.key = key

    def getapi(self) -> str:
        """
        Realiza una operación GET en la API ISAPI

        Returns:
            str: Respuesta en formato XML si exitosa
            requests.Response: Objeto Response si hay error

        Raises:
            DeviceConnectionError: Si hay error de conexión
            DeviceTimeoutError: Si hay timeout en la conexión
            DeviceRequestError: Si hay error en la solicitud
        """
        try:
            req = requests.get(
                self.url,
                auth=HTTPDigestAuth("admin", self.key),
                timeout=5
            )
            req.raise_for_status()

            if req.status_code == 200:
                return req.text
            else:
                return req

        # EXCEPCIONES
        except ConnectionError:
            raise DeviceConnectionError("Error: Connection Error")
        except Timeout:
            raise DeviceTimeoutError("Error: Timeout")
        except RequestException as e:
            raise DeviceRequestError(f"[!] Request Error: {e}")
        except KeyboardInterrupt:
            print("\n[-] Interrumpiendo Programa...")
            return None

    def putapi(self, c_data: str) -> str:
        """
        Realiza una operación PUT en la API ISAPI

        Args:
            c_data (str): Datos XML a enviar

        Returns:
            str: Respuesta en formato XML si exitosa
            requests.Response: Objeto Response si hay error

        Raises:
            DeviceConnectionError: Si hay error de conexión
            DeviceTimeoutError: Si hay timeout en la conexión
            DeviceRequestError: Si hay error en la solicitud
        """
        try:
            req = requests.put(
                self.url,
                data=c_data,
                headers={"Content-Type": "application/xml"},
                auth=HTTPDigestAuth("admin", self.key),
                timeout=6,
            )

            if req.status_code == 200:
                return req.text
            else:
                return req

            # EXCEPCIONES
        except Exception:
            raise HTTPException(status_code=404)


class OdooAPI:
    def __init__(self, url, db, username, password):
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        # Data from the class
        self.uid = self.login()
        self.models = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/object")
        self.search_table = None
        self.req_data = None

    def login(self):
        try:
            common = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/common")
            uid = common.authenticate(self.db, self.username, self.password, {})
            return uid
        except Exception as e:
            return f"Login Error: {e}"

    def search(self, table, element, operator):
        try:
            request = self.models.execute_kw(
                self.db,
                self.uid,
                self.password,
                table,
                "search",
                [[[element, "=", operator]]],
            )
            self.search_table = table
            self.req_data = request
            return request
        except Exception as e:
            return f"Error in Search Function: {e}"

    def read(self, request):
        try:
            read_req = self.models.execute_kw(
                self.db, self.uid, self.password, self.search_table, "read", [request]
            )
            return read_req
        except Exception as e:
            return f"Error in Read Function: {e}"
