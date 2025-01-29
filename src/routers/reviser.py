# FastAPI imports
from fastapi import APIRouter, status

# Custom Exceptions
from src.utils.exceptions import (
    DeviceConnectionError,
    DeviceRequestError,
    DeviceTimeoutError,
)

# Models and data formatting imports
from ..utils.db import models
from ..utils.db.schemas import IDList

# Hikvision API operator
from ..utils.operations import Hikvision as Hik

# Odoo requests library
from ..utils.odoo import Odoo

# Event logger
import logging
import inspect

logging.basicConfig(level=logging.ERROR)
router = APIRouter(tags=["reviser"], prefix="/revise")


# Check if DeviceName match with Odoo DeviceName
async def device_name(device: dict):
    api = Hik(device["ip"], device["password"])
    data = api.getname()
    if data != device["name"]:
        return {
            "status": "Error",
            "details": f"Odoo device name [{device['name']}] does not match with configured name [{data}]",
        }
    else:
        return "Okey"


# Check NTP configuration
async def device_ntp(device: dict):
    api = Hik(device["ip"], device["password"])
    data = api.getntp()
    conf = device["conf"]

    parameters = {"status": "", "server": "", "sync": ""}

    if data["server"] != conf["ntp"]["server"]:
        parameters["status"] = "Error"
        parameters["server"] = (
            f"NTP Server on device: [{data['server']}]. Correct server: [{conf['ntp']['server']}]"
        )
    else:
        parameters["server"] = "Okey"

    # Synchronization check
    if data["sync"] != conf["ntp"]["sync"]:
        parameters["status"] = "Error"
        parameters["sync"] = (
            f"Synchronization time with NTP server at device: [{data['sync']}]. Correct Synchronization: [{conf['ntp']['sync']}]"
        )
    else:
        parameters["sync"] = "Okey"

    # Check parameter errors and return device config status
    if parameters["status"] == "Error":
        return parameters
    else:
        return "Okey"


# Check DST configuration
async def device_dst(device: dict):
    api = Hik(device["ip"], device["password"])
    data = api.getdst()
    conf = device["conf"]

    parameters = {"status": "", "mode": "", "timezone": ""}

    # Server check
    if data["mode"] != conf["dst"]["mode"]:
        parameters["status"] = "Error"
        parameters["mode"] = (
            f"DST Mode on device: [{data['mode']}]. Correct Mode: [{conf['dst']['mode']}]"
        )
    else:
        parameters["mode"] = "Okey"

    # Synchronization check
    if data["timezone"] != conf["dst"]["timezone"]:
        parameters["status"] = "Error"
        parameters["timezone"] = (
            f"DST Timezone on device: [{data['timezone']}]. Correct Timezone: [{conf['dst']['timezone']}]"
        )
    else:
        parameters["timezone"] = "Okey"

    # Check parameter errors and return device config status
    if parameters["status"] == "Error":
        return parameters
    else:
        return "Okey"


# Check Security configuration
async def device_security(device: dict):
    api = Hik(device["ip"], device["password"])
    data = api.getsec()
    conf = device["conf"]

    parameters = {"status": "", "web": "", "rtsp": ""}
    # Web Authentication check
    if data["web_sec"] != conf["security"]["web"]:
        parameters["status"] = "Error"
        parameters["web"] = (
            f"WEB authentication on device: [{data['web_sec']}]. Correct WEB authentication: [{conf['security']['web']}]"
        )
    else:
        parameters["web"] = "Okey"

    # RSTP Authentication check
    if data["rtsp_sec"] != conf["security"]["rtsp"]:
        parameters["status"] = "Error"
        parameters["rtsp"] = (
            f"RTSP authentication on device: [{data['rtsp_sec']}]. Correct RTSP authentication: [{conf['security']['rtsp']}]"
        )
    else:
        parameters["rtsp"] = "Okey"

    # Check parameter errors and return device config status
    if parameters["status"] == "Error":
        return parameters
    else:
        return "Okey"


# Check DNS configuration
async def device_dns(device: dict):
    api = Hik(device["ip"], device["password"])
    data = api.getdns()
    conf = device["conf"]

    parameters = {"status": "", "primary": "", "secondary": ""}
    # Primary DNS check
    if data["primary"] != conf["dns"]["primary"]:
        parameters["status"] = "Error"
        parameters["primary"] = (
            f"Primary DNS on device: [{data['primary']}]. Correct DNS: [{conf['dns']['primary']}]"
        )
    else:
        parameters["primary"] = "Okey"

    # Secondary DNS check
    if data["secondary"] != conf["dns"]["secondary"]:
        parameters["status"] = "Error"
        parameters["secondary"] = (
            f"Secondary DNS on device: [{data['secondary']}]. Correct DNS: [{conf['dns']['secondary']}]"
        )
    else:
        parameters["secondary"] = "Okey"

    # Check parameter errors and return device config status
    if parameters["status"] == "Error":
        return parameters
    else:
        return "Okey"


# Check Mail configuration
async def device_mail(device: dict):
    api = Hik(device["ip"], device["password"])
    data = api.getmail()
    conf = device["conf"]

    parameters = {
        "status": "",
        "name": "",
        "sender": "",
        "server": "",
        "port": "",
        "receiver": "",
        "email": "",
    }
    # Check device sender name
    if data["name"] != f"{device['name']} {device['installation']}":
        parameters["status"] = "Error"
        parameters["name"] = (
            f"Sender name on device: [{data['name']}]. Correct sender name: [{device['name']} {device['installation']}]"
        )
    else:
        parameters["name"] = "Okey"

    # Sender email
    if data["sender"] != conf["mail"]["sender"]:
        parameters["status"] = "Error"
        parameters["sender"] = (
            f"Sender Email on device: [{data['sender']}]. Correct Sender: [{conf['mail']['sender']}]"
        )
    else:
        parameters["sender"] = "Okey"

    # SMTP Server
    if data["server"] != conf["mail"]["server"]:
        parameters["status"] = "Error"
        parameters["server"] = (
            f"SMTP Server on device: [{data['server']}]. Correct SMTP Server: [{conf['mail']['server']}]"
        )
    else:
        parameters["server"] = "Okey"

    # SMTP Port
    if data["port"] != conf["mail"]["port"]:
        parameters["status"] = "Error"
        parameters["port"] = (
            f"SMTP Port on device: [{data['port']}]. Correct SMTP Port: [{conf['mail']['port']}]"
        )
    else:
        parameters["port"] = "Okey"

    # Receiver Name
    if data["receiver"] != conf["mail"]["receiver"]:
        parameters["status"] = "Error"
        parameters["receiver"] = (
            f"Receiver name on device: [{data['receiver']}]. Correct receiver name: [{conf['mail']['receiver']}]"
        )
    else:
        parameters["receiver"] = "Okey"

    # Receiver email
    if data["email"] != conf["mail"]["email"]:
        parameters["status"] = "Error"
        parameters["email"] = (
            f"Receiver email on device: [{data['email']}]. Correct receiver email: [{conf['mail']['email']}]"
        )
    else:
        parameters["email"] = "Okey"

    # Check parameter errors and return device config status
    if parameters["status"] == "Error":
        return parameters
    else:
        return "Okey"


# Check Main Stream configuration
async def device_mstream(device: dict):
    api = Hik(device["ip"], device["password"])
    data = api.getmstream()
    conf = device["conf"]

    parameters = {
        "status": "",
        "name": "",
        "encoding": "",
        "plus": "",
        "width": "",
        "height": "",
        "bitrate": "",
        "average": "",
        "fps": "",
    }
    # Channel Name
    if data["name"] != device["name"]:
        parameters["status"] = "Error"
        parameters["name"] = (
            f"Channel name on device: [{data['name']}]. Correct channel name: [{device['name']}]"
        )
    else:
        parameters["name"] = "Okey"

    # H.265 Encoding
    if data["encoding"] != conf["mstream"]["encoding"]:
        parameters["status"] = "Error"
        parameters["encoding"] = (
            f"Encoding type on device: [{data['encoding']}]. Correct encoding: [{conf['mstream']['encoding']}]"
        )
    else:
        parameters["encoding"] = "Okey"

    # H.265 Plus
    if data["plus"] != conf["mstream"]["plus"]:
        parameters["status"] = "Error"
        parameters["plus"] = (
            f"Encoding Plus mode on device: [{data['plus']}]. Correct Plus mode: [{conf['mstream']['plus']}]"
        )
    else:
        parameters["plus"] = "Okey"

    # Video Width
    if data["width"] != conf["mstream"]["width"]:
        parameters["status"] = "Error"
        parameters["width"] = (
            f"Video Width on device: [{data['width']}]. Correct Width: [{conf['mstream']['width']}]"
        )
    else:
        parameters["width"] = "Okey"

    # Video Height
    if data["height"] != conf["mstream"]["height"]:
        parameters["status"] = "Error"
        parameters["height"] = (
            f"Video Height on device: [{data['height']}]. Correct Width: [{conf['mstream']['height']}]"
        )
    else:
        parameters["height"] = "Okey"

    # Max. Bitrate
    if data["bitrate"] != conf["mstream"]["bitrate"]:
        parameters["status"] = "Error"
        parameters["bitrate"] = (
            f"Bitrate on device: [{data['bitrate']}]. Correct Bitrate: [{conf['mstream']['bitrate']}]"
        )
    else:
        parameters["bitrate"] = "Okey"

    # Min. Bitrate
    if data["average"] != conf["mstream"]["average"]:
        parameters["status"] = "Error"
        parameters["average"] = (
            f"Average Bitrate on device: [{data['average']}]. Correct average Bitrate: [{conf['mstream']['average']}]"
        )
    else:
        parameters["average"] = "Okey"

    # FPS
    if data["fps"] != conf["mstream"]["fps"]:
        parameters["status"] = "Error"
        parameters["fps"] = (
            f"FPS on device: [{data['fps']}]. Correct FPS: [{conf['mstream']['fps']}]"
        )
    else:
        parameters["fps"] = "Okey"

    # Check parameter errors and return device config status
    if parameters["status"] == "Error":
        return parameters
    else:
        return "Okey"


# Check Sub Stream configuration
async def device_sstream(device: dict):
    api = Hik(device["ip"], device["password"])
    data = api.getsstream()
    conf = device["conf"]

    parameters = {
        "status": "",
        "name": "",
        "encoding": "",
        "width": "",
        "height": "",
        "bitrate": "",
        "fps": "",
    }
    # Channel Name
    if data["name"] != device["name"]:
        parameters["status"] = "Error"
        parameters["name"] = (
            f"Channel name on device: [{data['name']}]. Correct channel name: [{device['name']}]"
        )
    else:
        parameters["name"] = "Okey"

    # H.265 Encoding
    if data["encoding"] != conf["sstream"]["encoding"]:
        parameters["status"] = "Error"
        parameters["encoding"] = (
            f"Encoding type on device: [{data['encoding']}]. Correct encoding: [{conf['sstream']['encoding']}]"
        )
    else:
        parameters["encoding"] = "Okey"

    # Video Width
    if data["width"] != conf["sstream"]["width"]:
        parameters["status"] = "Error"
        parameters["width"] = (
            f"Video Width on device: [{data['width']}]. Correct Width: [{conf['sstream']['width']}]"
        )
    else:
        parameters["width"] = "Okey"

    # Video Height
    if data["height"] != conf["sstream"]["height"]:
        parameters["status"] = "Error"
        parameters["height"] = (
            f"Video Height on device: [{data['height']}]. Correct Width: [{conf['sstream']['height']}]"
        )
    else:
        parameters["height"] = "Okey"

    # Max. Bitrate
    if data["bitrate"] != conf["sstream"]["bitrate"]:
        parameters["status"] = "Error"
        parameters["bitrate"] = (
            f"Bitrate on device: [{data['bitrate']}]. Correct Bitrate: [{conf['sstream']['bitrate']}]"
        )
    else:
        parameters["bitrate"] = "Okey"

    # FPS
    if data["fps"] != conf["sstream"]["fps"]:
        parameters["status"] = "Error"
        parameters["fps"] = (
            f"FPS on device: [{data['fps']}]. Correct FPS: [{conf['sstream']['fps']}]"
        )
    else:
        parameters["fps"] = "Okey"

    # Check parameter errors and return device config status
    if parameters["status"] == "Error":
        return parameters
    else:
        return "Okey"


# Check if OSD Show name match with Odoo name field
async def device_osd(device: dict):
    api = Hik(device["ip"], device["password"])
    data = api.getosd()
    if data != device["name"]:
        return {
            "status": "Error",
            "details": f"Odoo device name [{device['name']}] does not match with configured name [{data}]",
        }
    else:
        return "Okey"


# Overlay data showing format check
async def device_overlay(device: dict):
    api = Hik(device["ip"], device["password"])
    data = api.getoverlay()
    conf = device["conf"]

    parameters = {"status": "", "week": "", "format": ""}

    # No Week Display
    if data["week"] != conf["overlays"]["week"]:
        parameters["status"] = "Error"
        parameters["week"] = (
            f"Week OSD display on device: [{data['week']}]. Correct Week display configuration: [{conf['overlays']['week']}]"
        )
    else:
        parameters["week"] = "Okey"

    # Date Format
    if data["format"] != conf["overlays"]["format"]:
        parameters["status"] = "Error"
        parameters["format"] = (
            f"Date format on device: [{data['format']}]. Correct Week display configuration: [{conf['overlays']['format']}]"
        )
    else:
        parameters["format"] = "Okey"

    # Check configuration Status
    if parameters["status"] == "Error":
        return parameters
    else:
        return "Okey"


# Motion event configurations
async def device_motion(device: dict):
    api = Hik(device["ip"], device["password"])
    data = api.getmotion()
    conf = device["conf"]

    parameters = {
        "status": "",
        "enabled": "",
        "grid": "",
        "sensitivity": "",
        "target": "",
    }

    # Enabled
    if data["enabled"] != conf["motion"]["enabled"]:
        parameters["status"] = "Error"
        parameters["enabled"] = (
            f"Motion detection enabled on device: [{data['enabled']}]. Correct mode: [{conf['motion']['enabled']}]"
        )
    else:
        parameters["enabled"] = "Okey"

    # Grid Map
    if data["grid"] != conf["motion"]["grid"]:
        parameters["status"] = "Error"
        parameters["grid"] = (
            f"Grid configuration on device: [{data['grid']}]. Correct motion grid: [{conf['motion']['grid']}]"
        )
    else:
        parameters["grid"] = "Okey"

    # Sensitivity Level
    if data["sensitivity"] != conf["motion"]["sensitivity"]:
        parameters["status"] = "Error"
        parameters["sensitivity"] = (
            f"Sensitivity level on device: [{data['sensitivity']}]. Correct sensitivity level: [{conf['motion']['sensitivity']}]"
        )
    else:
        parameters["sensitivity"] = "Okey"

    # Target Type
    if data["target"] != conf["motion"]["target"]:
        parameters["status"] = "Error"
        parameters["target"] = (
            f"Target detection type on device: [{data['target']}]. Correct target types: [{conf['motion']['target']}]"
        )
    else:
        parameters["target"] = "Okey"

    if parameters["status"] == "Error":
        return parameters
    else:
        return "Okey"


# Recording enabled
async def device_record(device: dict):
    api = Hik(device["ip"], device["password"])
    data = api.getrecord()
    conf = device["conf"]

    parameters = {"status": "", "target": "", "method": ""}

    # Motion Detection > Linkage Method > Trigger Recording
    if data["target"] != conf["record"]["target"]:
        parameters["status"] = "Error"
        parameters["target"] = (
            f"Record target on device: [{data['target']}]. Correct record target: [{conf['record']['target']}]"
        )
    else:
        parameters["target"] = "Okey"

    # Record activated
    if data["method"] != conf["record"]["method"]:
        parameters["status"] = "Error"
        parameters["method"] = (
            f"Record activated on device: [{data['method']}]. Correct record mode: [{conf['record']['method']}]"
        )
    else:
        parameters["method"] = "Okey"

    if parameters["status"] == "Error":
        return parameters
    else:
        return "Okey"


# SD Error Exception
async def device_sderror(device: dict):
    api = Hik(device["ip"], device["password"])
    data = api.getsderr()
    conf = device["conf"]

    parameters = {"status": "", "method": ""}

    # Email send when exception occurs
    if data != conf["exceptions"]["disk"]:
        parameters["status"] = "Error"
        parameters["method"] = (
            f"SD Error exceotion on device: [{data}]. Correct exception mode: [{conf['exceptions']['disk']}]"
        )
    else:
        parameters["method"] = "Okey"

    if parameters["status"] == "Error":
        return parameters
    else:
        return "Okey"


# Illegal Access Exception
async def device_access(device: dict):
    api = Hik(device["ip"], device["password"])
    data = api.getillaccess()
    conf = device["conf"]

    parameters = {"status": "", "method": ""}

    # Email send when exception occurs
    if data != conf["exceptions"]["login"]:
        parameters["status"] = "Error"
        parameters["method"] = (
            f"Illegal access exception on device: [{data}]. Correct exception mode: [{conf['exceptions']['login']}]"
        )
    else:
        parameters["method"] = "Okey"

    if parameters["status"] == "Error":
        return parameters
    else:
        return "Okey"


# SD Quota
async def device_quota(device: dict):
    api = Hik(device["ip"], device["password"])
    data = api.getquota()
    conf = device["conf"]

    parameters = {"status": "", "picture": "", "video": ""}

    if data["picture"] != conf["quota"]["picture"]:
        parameters["status"] = "Error"
        parameters["picture"] = (
            f"Disk quota for images on device: [{data['picture']}]. Correct quota for images: [{conf['quota']['picture']}]"
        )
    else:
        parameters["picture"] = "Okey"

    if data["video"] != conf["quota"]["video"]:
        parameters["status"] = "Error"
        parameters["video"] = (
            f"Disk quota for video on device: [{data['video']}]. Correct quota for images: [{conf['quota']['video']}]"
        )
    else:
        parameters["video"] = "Okey"

    if parameters["status"] == "Error":
        return parameters
    else:
        return "Okey"


# SD Info
async def device_sd(device: dict):
    api = Hik(device["ip"], device["password"])
    data = api.getsd()
    conf = device["conf"]

    parameters = {"status": "", "state": ""}

    # if data['capacity'] != conf['sd']['capacity']:
    #    parameters['status'] = 'Error'
    #    parameters['capacity'] = 'Error'
    # else:
    #    parameters['capacity'] = 'Okey'

    if data["state"] != conf["sd"]["state"]:
        parameters["status"] = "Error"
        parameters["state"] = (
            f"SD Status on device: [{data['state']}]. Correct SD State: [{conf['sd']['state']}]"
        )
    else:
        parameters["state"] = "Okey"

    if parameters["status"] == "Error":
        return parameters
    else:
        return "Okey"


# Calendar
async def device_calendar(device: dict):
    api = Hik(device["ip"], device["password"])
    data = api.getcalendar()
    conf = device["conf"]

    parameters = {
        "status": "",
        "enabled": "",
        "advanced": {
            "overwrite": "",
            "prerecord": "",
            "postrecord": "",
            "expiration": "",
            "duration": "",
        },
        "schedule": {
            "Monday": {"start": "", "end": "", "mode": ""},
            "Tuesday": {"start": "", "end": "", "mode": ""},
            "Wednesday": {"start": "", "end": "", "mode": ""},
            "Thursday": {"start": "", "end": "", "mode": ""},
            "Friday": {"start": "", "end": "", "mode": ""},
            "Saturday": {"start": "", "end": "", "mode": ""},
            "Sunday": {"start": "", "end": "", "mode": ""},
        },
    }

    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    # Enabled
    for day in days:
        if data["enabled"] != conf["calendar"]["enabled"]:
            parameters["status"] = "Error"
            parameters["enabled"] = (
                f"Enabled recording calendar on device: [{data['enabled']}]. Correct calendar mode: [{conf['calendar']['enabled']}]"
            )
        else:
            parameters["enabled"] = "Okey"

    # Overwrite
    for day in days:
        if data["advanced"]["overwrite"] != conf["calendar"]["advanced"]["overwrite"]:
            parameters["status"] = "Error"
            parameters["advanced"]["overwrite"] = (
                f"Overwrite video option on device: [{data['advanced']['overwrite']}]. Correct overwrite mode: [{conf['calendar']['advanced']['overwrite']}]"
            )
        else:
            parameters["advanced"]["overwrite"] = "Okey"

    # Pre-Record
    for day in days:
        if data["advanced"]["prerecord"] != conf["calendar"]["advanced"]["prerecord"]:
            parameters["status"] = "Error"
            parameters["advanced"]["prerecord"] = (
                f"Pre-Record time on device: [{data['advanced']['prerecord']}]. Correct Pre-Record time: [{conf['calendar']['advanced']['prerecord']}]"
            )
        else:
            parameters["advanced"]["prerecord"] = "Okey"

    # Post-Record
    for day in days:
        if data["advanced"]["postrecord"] != conf["calendar"]["advanced"]["postrecord"]:
            parameters["status"] = "Error"
            parameters["advanced"]["postrecord"] = (
                f"Post-Record time on device: [{data['advanced']['postrecord']}]. Correct Post-Record time: [{conf['calendar']['advanced']['postrecord']}]"
            )
        else:
            parameters["advanced"]["postrecord"] = "Okey"

    model = str(device["model"])
    if model == "DS-2CD2183G2-IU":
        # Expiration Enabled
        for day in days:
            if (
                data["advanced"]["expiration"]
                != conf["calendar"]["advanced"]["expiration"]
            ):
                parameters["status"] = "Error"
                parameters["advanced"]["expiration"] = (
                    f"Expiration time on device: [{data['advanced']['expiration']}]. Correct expiration mode: [{conf['calendar']['advanced']['expiration']}]"
                )
            else:
                parameters["advanced"]["expiration"] = "Okey"

        # Expiration Duration
        for day in days:
            if data["advanced"]["duration"] != conf["calendar"]["advanced"]["duration"]:
                parameters["status"] = "Error"
                parameters["advanced"]["duration"] = (
                    f"Video duration on device: [{data['advanced']['duration']}]. Correct duration time: [{conf['calendar']['advanced']['duration']}]"
                )
            else:
                parameters["advanced"]["duration"] = "Okey"

    # Start Time
    for day in days:
        try:
            if (
                data["schedule"]["start"][day]
                != conf["calendar"]["schedule"][day]["start"]
            ):
                parameters["status"] = "Error"
                parameters["schedule"][day]["start"] = (
                    f"Start {day} time: [{data['schedule']['start'][day]}]. Correct {day} start time: [{conf['calendar']['schedule'][day]['start']}]"
                )
            else:
                parameters["schedule"][day]["start"] = "Okey"
        except KeyError:
            parameters["status"] = "Error"
            parameters["schedule"][day]["start"] = f"No start time on {day}"

    # End Time
    for day in days:
        try:
            if data["schedule"]["end"][day] != conf["calendar"]["schedule"][day]["end"]:
                parameters["status"] = "Error"
                parameters["schedule"][day]["end"] = (
                    f"End {day} time: [{data['schedule']['end'][day]}]. Correct {day} end time: [{conf['calendar']['schedule'][day]['end']}]"
                )
            else:
                parameters["schedule"][day]["end"] = "Okey"
        except KeyError:
            parameters["status"] = "Error"
            parameters["schedule"][day]["end"] = f"No end time on {day}"
    # Mode
    for day in days:
        try:
            if (
                data["schedule"]["mode"][day]
                != conf["calendar"]["schedule"][day]["mode"]
            ):
                parameters["status"] = "Error"
                parameters["schedule"][day]["mode"] = (
                    f"Record {day} mode: [{data['schedule']['mode'][day]}]. Correct {day} mode: [{conf['calendar']['schedule'][day]['mode']}]"
                )
            else:
                parameters["schedule"][day]["mode"] = "Okey"
        except KeyError:
            parameters["status"] = "Error"
            parameters["schedule"][day]["mode"] = f"No mode selected on {day}"

    if parameters["status"] == "Error":
        return parameters
    else:
        return "Okey"


@router.post("/", status_code=status.HTTP_200_OK)
async def revise(id_list: IDList):
    erp = Odoo()
    comprobations = []
    for id in id_list.ids:
        try:
            device = models.device(id)
            if device is not None:
                device["conf"] = erp.model_conf(device["model"])
                parameters = {
                    "id": "",
                    "status": "Okey",
                    "details": [],
                    "report": {
                        "name": {},
                        "ntp": {},
                        "dst": {},
                        "security": {},
                        "dns": {},
                        "mail": {},
                        "mstream": {},
                        "sstream": {},
                        "osd": {},
                        "overlay": {},
                        "motion": {},
                        "record": {},
                        "sderror": {},
                        "access": {},
                        "quota": {},
                        "sd": {},
                        "calendar": {},
                    },
                }

                parameters["id"] = str(id)

                # Module reading
                current_module = inspect.getmodule(inspect.currentframe())
                functions = dict(
                    inspect.getmembers(current_module, inspect.iscoroutinefunction)
                )

                # Listing function names
                excecution_order = [
                    "device_name",
                    "device_ntp",
                    "device_dst",
                    "device_security",
                    "device_dns",
                    "device_mail",
                    "device_mstream",
                    "device_sstream",
                    "device_osd",
                    "device_overlay",
                    "device_motion",
                    "device_record",
                    "device_sderror",
                    "device_access",
                    "device_quota",
                    "device_sd",
                    "device_calendar",
                ]

                # Loop to execute all functions inside this module
                for func_name in excecution_order:
                    if func_name in functions:
                        result = await functions[func_name](device)
                        key = func_name.split("_")[1]
                        if key in parameters["report"]:
                            parameters["report"][key] = result

                # Set status to error if something fails
                for v in parameters["report"].values():
                    if v != "Okey":
                        parameters["status"] = "Error"

                # Add to details sections that has errors
                for k, v in parameters["report"].items():
                    if v != "Okey" and k != "status":
                        parameters["details"].append(f"{k} error")

                # Set details to Okey if all is correct
                if parameters["status"] == "Okey":
                    parameters["details"] = "Correct device configuration"

                comprobations.append(parameters)

        except DeviceConnectionError as e:
            logging.error(f"Connection Error: {e}")
            comprobations.append({"id": str(id), "details": "Device connection Error"})
        except DeviceTimeoutError as e:
            logging.error(f"Timeout Error: {e}")
            comprobations.append(
                {"id": str(id), "details": "Timeout comunication Error"}
            )
        except DeviceRequestError as e:
            logging.error(f"Request Error: {e}")
            comprobations.append({"id": str(id), "details": f"Request Error: {e}"})
    return comprobations
