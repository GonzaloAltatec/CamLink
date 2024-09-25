#FastAPI imports
from fastapi import APIRouter, Depends, HTTPException, status
#SQLAlchemy Session import
from sqlalchemy.orm import Session
#Database import
from ..utils.db import models, database
#Hikvision API operator
from ..utils.operations import Hikvision as Hik
#JSON Library
import json
#File path Library
from pathlib import Path

router = APIRouter(
    tags=['reviser'],
    prefix='/revise'
)

#Get device element from DB and show data
@router.get('/{id}/db-info', status_code=status.HTTP_200_OK) 
def db_info(id:int, db:Session=Depends(database.get_db)):
    device = db.query(models.Device).filter(models.Device.id == id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return device

#Check if DeviceName match with Odoo DeviceName
@router.get('/{id}/name', status_code=status.HTTP_200_OK) 
def device_name(id:int, db:Session=Depends(database.get_db)):
    device = db.query(models.Device).filter(models.Device.id == id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    api = Hik(device.ip, device.password)
    data = api.getname()
    if data != device.name:
        return {'status': 'Incorrect Name',
                'device_name': data,
                'odoo_name': device.name}
    else:
        return(status.HTTP_200_OK)

#Check NTP configuration
@router.get('/{id}/ntp', status_code=status.HTTP_200_OK) 
def device_ntp(id:int, db:Session=Depends(database.get_db)):
    device = db.query(models.Device).filter(models.Device.id == id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    api = Hik(device.ip, device.password)
    data = api.getntp()
    conf_path = Path('src') / 'utils' / 'configurations' / f'{device.model}.json'
    with open(conf_path, 'r') as f:
        conf = json.load(f)

    parameters = {'status': '', 'server': '', 'sync': ''}
    #NTP server check (Default: es.pool.ntp.org)
    if data['server'] != conf['ntp']['server']:
        parameters['status'] = 'Error'
        parameters['server'] = 'Error'
    else:
        parameters['server'] = 'Correct'
    
    #Synchronization check
    if data['sync'] != conf['ntp']['sync']:
        parameters['status'] = 'Error'
        parameters['sync'] = 'Error'
    else:
        parameters['sync'] = 'Correct'

    #Check parameter errors and return device config status
    if parameters['server'] == 'Error' or parameters['sync'] == 'Error':
        return(parameters)
    else:
        return(status.HTTP_200_OK)

#Check DST configuration
@router.get('/{id}/dst', status_code=status.HTTP_200_OK) 
def device_dst(id:int, db:Session=Depends(database.get_db)):
    device = db.query(models.Device).filter(models.Device.id == id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    api = Hik(device.ip, device.password)
    data = api.getdst()
    conf_path = Path('src') / 'utils' / 'configurations' / f'{device.model}.json'
    with open(conf_path, 'r') as f:
        conf = json.load(f)
    parameters = {'status': '', 'mode': '', 'timezone': ''}

    #Server check
    if data['mode'] != conf['dst']['mode']:
        parameters['status'] = 'Error'
        parameters['mode'] = 'Error'
    else:
        parameters['mode'] = 'Correct'
    
    #Synchronization check
    if data['timezone'] != conf['dst']['timezone']:
        parameters['status'] = 'Error'
        parameters['timezone'] = 'Error'
    else:
        parameters['sync'] = 'Correct'

    #Check parameter errors and return device config status
    if parameters['mode'] == 'Error' or parameters['timezone'] == 'Error':
        return(parameters)
    else:
        return(status.HTTP_200_OK)

#Check Security configuration
@router.get('/{id}/security', status_code=status.HTTP_200_OK) 
def device_security(id:int, db:Session=Depends(database.get_db)):
    device = db.query(models.Device).filter(models.Device.id == id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    api = Hik(device.ip, device.password)
    data = api.getsec()
    conf_path = Path('src') / 'utils' / 'configurations' / f'{device.model}.json'
    with open(conf_path, 'r') as f:
        conf = json.load(f)

    parameters = {'status': '', 'web': '', 'rtsp': ''}
    #Web Authentication check
    if data['web_sec'] != conf['security']['web']:
        parameters['status'] = 'Error'
        parameters['web'] = 'Error'
    else:
        parameters['web'] = 'Correct'
    
    #RSTP Authentication check
    if data['rtsp_sec'] != conf['security']['rtsp']:
        parameters['status'] = 'Error'
        parameters['rtsp'] = 'Error'
    else:
        parameters['rtsp'] = 'Correct'

    #Check parameter errors and return device config status
    if parameters['web'] == 'Error' or parameters['rtsp'] == 'Error':
        return(parameters)
    else:
        return(status.HTTP_200_OK)

#Check DNS configuration
@router.get('/{id}/dns', status_code=status.HTTP_200_OK) 
def device_dns(id:int, db:Session=Depends(database.get_db)):
    device = db.query(models.Device).filter(models.Device.id == id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    api = Hik(device.ip, device.password)
    data = api.getdns()
    conf_path = Path('src') / 'utils' / 'configurations' / f'{device.model}.json'
    with open(conf_path, 'r') as f:
        conf = json.load(f)

    parameters = {'status': '', 'primary': '', 'secondary': ''}
    #Primary DNS check
    if data['primary'] != conf['dns']['primary']:
        parameters['status'] = 'Error'
        parameters['primary'] = 'Error'
    else:
        parameters['primary'] = 'Correct'
    
    #Secondary DNS check
    if data['secondary'] != conf['dns']['secondary']:
        parameters['status'] = 'Error'
        parameters['secondary'] = 'Error'
    else:
        parameters['secondary'] = 'Correct'

    #Check parameter errors and return device config status
    if parameters['primary'] == 'Error' or parameters['secondary'] == 'Error':
        return(parameters)
    else:
        return(status.HTTP_200_OK)

#Check Mail configuration
@router.get('/{id}/email', status_code=status.HTTP_200_OK) 
def device_mail(id:int, db:Session=Depends(database.get_db)):
    device = db.query(models.Device).filter(models.Device.id == id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    api = Hik(device.ip, device.password)
    data = api.getmail()
    conf_path = Path('src') / 'utils' / 'configurations' / f'{device.model}.json'
    with open(conf_path, 'r') as f:
        conf = json.load(f)

    parameters = {'status': '', 'name': '', 'sender': '', 'server': '', 'port': '', 'receiver': '', 'email': ''}
    #Check device sender name
    if data['name'] != f'{device.name} {device.installation}':
        parameters['status'] = 'Error'
        parameters['name'] = 'Error'
    else:
        parameters['name'] = 'Correct'
    
    #SMTP Server
    if data['server'] != conf['mail']['server']:
        parameters['status'] = 'Error'
        parameters['server'] = 'Error'
    else:
        parameters['server'] = 'Correct'

    #SMTP Port
    if data['port'] != conf['mail']['port']:
        parameters['status'] = 'Error'
        parameters['port'] = 'Error'
    else:
        parameters['port'] = 'Correct'

    #Sender email
    if data['sender'] != conf['mail']['sender']:
        parameters['status'] = 'Error'
        parameters['sender'] = 'Error'
    else:
        parameters['sender'] = 'Correct'

    #Receiver Name
    if data['receiver'] != conf['mail']['receiver']:
        parameters['status'] = 'Error'
        parameters['receiver'] = 'Error'
    else:
        parameters['receiver'] = 'Correct'

    #Receiver email
    if data['email'] != conf['mail']['email']:
        parameters['status'] = 'Error'
        parameters['email'] = 'Error'
    else:
        parameters['email'] = 'Correct'

    #Check parameter errors and return device config status
    if parameters['name'] == 'Error' or parameters['server'] == 'Error' or parameters['port'] == 'Error' or parameters['sender'] == 'Error' or parameters['receiver'] == 'Error' or parameters['email'] == 'Error':
        return(parameters)
    else:
        return(status.HTTP_200_OK)

#Check Main Stream configuration
@router.get('/{id}/mstream', status_code=status.HTTP_200_OK) 
def device_mstream(id:int, db:Session=Depends(database.get_db)):
    device = db.query(models.Device).filter(models.Device.id == id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    api = Hik(device.ip, device.password)
    data = api.getmstream()
    conf_path = Path('src') / 'utils' / 'configurations' / f'{device.model}.json'
    with open(conf_path, 'r') as f:
        conf = json.load(f)

    parameters = {'status': '', 'name': '', 'encoding': '', 'plus': '', 'width': '', 'height': '', 'bitrate': '', 'average': '', 'fps': ''}
    #Channel Name
    if data['name'] != device.name:
        parameters['status'] = 'Error'
        parameters['name'] = 'Error'
    else:
        parameters['name'] = 'Correct'
    
    #H.265 Encoding
    if data['encoding'] != conf['mstream']['encoding']:
        parameters['status'] = 'Error'
        parameters['encoding'] = 'Error'
    else:
        parameters['encoding'] = 'Correct'

    #H.265 Plus
    if data['plus'] != conf['mstream']['plus']:
        parameters['status'] = 'Error'
        parameters['plus'] = 'Error'
    else:
        parameters['plus'] = 'Correct'

    #Video Width
    if data['width'] != conf['mstream']['width']:
        parameters['status'] = 'Error'
        parameters['width'] = 'Error'
    else:
        parameters['width'] = 'Correct'

    #Video Height
    if data['height'] != conf['mstream']['height']:
        parameters['status'] = 'Error'
        parameters['height'] = 'Error'
    else:
        parameters['height'] = 'Correct'

    #Max. Bitrate
    if data['bitrate'] != conf['mstream']['bitrate']:
        parameters['status'] = 'Error'
        parameters['bitrate'] = 'Error'
    else:
        parameters['bitrate'] = 'Correct'

    #Min. Bitrate
    if data['average'] != conf['mstream']['average']:
        parameters['status'] = 'Error'
        parameters['average'] = 'Error'
    else:
        parameters['average'] = 'Correct'

    #FPS
    if data['fps'] != conf['mstream']['fps']:
        parameters['status'] = 'Error'
        parameters['fps'] = 'Error'
    else:
        parameters['fps'] = 'Correct'

    #Check parameter errors and return device config status
    if parameters['status'] == 'Error':
        return(parameters)
    else:
        return(status.HTTP_200_OK)

#Check Sub Stream configuration
@router.get('/{id}/sstream', status_code=status.HTTP_200_OK) 
def device_sstream(id:int, db:Session=Depends(database.get_db)):
    device = db.query(models.Device).filter(models.Device.id == id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    api = Hik(device.ip, device.password)
    data = api.getsstream()
    conf_path = Path('src') / 'utils' / 'configurations' / f'{device.model}.json'
    with open(conf_path, 'r') as f:
        conf = json.load(f)

    parameters = {'status': '', 'name': '', 'encoding': '', 'width': '', 'height': '', 'bitrate': '', 'fps': ''}
    #Channel Name
    if data['name'] != device.name:
        parameters['status'] = 'Error'
        parameters['name'] = 'Error'
    else:
        parameters['name'] = 'Correct'
    
    #H.265 Encoding
    if data['encoding'] != conf['sstream']['encoding']:
        parameters['status'] = 'Error'
        parameters['encoding'] = 'Error'
    else:
        parameters['encoding'] = 'Correct'

    #Video Width
    if data['width'] != conf['sstream']['width']:
        parameters['status'] = 'Error'
        parameters['width'] = 'Error'
    else:
        parameters['width'] = 'Correct'

    #Video Height
    if data['height'] != conf['sstream']['height']:
        parameters['status'] = 'Error'
        parameters['height'] = 'Error'
    else:
        parameters['height'] = 'Correct'

    #Max. Bitrate
    if data['bitrate'] != conf['sstream']['bitrate']:
        parameters['status'] = 'Error'
        parameters['bitrate'] = 'Error'
    else:
        parameters['bitrate'] = 'Correct'
  
    #FPS
    if data['fps'] != conf['sstream']['fps']:
        parameters['status'] = 'Error'
        parameters['fps'] = 'Error'
    else:
        parameters['fps'] = 'Correct'

    #Check parameter errors and return device config status
    if parameters['status'] == 'Error':
        return(parameters)
    else:
        return(status.HTTP_200_OK)

#Check if OSD Show name match with Odoo name field
@router.get('/{id}/osd', status_code=status.HTTP_200_OK)
def device_osd(id:int, db:Session=Depends(database.get_db)):
    device = db.query(models.Device).filter(models.Device.id == id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    api = Hik(device.ip, device.password)
    data = api.getosd()
    
    if data != device.name:
        return('Error')
    else:
        return(status.HTTP_200_OK)

#Overlay data showing format check
@router.get('/{id}/overlays', status_code=status.HTTP_200_OK)
def device_overlay(id:int, db:Session=Depends(database.get_db)):
    device = db.query(models.Device).filter(models.Device.id == id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    api = Hik(device.ip, device.password)
    data = api.getoverlay()
    conf_path = Path('src') / 'utils' / 'configurations' / f'{device.model}.json'
    with open(conf_path, 'r') as f:
        conf = json.load(f)

    parameters = {'status': '', 'week': '', 'format': ''}
    
    #No Week Display
    if data['week'] != conf['overlays']['week']:
        parameters['status'] = 'Error'
        parameters['week'] = 'Error'
    else:
        parameters['week'] = 'Correct'

    #Date Format
    if data['format'] != conf['overlays']['format']:
        parameters['status'] = 'Error'
        parameters['format'] = 'Error'
    else:
        parameters['format'] = 'Correct'

    #Check configuration Status
    if parameters['status'] == 'Error':
        return(parameters)
    else:
        return(status.HTTP_200_OK)

#Motion event configurations
@router.get('/{id}/motion', status_code=status.HTTP_200_OK)
def device_motion(id:int, db:Session=Depends(database.get_db)):
    device = db.query(models.Device).filter(models.Device.id == id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    api = Hik(device.ip, device.password)
    data = api.getmotion()
    conf_path = Path('src') / 'utils' / 'configurations' / f'{device.model}.json'
    with open(conf_path, 'r') as f:
        conf = json.load(f)

    parameters = {'status': '', 'enabled': '', 'grid': '', 'sensitivity': '', 'target': ''}

    #Enabled
    if data['enabled'] != conf['motion']['enabled']:
        parameters['status'] = 'Error'
        parameters['enabled'] = 'Error'
    else:
        parameters['enabled'] = 'Correct'

    #Grid Map
    if data['grid'] != conf['motion']['grid']:
        parameters['status'] = 'Error'
        parameters['grid'] = 'Error'
    else:
        parameters['grid'] = 'Correct'

    #Sensitivity Level
    if data['sensitivity'] != conf['motion']['sensitivity']:
        parameters['status'] = 'Error'
        parameters['sensitivity'] = 'Error'
    else:
        parameters['sensitivity'] = 'Correct'

    #Target Type
    if data['target'] != conf['motion']['target']:
        parameters['status'] = 'Error'
        parameters['target'] = 'Error'
    else:
        parameters['target'] = 'Correct'

    if parameters['status'] == 'Error':
        return parameters
    else:
        return (status.HTTP_200_OK)

#Recording enabled
@router.get('/{id}/record', status_code=status.HTTP_200_OK)
def device_record(id:int, db:Session=Depends(database.get_db)):
    device = db.query(models.Device).filter(models.Device.id == id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    api = Hik(device.ip, device.password)
    data = api.getrecord()
    conf_path = Path('src') / 'utils' / 'configurations' / f'{device.model}.json'
    with open(conf_path, 'r') as f:
        conf = json.load(f)

    parameters = {'status': '', 'target': '', 'method': ''}

    #Motion Detection > Linkage Method > Trigger Recording
    if data['target'] != conf['record']['target']:
        parameters['status'] = 'Error'
        parameters['target'] = 'Error'
    else:
        parameters['target'] = 'Correct'

    #Record activated
    if data['method'] != conf['record']['method']:
        parameters['status'] = 'Error'
        parameters['method'] = 'Error'
    else:
        parameters['method'] = 'Correct'

    if parameters['status'] == 'Error':
        return (parameters)
    else:
        return(status.HTTP_200_OK)

#SD Error Exception
@router.get('/{id}/sderror', status_code=status.HTTP_200_OK)
def device_sderror(id:int, db:Session=Depends(database.get_db)):
    device = db.query(models.Device).filter(models.Device.id == id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    api = Hik(device.ip, device.password)
    data = api.getsderr()

    conf_path = Path('src') / 'utils' / 'configurations' / f'{device.model}.json'
    with open(conf_path, 'r') as f:
        conf = json.load(f)

    parameters = {'status': '', 'method': ''}

    #Email send when exception occurs
    if data != conf['exceptions']['disk']:
        parameters['status'] = 'Error'
        parameters['method'] = 'Error'
    else:
        parameters['method'] = 'Correct'

    if parameters['status'] == 'Error':
        return(parameters)
    else:
        return(status.HTTP_200_OK)

#Illegal Access Exception
@router.get('/{id}/illaccess', status_code=status.HTTP_200_OK)
def device_access(id:int, db:Session=Depends(database.get_db)):
    device = db.query(models.Device).filter(models.Device.id == id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    api = Hik(device.ip, device.password)
    data = api.getillaccess()

    conf_path = Path('src') / 'utils' / 'configurations' / f'{device.model}.json'
    with open(conf_path, 'r') as f:
        conf = json.load(f)

    parameters = {'status': '', 'method': ''}

    #Email send when exception occurs
    if data != conf['exceptions']['login']:
        parameters['status'] = 'Error'
        parameters['method'] = 'Error'
    else:
        parameters['method'] = 'Correct'

    if parameters['status'] == 'Error':
        return(parameters)
    else:
        return(status.HTTP_200_OK)

#SD Quota
@router.get('/{id}/quota', status_code=status.HTTP_200_OK)
def device_quota(id:int, db:Session=Depends(database.get_db)):
    device = db.query(models.Device).filter(models.Device.id == id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    api = Hik(device.ip, device.password)
    data = api.getquota()

    conf_path = Path('src') / 'utils' / 'configurations' / f'{device.model}.json'
    with open(conf_path, 'r') as f:
        conf = json.load(f)

    parameters = {'status': '', 'picture': '', 'video': ''}

    if data['picture'] != conf['quota']['picture']:
        parameters['status'] = 'Error'
        parameters['picture'] = 'Error'
    else:
        parameters['picture'] = 'Correct'

    if data['video'] != conf['quota']['video']:
        parameters['status'] = 'Error'
        parameters['video'] = 'Error'
    else:
        parameters['video'] = 'Correct'

    if parameters['status'] == 'Error':
        return (parameters)
    else:
        return(status.HTTP_200_OK)

#SD Info
@router.get('/{id}/sd', status_code=status.HTTP_200_OK)
def device_sd(id:int, db:Session=Depends(database.get_db)):
    device = db.query(models.Device).filter(models.Device.id == id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    api = Hik(device.ip, device.password)
    data = api.getsd()

    conf_path = Path('src') / 'utils' / 'configurations' / f'{device.model}.json'
    with open(conf_path, 'r') as f:
        conf = json.load(f)

    parameters = {'status': '', 'capacity': '', 'state': ''}

    if data['capacity'] != conf['sd']['capacity']:
        parameters['status'] = 'Error'
        parameters['capacity'] = 'Error'
    else:
        parameters['capacity'] = 'Correct'

    if data['state'] != conf['sd']['state']:
        parameters['status'] = 'Error'
        parameters['state'] = 'Error'
    else:
        parameters['state'] = 'Correct'

    if parameters['status'] == 'Error':
        return (parameters)
    else:
        return(status.HTTP_200_OK)

#Calendar
@router.get('/{id}/calendar', status_code=status.HTTP_200_OK)
def device_calendar(id:int, db:Session=Depends(database.get_db)):
    device = db.query(models.Device).filter(models.Device.id == id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    api = Hik(device.ip, device.password)
    data = api.getcalendar()

    conf_path = Path('src') / 'utils' / 'configurations' / f'{device.model}.json'
    with open(conf_path, 'r') as f:
        conf = json.load(f)

    parameters = {'status': '', 
                  'enabled': '',
                  'advanced': {'overwrite': '',
                               'prerecord': '',
                               'postrecord': '',
                               'expiration': '',
                               'duration': ''},
                  'schedule': {'Monday': {'start': '', 'end': '', 'mode': ''}, 
                                             'Tuesday': {'start': '', 'end': '', 'mode': ''}, 
                                             'Wednesday': {'start': '', 'end': '', 'mode': ''}, 
                                             'Thursday': {'start': '', 'end': '', 'mode': ''}, 
                                             'Friday': {'start': '', 'end': '', 'mode': ''}, 
                                             'Saturday': {'start': '', 'end': '', 'mode': ''}, 
                                             'Sunday': {'start': '', 'end': '', 'mode': ''}}}

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    #Enabled
    for day in days:
        if data['enabled'] != conf['calendar']['enabled']:
            parameters['status'] = 'Error'
            parameters['enabled'] = 'Error'
    else:
            parameters['enabled'] = 'Correct'
    
    #Overwrite
    for day in days:
        if data['advanced']['overwrite'] != conf['calendar']['advanced']['overwrite']:
            parameters['status'] = 'Error'
            parameters['advanced']['overwrite'] = 'Error'
        else:
            parameters['advanced']['overwrite'] = 'Correct'
    
    #Pre-Record
    for day in days:
        if data['advanced']['prerecord'] != conf['calendar']['advanced']['prerecord']:
            parameters['status'] = 'Error'
            parameters['advanced']['prerecord'] = 'Error'
        else:
            parameters['advanced']['prerecord'] = 'Correct'

    #Post-Record
    for day in days:
        if data['advanced']['postrecord'] != conf['calendar']['advanced']['postrecord']:
            parameters['status'] = 'Error'
            parameters['advanced']['postrecord'] = 'Error'
        else:
            parameters['advanced']['postrecord'] = 'Correct'

    model = str(device.model)
    if model == 'DS-2CD2183G2-IU':
        #Expiration Enabled
        for day in days:
            if data['advanced']['expiration'] != conf['calendar']['advanced']['expiration']:
                parameters['status'] = 'Error'
                parameters['advanced']['expiration'] = 'Error'
            else:
                parameters['advanced']['expiration'] = 'Correct'

        #Expiration Duration
        for day in days:
            if data['advanced']['duration'] != conf['calendar']['advanced']['duration']:
                parameters['status'] = 'Error'
                parameters['advanced']['duration'] = 'Error'
            else:
                parameters['advanced']['duration'] = 'Correct'

    #Start Time
    for day in days:
        if data['schedule']['start'][day] != conf['calendar']['schedule'][day]['start']:
            parameters['status'] = 'Error'
            parameters['schedule'][day]['start'] = 'Error'
        else:
            parameters['schedule'][day]['start'] = 'Correct'

    #End Time
    for day in days:
        if data['schedule']['end'][day] != conf['calendar']['schedule'][day]['end']:
            parameters['status'] = 'Error'
            parameters['schedule'][day]['end'] = 'Error'
        else:
            parameters['schedule'][day]['end'] = 'Correct'

    #Mode
    for day in days:
        if data['schedule']['mode'][day] != conf['calendar']['schedule'][day]['mode']:
            parameters['status'] = 'Error'
            parameters['schedule'][day]['mode'] = 'Error'
        else:
            parameters['schedule'][day]['mode'] = 'Correct'
 
    if parameters['status'] == 'Error':
        return (parameters)
    else:
        return(status.HTTP_200_OK)

@router.get('/{id}/', status_code=status.HTTP_200_OK)
def revise(id:int, db:Session=Depends(database.get_db)):
    parameters = {'status': '200',
                  'name': '',
                  'ntp': '',
                  'dst': '',
                  'security': '',
                  'dns': '',
                  'email': '',
                  'mstream': '',
                  'sstream': '',
                  'osd': '',
                  'overlay': '',
                  'motion': '',
                  'record': '',
                  'sderror': '',
                  'illaccess': '',
                  'quota': '',
                  'sd': '',
                  'calendar': ''}

    name_call = device_name(id, db)
    parameters['name'] = str(name_call)

    ntp_call = device_ntp(id, db)
    parameters['ntp'] = str(ntp_call)

    dst_call = device_dst(id, db)
    parameters['dst'] = str(dst_call)

    security_call = device_security(id, db)
    parameters['security'] = str(security_call)

    dns_call = device_dns(id, db)
    parameters['dns'] = str(dns_call)

    email_call = device_mail(id, db)
    parameters['email'] = str(email_call)

    mstream_call = device_mstream(id, db)
    parameters['mstream'] = str(mstream_call)

    sstream_call = device_sstream(id, db)
    parameters['sstream'] = str(sstream_call)

    osd_call = device_osd(id, db)
    parameters['osd'] = str(osd_call)

    overlay_call = device_overlay(id, db)
    parameters['overlay'] = str(overlay_call)

    motion_call = device_motion(id, db)
    parameters['motion'] = str(motion_call)

    record_call = device_record(id, db)
    parameters['record'] = str(record_call)

    sderror_call = device_sderror(id, db)
    parameters['sderror'] = str(sderror_call)

    illaccess_call = device_access(id, db)
    parameters['illaccess'] = str(illaccess_call)

    quota_call = device_quota(id, db)
    parameters['quota'] = str(quota_call)

    sd_call = device_sd(id, db)
    parameters['sd'] = str(sd_call)

    calendar_call = device_calendar(id, db)
    parameters['calendar'] = str(calendar_call)

    for x in parameters.values():
        if x != '200':
            parameters['status'] = '400'

    return(parameters)
