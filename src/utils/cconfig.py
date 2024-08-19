from .comunication import ISAPI
from pathlib import Path
import xml.etree.ElementTree as ET

class Cameras:
    def __init__(self, ip, password):
        self.ip = ip
        self.password = password

class Hikvision(Cameras):
    def __init__(self, ip, password):
        super().__init__(ip, password)
        self.xmlschema = '{http://www.hikvision.com/ver20/XMLSchema}'
        self.model = self.getmodel()
        self.gateway = self.defgateway()
        self.api = ISAPI(self.ip, self.password)
        self.act_dir = Path(__file__).parent
        self.directory = f'{self.act_dir}/xml/{self.model}/'
        
    #INFORMATION
    def defgateway(self): #Default gateway for the Hikvision camera API
        ip = self.ip.split('.')
        gateway = str(ip[0] + '.' + ip[1] + '.' + ip[2] + '.' + '1')
        return(gateway)
    
    def getmodel(self): #Check deviceInfo endpoint and filter <model> tag to get the camera model
        try:
            req = ISAPI(f'http://{self.ip}/ISAPI/System/deviceInfo', self.password)
            response = req.getapi()
            root = ET.fromstring(response.text)
            tag = f'{self.xmlschema}model'
            filtered = root.find(tag).text
            return(filtered)
        except Exception as e:
            return(f'Error {e}')
    
    def info(self): #Show camera info
        req = ISAPI(f'http://{self.ip}/ISAPI/System/deviceInfo', self.password)
        return(req.getapi())

    def getsn(self): #Ask camera S/N
        req = ISAPI(f'http://{self.ip}/ISAPI/System/deviceInfo', self.password)
        response = req.getapi()
        root = ET.fromstring(response.text)
        tag = f'{self.xmlschema}subSerialNumber'
        filtered = root.find(tag).text
        return(filtered)

    #XML UTILS
    def remove_namespace(self, root, tree, namespace):
        for elem in tree.iter():
            if '}' in elem.tag:
                elem.tag = elem.tag.split('}', 1)[1]
            if namespace in elem.attrib:
                del elem.attrib[namespace]
        if namespace in root.attrib:
            del root.attrib[namespace]

    #CONFIGURATIONS
    def putname(self, name): #Modify camera name
        req = ISAPI(f'http://{self.ip}/ISAPI/System/deviceInfo', self.password)
        data = f'<deviceName>{name}</deviceName>'
        parameter = req.putapi(data)
        return(parameter)
    
    def putosd(self, name): #Modifiy OSD
        #Change OSD name
        osd_req = ISAPI(f'http://{self.ip}/ISAPI/System/Video/inputs/channels/1', self.password)
        #osd_data = f'<name>{name}</deviceName>'
        
        
        osd_tree = ET.parse(f'{self.directory}osd.xml')
        osd_root = osd_tree.getroot()
        
        #Here we write the new named given to the function to a new XML file
        for osname in osd_root.iter(f'{self.xmlschema}name'):
            osname.text = f'{name}'
            osd_tree.write(f'{self.directory}osdcp.xml')
        
        #Now we call to a function that removes the namespace from the XML file
        self.remove_namespace(osd_root, osd_tree, self.xmlschema)
        osd_tree.write(f'{self.directory}osdcp.xml')

        #Save all the changes to the XML file before sending to the PUT request
        with open(f'{self.directory}osdcp.xml', 'r') as f:
            osd_xml = f.read()
            f.close()
        osd_conf = osd_req.putapi(osd_xml)
        
        #Change overlay settings (Date Format and Hide Week)
        over_req = ISAPI(f'http://{self.ip}/ISAPI/System/Video/inputs/channels/1/overlays', self.password)
        with open(f'{self.directory}overlay.xml', 'r') as f:
            over_xml = f.read()
            f.close()
        over_conf = over_req.putapi(over_xml)
        return(osd_conf, over_conf)

    def putmail(self, name, sys_name): #Modify mail configurations
        req = ISAPI(f'http://{self.ip}/ISAPI/System/network/mailing/1', self.password)
        
        tree = ET.parse(f'{self.directory}mail.xml')
        root = tree.getroot()

        for parent in root.iter(f'{self.xmlschema}sender'):
            for sender in parent.iter(f'{self.xmlschema}name'):
                sender.text = f'{name} {sys_name}'
                tree.write(f'{self.directory}mailcp.xml')
        
        self.remove_namespace(root, tree, self.xmlschema)
        tree.write(f'{self.directory}mailcp.xml')

        with open(f'{self.directory}mailcp.xml', 'r') as f:
            data_xml = f.read()
            f.close()

        config = req.putapi(data_xml)
        return(config)

    def sd_formatter(self): #Format camera SD card
        #Establish the image/video quota
        quota_req = ISAPI(f'http://{self.ip}/ISAPI/ContentMgmt/Storage/quota', self.password)
        with open(f'{self.directory}quota.xml', 'r') as f:
            quota_xml = f.read()
            f.close()
        quota_conf = quota_req.putapi(quota_xml)

        #Format the card
        format_req = ISAPI(f'http://{self.ip}/ISAPI/ContentMgmt/Storage/hdd/1/format?formatType="EXT4"', self.password)
        format_conf = format_req.putapi('')
        return(quota_conf, format_conf)

    def putime(self): #Configure "Time Settings" (Return actual device time)
        #NTP Configuration
        ntp_req = ISAPI(f'http://{self.ip}/ISAPI/System/time/ntpServers', self.password)
        with open(f'{self.directory}ntp.xml', 'r') as f:
            ntp_xml = f.read()
            f.close()
        ntp_req.putapi(ntp_xml)

        #DST Configuration
        time_req = ISAPI(f'http://{self.ip}/ISAPI/System/time', self.password)
        with open(f'{self.directory}dst.xml', 'r') as f:
            time_xml = f.read()
            f.close()
        time_req.putapi(time_xml)

        #Time request
        h_req = ISAPI(f'http://{self.ip}/ISAPI/System/time/localTime', self.password)
        return(h_req.getapi())
    
    def putsec(self): #Configure "Security" settings
        websec_req = ISAPI(f'http://{self.ip}/ISAPI/Security/webCertificate', self.password)
        with open(f'{self.directory}security.xml', 'r') as f:
            sec_xml = f.read()
            f.close()
        websec_conf = websec_req.putapi(sec_xml)

        rtspsec_req = ISAPI(f'http://{self.ip}/ISAPI/Streaming/channels/101', self.password)
        with open(f'{self.directory}rtspsec.xml', 'r') as f:
            rtspsec_xml = f.read()
            f.close()
        rtsp_conf = rtspsec_req.putapi(rtspsec_xml)

        return(websec_conf, rtsp_conf)

    def putnet(self): #DNS Configuration
        #Discovery Mode configuration
        discmode_req = ISAPI(f'http://{self.ip}/ISAPI/System/discoveryMode', self.password)
        with open(f'{self.directory}discovery.xml', 'r') as f:
            discmode_xml = f.read()
            f.close()
        discmode_conf = discmode_req.putapi(discmode_xml)

        #Fill DNS fields
        dns_req = ISAPI(f'http://{self.ip}/ISAPI/System/Network/interfaces/1', self.password)
        dns_tree = ET.parse(f'{self.directory}dns.xml')
        dns_root = dns_tree.getroot()

        #Set the IP camera field with it's own IP
        for camip in dns_root.iter(f'{self.xmlschema}ipAddress'):
            camip.text = f'{self.ip}'
            dns_tree.write(f'{self.directory}dnscp.xml')

        self.remove_namespace(dns_root, dns_tree, self.xmlschema)
        dns_tree.write(f'{self.directory}dnscp.xml')

        #Parsing another time the new XML File
        dnscp_tree = ET.parse(f'{self.directory}dnscp.xml')
        dnscp_root = dnscp_tree.getroot()

        #Change the previous writings to correct the Gateway
        for parent1 in dnscp_root.iter('DefaultGateway'):
            for routip in parent1.iter('ipAddress'):
                routip.text = f'{self.gateway}'
                dnscp_tree.write(f'{self.directory}dnscp.xml')
        
        #Setting Primary DNS
        for parent2 in dnscp_root.iter('PrimaryDNS'):
            for mdns in parent2.iter('ipAddress'):
                mdns.text = '8.8.8.8'
                dnscp_tree.write(f'{self.directory}dnscp.xml')
        
        #Setting the secondary DNS
        for parent3 in dnscp_root.iter('SecondaryDNS'):
            for sdns in parent3.iter('ipAddress'):
                sdns.text = '8.8.4.4'
                dnscp_tree.write(f'{self.directory}dnscp.xml')
         
        with open(f'{self.directory}dnscp.xml', 'r') as f:
            dns_xml = f.read()
            f.close()

        dns_conf = dns_req.putapi(dns_xml)

        return(discmode_conf, dns_conf)

    def putvideo(self, name): #Configure video parameters
        #Configure Main-Stream video
        mainvid_req = ISAPI(f'http://{self.ip}/ISAPI/Streaming/channels/101', self.password)
        mainvid_tree = ET.parse(f'{self.directory}mstream.xml')
        mainvid_root = mainvid_tree.getroot()

        for mvid in mainvid_root.iter(f'{self.xmlschema}channelName'):
            mvid.text = f'{name}'
            mainvid_tree.write(f'{self.directory}mstreamcp.xml')
        
        self.remove_namespace(mainvid_root, mainvid_tree, self.xmlschema)
        mainvid_tree.write(f'{self.directory}mstreamcp.xml')

        with open(f'{self.directory}mstreamcp.xml', 'r') as f:
            mainvid_xml = f.read()
            f.close()

        mainvid_conf = mainvid_req.putapi(mainvid_xml)

        #Configure Sub-Stream video
        subvid_req = ISAPI(f'http://{self.ip}/ISAPI/Streaming/channels/102', self.password)
        subvid_tree = ET.parse(f'{self.directory}sstream.xml')
        subvid_root = subvid_tree.getroot()
                
        for svid in subvid_root.iter(f'{self.xmlschema}channelName'):
            svid.text = f'{name}'
            subvid_tree.write(f'{self.directory}sstreamcp.xml')
        
        self.remove_namespace(subvid_root, subvid_tree, self.xmlschema)
        subvid_tree.write(f'{self.directory}sstreamcp.xml')

        with open(f'{self.directory}sstreamcp.xml', 'r') as f:
            subvid_xml = f.read()
            f.close()
        
        subvid_conf = subvid_req.putapi(subvid_xml)

        return(mainvid_conf, subvid_conf)

    def putevents(self): #Configure Motion Detection and Exceptions
        #Motion Detection
        motion_req = ISAPI(f'http://{self.ip}/ISAPI/System/Video/inputs/channels/1/motionDetection', self.password)
        with open(f'{self.directory}motion.xml', 'r') as f:
            motion_xml = f.read()
            f.close()
        motion_conf = motion_req.putapi(motion_xml)

        #Motion Recording Trigger
        trigger_req = ISAPI(f'http://{self.ip}/ISAPI/Event/triggers/VMD-1', self.password)
        with open(f'{self.directory}vmdtrigger.xml', 'r') as f:
            trigger_xml = f.read()
            f.close()
        trigger_conf = trigger_req.putapi(trigger_xml)

        #HDD Error Exception
        hddexcep_req = ISAPI(f'http://{self.ip}/ISAPI/Event/triggers/diskerror', self.password)
        with open(f'{self.directory}disktrigger.xml', 'r') as f:
            hddexcep_xml = f.read()
            f.close()
        hddexcep_conf = hddexcep_req.putapi(hddexcep_xml)

        #Ilegal Login Exception
        logexcep_req = ISAPI(f'http://{self.ip}/ISAPI/Event/triggers/illaccess', self.password)
        with open(f'{self.directory}illtrigger.xml', 'r') as f:
            logexcep_xml = f.read()
            f.close()
        logexcep_conf = logexcep_req.putapi(logexcep_xml)

        #Motion Detection Schedule
        schedule_req = ISAPI(f'http://{self.ip}/ISAPI/Event/schedules/motionDetections/VMD_video1', self.password)
        with open(f'{self.directory}schtrigger.xml', 'r') as f:
            schedule_xml = f.read()
            f.close()
        schedule_conf = schedule_req.putapi(schedule_xml)

        return(motion_conf, trigger_conf, schedule_conf, hddexcep_conf, logexcep_conf)
    
    def putschedule(self): #Configure recording calendar
        sch_req = ISAPI(f'http://{self.ip}/ISAPI/ContentMgmt/record/tracks', self.password)
        with open(f'{self.directory}calendar.xml', 'r') as f:
            sch_xml = f.read()
            f.close()
        sch_conf = sch_req.putapi(sch_xml)

        return(sch_conf)

    def upfirmware(self): #Firmware Updater
        #Check camera Firmware version
        req = ISAPI(f'http://{self.ip}/ISAPI/System/deviceInfo', self.password)
        req_get = req.getapi()
        root = ET.fromstring(req_get.text)

        for x in root.iter(f'{self.xmlschema}firmwareVersion'):
            version = x.text

        #Check local Firmware
        local_version_file = open(f'{self.act_dir}/firmwares/{self.model}/Version.txt', 'r')
        for ver in local_version_file.readlines():    
            local_version_list = ver.split('.')
        
        cam_ver_str = version.replace('V', '')
        cam_ver_list = cam_ver_str.split('.')

        up_req = ISAPI(f'http://{self.ip}/ISAPI/System/updateFirmware', self.password)

        with open(f'{self.act_dir}/firmwares/{self.model}/digicap.dav', 'rb') as f:
            firmware = f.read()
            f.close()

        if cam_ver_list[0] < local_version_list[0]:
            up_req.putapi(firmware)
            return('Actualizando...')
        elif cam_ver_list[0] > local_version_list[0]:
            return('NUEVO FIRMWARE!!!')
        elif cam_ver_list[0] == local_version_list[0]:
            if cam_ver_list[1] < local_version_list[1]:
                up_req.putapi(firmware)
                return('Actualizando...')
            elif cam_ver_list[1] > local_version_list[1]:
                return('NUEVO FIRMWARE!!!')
            elif cam_ver_list[1] == local_version_list[1]:
                if cam_ver_list[2] < local_version_list[2]:
                    up_req.putapi(firmware)
                    return('Actualizando...')
                elif cam_ver_list[2] > local_version_list[2]:
                    return('NUEVO FIRMWARE!!!')
                elif cam_ver_list[2] == local_version_list[2]:
                    return('FIRMWARE ACTUALIZADO')
    
    def reboot(self): #Camera Reboot
        req = ISAPI(f'http://{self.ip}/ISAPI/System/reboot', self.password)
        reboot = req.putapi('')
        return(reboot)

    def configurate(self, name, sys_name): #Execute all configurations
        try:
            self.putname(name)
            self.putvideo(name)
            self.putmail(name, sys_name)
            self.putime()
            self.putsec()
            self.putnet()
            self.putevents()
            self.putschedule()
            self.putosd(name)
            self.sd_formatter()
            self.upfirmware()
            self.reboot()
            return(f'Configurada camara {name}')
        except Exception as e:
            return(f'ERROR [{e}]')