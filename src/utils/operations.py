from .comunication import ISAPI
from pathlib import Path
import xml.etree.ElementTree as ET
from .exceptions import DeviceRequestError, DeviceConnectionError, DeviceTimeoutError


class Hikvision:
    def __init__(self, ip, password):
        self.ip = ip
        self.password = password
        self.xmlschema = "{http://www.hikvision.com/ver20/XMLSchema}"
        self.namespace = {"ns": "http://www.hikvision.com/ver20/XMLSchema"}
        self.model = self.getmodel()
        self.gateway = self.defgateway()
        self.api = ISAPI(self.ip, self.password)
        self.act_dir = Path(__file__).parent
        self.directory = f"{self.act_dir}/xml/{self.model}/"

    # --------------------------------------------------------------------------
    # XML UTILS
    def remove_namespace(self, root, tree, namespace):
        for elem in tree.iter():
            if "}" in elem.tag:
                elem.tag = elem.tag.split("}", 1)[1]
            if namespace in elem.attrib:
                del elem.attrib[namespace]
        if namespace in root.attrib:
            del root.attrib[namespace]

    # --------------------------------------------------------------------------
    # CLASS DATA
    def defgateway(self):  # Default gateway for the Hikvision camera API
        ip = self.ip.split(".")
        gateway = str(ip[0] + "." + ip[1] + "." + ip[2] + "." + "1")
        return gateway

    def getmodel(
        self,
    ):  # Check deviceInfo endpoint and filter <model> tag to get the camera model
        try:
            req = ISAPI(f"http://{self.ip}/ISAPI/System/deviceInfo", self.password)
            response = str(req.getapi())
            if not response:
                raise DeviceRequestError("Request Error")
            root = ET.ElementTree(ET.fromstring(response))
            model_tag = root.find("ns:model", self.namespace)
            model_text = model_tag.text if model_tag is not None else None
            return model_text

        except DeviceConnectionError as e:
            return e
        except DeviceTimeoutError as e:
            print(e)
        except DeviceRequestError as e:
            print(e)
        except ET.ParseError:
            print("Error al analizar el XML de la respuesta")
        return None

    # --------------------------------------------------------------------------
    # INFORMATION
    def info(self):  # Show device info (Not working on API Response)
        try:
            req = ISAPI(f"http://{self.ip}/ISAPI/System/deviceInfo", self.password)
            response = req.getapi()
            return response

        except DeviceConnectionError as e:
            return e
        except DeviceTimeoutError as e:
            print(e)
        except DeviceRequestError as e:
            print(e)
        except ET.ParseError:
            print("Error al analizar el XML de la respuesta")
        return None

    # GET device name
    def getname(self):
        req = ISAPI(f"http://{self.ip}/ISAPI/System/deviceInfo", self.password)
        response = str(req.getapi())
        root = ET.ElementTree(ET.fromstring(response))
        name_text = None
        name_tag = root.find("ns:deviceName", self.namespace)
        if name_tag is not None:
            name_text = name_tag.text
        return name_text

    # GET device NTP
    def getntp(self):
        req = ISAPI(f"http://{self.ip}/ISAPI/System/time/ntpServers", self.password)
        response = str(req.getapi())
        root = ET.ElementTree(ET.fromstring(response)).getroot()
        server_text = None
        sync_text = None
        ntp_server = root.find("ns:NTPServer", self.namespace)
        if ntp_server is not None:
            server_tag = ntp_server.find("ns:hostName", self.namespace)
            sync_tag = ntp_server.find("ns:synchronizeInterval", self.namespace)
            if server_tag is not None:
                server_text = server_tag.text
            if sync_tag is not None:
                sync_text = sync_tag.text
        return {"server": server_text, "sync": sync_text}

    # GET device DST
    def getdst(self):
        req = ISAPI(f"http://{self.ip}/ISAPI/System/time", self.password)
        response = str(req.getapi())
        root = ET.ElementTree(ET.fromstring(response)).getroot()
        mode_text = None
        time_text = None
        mode_tag = root.find("ns:timeMode", self.namespace)
        time_tag = root.find("ns:timeZone", self.namespace)
        if mode_tag is not None:
            mode_text = mode_tag.text
        if time_tag is not None:
            time_text = time_tag.text
        return {"mode": mode_text, "timezone": time_text}

    # GET device Security authentication type
    def getsec(self):
        web_req = ISAPI(
            f"http://{self.ip}/ISAPI/Security/webCertificate", self.password
        )
        web_response = str(web_req.getapi())
        web_root = ET.ElementTree(ET.fromstring(web_response))
        web_text = None
        web_tag = web_root.find("ns:CertificateType", self.namespace)
        if web_tag is not None:
            web_text = web_tag.text

        rtsp_text = None
        if self.model == "DS-2CD2183G2-IU" or self.model == "DS-2CD1143G2-IUF":
            rtsp_req = ISAPI(
                f"http://{self.ip}/ISAPI/Streaming/channels/101", self.password
            )
            rtsp_response = str(rtsp_req.getapi())
            rtsp_root = ET.ElementTree(ET.fromstring(rtsp_response)).getroot()
            rtsp_tag = rtsp_root.find("ns:Transport", self.namespace)
            if rtsp_tag is not None:
                sec_tag = rtsp_tag.find("ns:Security", self.namespace)
                if sec_tag is not None:
                    cert_tag = sec_tag.find("ns:certificateType", self.namespace)
                    if cert_tag is not None:
                        rtsp_text = cert_tag.text

        elif self.model == "DS-7632NXI-K2":
            rtsp_req = ISAPI(
                f"http://{self.ip}/ISAPI/Security/RTSPCertificate", self.password
            )
            rtsp_response = str(rtsp_req.getapi())
            rtsp_root = ET.ElementTree(ET.fromstring(rtsp_response))
            rtsp_tag = rtsp_root.find("ns:certificateType", self.namespace)
            if rtsp_tag is not None:
                rtsp_text = rtsp_tag.text

        return {"web_sec": web_text, "rtsp_sec": rtsp_text}

    # GET device DNS Addresses
    def getdns(self):
        req = ISAPI(
            f"http://{self.ip}/ISAPI/System/Network/interfaces/1", self.password
        )
        response = str(req.getapi())
        root = ET.ElementTree(ET.fromstring(response)).getroot()
        primary_dns_text = None
        secondary_dns_text = None
        network_tag = root.find("ns:IPAddress", self.namespace)
        if network_tag is not None:
            primary_dns_tag = network_tag.find("ns:PrimaryDNS", self.namespace)
            if primary_dns_tag is not None:
                primary_ip = primary_dns_tag.find("ns:ipAddress", self.namespace)
                if primary_ip is not None:
                    primary_dns_text = primary_ip.text

            secondary_dns_tag = network_tag.find("ns:SecondaryDNS", self.namespace)
            if secondary_dns_tag is not None:
                secondary_ip = secondary_dns_tag.find("ns:ipAddress", self.namespace)
                if secondary_ip is not None:
                    secondary_dns_text = secondary_ip.text

        return {"primary": primary_dns_text, "secondary": secondary_dns_text}

    # GET device Mail
    def getmail(self):
        req = ISAPI("", self.password)
        name_text = None
        sender_text = None
        server_text = None
        port_text = None
        receiver_text = None
        email_text = None

        if self.model == "DS-2CD2183G2-IU" or self.model == "DS-2CD1143G2-IUF":
            req = ISAPI(
                f"http://{self.ip}/ISAPI/System/network/mailing/1", self.password
            )
            response = str(req.getapi())
            root = ET.ElementTree(ET.fromstring(response)).getroot()

            sender_tag = root.find("ns:sender", self.namespace)
            if sender_tag is not None:
                email_tag = sender_tag.find("ns:emailAddress", self.namespace)
                if email_tag is not None:
                    sender_text = email_tag.text

                name_tag = sender_tag.find("ns:name", self.namespace)
                if name_tag is not None:
                    name_text = name_tag.text

                smtp_tag = sender_tag.find("ns:smtp", self.namespace)
                if smtp_tag is not None:
                    server_tag = smtp_tag.find("ns:hostName", self.namespace)
                    if server_tag is not None:
                        server_text = server_tag.text

                    port_tag = smtp_tag.find("ns:portNo", self.namespace)
                    if port_tag is not None:
                        port_text = port_tag.text

            receiver_lst_tag = root.find("ns:receiverList", self.namespace)
            if receiver_lst_tag is not None:
                receiver_tag = receiver_lst_tag.find("ns:receiver", self.namespace)
                if receiver_tag is not None:
                    receiver_name_tag = receiver_tag.find("ns:name", self.namespace)
                    if receiver_name_tag is not None:
                        receiver_text = receiver_name_tag.text

                    receiver_email_tag = receiver_tag.find(
                        "ns:emailAddress", self.namespace
                    )
                    if receiver_email_tag is not None:
                        email_text = receiver_email_tag.text

        elif self.model == "DS-7632NXI-K2":
            req = ISAPI(f"http://{self.ip}/ISAPI/System/Network/mailing", self.password)
            response = str(req.getapi())
            root = ET.ElementTree(ET.fromstring(response)).getroot()

            mailing_ns = {"ns": "http://www.isapi.org/ver20/XMLSchema"}
            mailing_tag = root.find("ns:mailing", mailing_ns)
            if mailing_tag is not None:
                sender_tag = mailing_tag.find("ns:sender", mailing_ns)
                if sender_tag is not None:
                    email_tag = sender_tag.find("ns:emailAddress", mailing_ns)
                    if email_tag is not None:
                        sender_text = email_tag.text

                    name_tag = sender_tag.find("ns:name", mailing_ns)
                    if name_tag is not None:
                        name_text = name_tag.text

                    smtp_tag = sender_tag.find("ns:smtp", mailing_ns)
                    if smtp_tag is not None:
                        server_tag = smtp_tag.find("ns:hostName", mailing_ns)
                        if server_tag is not None:
                            server_text = server_tag.text

                        port_tag = smtp_tag.find("ns:portNo", mailing_ns)
                        if port_tag is not None:
                            port_text = port_tag.text

                receiver_lst_tag = mailing_tag.find("ns:receiverList", mailing_ns)
                if receiver_lst_tag is not None:
                    receiver_tag = receiver_lst_tag.find("ns:receiver", mailing_ns)
                    if receiver_tag is not None:
                        receiver_name_tag = receiver_tag.find("ns:name", mailing_ns)
                        if receiver_name_tag is not None:
                            receiver_text = receiver_name_tag.text

                        receiver_email_tag = receiver_tag.find(
                            "ns:emailAddress", mailing_ns
                        )
                        if receiver_email_tag is not None:
                            email_text = receiver_email_tag.text

        return {
            "name": name_text,
            "sender": sender_text,
            "server": server_text,
            "port": port_text,
            "receiver": receiver_text,
            "email": email_text,
        }

    # GET device Main-Stream
    def getmstream(self):
        req = ISAPI(f"http://{self.ip}/ISAPI/Streaming/channels/101", self.password)
        response = str(req.getapi())
        root = ET.ElementTree(ET.fromstring(response)).getroot()
        name_text = None
        encoding_text = None
        plus_text = None
        width_text = None
        height_text = None
        bitrate_text = None
        average_text = None
        fps_text = None

        # Channel Name
        name_tag = root.find("ns:channelName", self.namespace)
        if name_tag is not None:
            name_text = name_tag.text

        # Video
        video_tag = root.find("ns:Video", self.namespace)
        if video_tag is not None:
            # H265
            encoding_tag = video_tag.find("ns:videoCodecType", self.namespace)
            if encoding_tag is not None:
                encoding_text = encoding_tag.text
            # H265 +
            codec_tag = video_tag.find("ns:SmartCodec", self.namespace)
            if codec_tag is not None:
                plus_tag = codec_tag.find("ns:enabled", self.namespace)
                if plus_tag is not None:
                    plus_text = plus_tag.text

            # Width
            width_tag = video_tag.find("ns:videoResolutionWidth", self.namespace)
            if width_tag is not None:
                width_text = width_tag.text

            # Height
            height_tag = video_tag.find("ns:videoResolutionHeight", self.namespace)
            if height_tag is not None:
                height_text = height_tag.text

            # Bitrate Max.
            bitmax_tag = video_tag.find("ns:vbrUpperCap", self.namespace)
            if bitmax_tag is not None:
                bitrate_text = bitmax_tag.text

            # Bitrate Min.
            bitmin_tag = video_tag.find("ns:vbrAverageCap", self.namespace)
            if bitmin_tag is not None:
                average_text = bitmin_tag.text

            # FPS
            fps_tag = video_tag.find("ns:maxFrameRate", self.namespace)
            if fps_tag is not None:
                fps_text = fps_tag.text

        return {
            "name": name_text,
            "encoding": encoding_text,
            "plus": plus_text,
            "width": width_text,
            "height": height_text,
            "bitrate": bitrate_text,
            "average": average_text,
            "fps": fps_text,
        }

    # GET device Sub-Stream
    def getsstream(self):
        req = ISAPI(f"http://{self.ip}/ISAPI/Streaming/channels/102", self.password)
        response = str(req.getapi())
        root = ET.ElementTree(ET.fromstring(response)).getroot()
        name_text = None
        encoding_text = None
        width_text = None
        height_text = None
        bitrate_text = None
        fps_text = None

        # Channel Name
        name_tag = root.find("ns:channelName", self.namespace)
        if name_tag is not None:
            name_text = name_tag.text

        # Video
        video_tag = root.find("ns:Video", self.namespace)
        if video_tag is not None:
            # H265
            encoding_tag = video_tag.find("ns:videoCodecType", self.namespace)
            if encoding_tag is not None:
                encoding_text = encoding_tag.text

            # Width
            width_tag = video_tag.find("ns:videoResolutionWidth", self.namespace)
            if width_tag is not None:
                width_text = width_tag.text

            # Height
            height_tag = video_tag.find("ns:videoResolutionHeight", self.namespace)
            if height_tag is not None:
                height_text = height_tag.text

            # Bitrate Max.
            bitmax_tag = video_tag.find("ns:vbrUpperCap", self.namespace)
            if bitmax_tag is not None:
                bitrate_text = bitmax_tag.text

            # FPS
            fps_tag = video_tag.find("ns:maxFrameRate", self.namespace)
            if fps_tag is not None:
                fps_text = fps_tag.text

        return {
            "name": name_text,
            "encoding": encoding_text,
            "width": width_text,
            "height": height_text,
            "bitrate": bitrate_text,
            "fps": fps_text,
        }

    # GET OSD Name
    def getosd(self):
        req = ISAPI(
            f"http://{self.ip}/ISAPI/System/Video/inputs/channels/1", self.password
        )
        response = str(req.getapi())
        root = ET.ElementTree(ET.fromstring(response))
        name_text = None

        name_tag = root.find("ns:name", self.namespace)
        if name_tag is not None:
            name_text = name_tag.text

        return name_text

    # GET Overlay Configuration
    def getoverlay(self):
        req = ISAPI(
            f"http://{self.ip}/ISAPI/System/Video/inputs/channels/1/overlays",
            self.password,
        )
        response = str(req.getapi())
        root = ET.ElementTree(ET.fromstring(response)).getroot()
        week_text = None
        format_text = None

        # XML Root
        over_tag = root.find("ns:DateTimeOverlay", self.namespace)
        if over_tag is not None:
            # Date Format
            format_tag = over_tag.find("ns:dateStyle", self.namespace)
            if format_tag is not None:
                format_text = format_tag.text

            # Week
            week_tag = over_tag.find("ns:displayWeek", self.namespace)
            if week_tag is not None:
                week_text = week_tag.text

        return {"week": week_text, "format": format_text}

    # GET Motion Detection
    def getmotion(self):
        req = ISAPI(
            f"http://{self.ip}/ISAPI/System/Video/inputs/channels/1/motionDetection",
            self.password,
        )
        response = str(req.getapi())
        root = ET.ElementTree(ET.fromstring(response)).getroot()
        enabled_text = None
        grid_text = None
        sensitivity_text = None
        target_text = None

        # Motion Enabled
        enabled_tag = root.find("ns:enabled", self.namespace)
        if enabled_tag is not None:
            enabled_text = enabled_tag.text

        # Motion Options
        motion_tag = root.find("ns:MotionDetectionLayout", self.namespace)
        if motion_tag is not None:
            # Sensitivity
            sensitivity_tag = motion_tag.find("ns:sensitivityLevel", self.namespace)
            if sensitivity_tag is not None:
                sensitivity_text = sensitivity_tag.text

            # Target
            target_tag = motion_tag.find("ns:targetType", self.namespace)
            if target_tag is not None:
                target_text = target_tag.text

            # Grid Map
            layout_tag = motion_tag.find("ns:layout", self.namespace)
            if layout_tag is not None:
                grid_tag = layout_tag.find("ns:gridMap", self.namespace)
                if grid_tag is not None:
                    grid_text = grid_tag.text

        return {
            "enabled": enabled_text,
            "grid": grid_text,
            "sensitivity": sensitivity_text,
            "target": target_text,
        }

    # GET Recording
    def getrecord(self):
        req = ISAPI(f"http://{self.ip}/ISAPI/Event/triggers/VMD-1", self.password)
        response = str(req.getapi())
        root = ET.ElementTree(ET.fromstring(response)).getroot()
        target_text = None
        method_text = None

        list_tag = root.find("ns:EventTriggerNotificationList", self.namespace)
        if list_tag is not None:
            event_tag = list_tag.find("ns:EventTriggerNotification", self.namespace)
            if event_tag is not None:
                # ID Tag (Record Target)
                id_tag = event_tag.find("ns:id", self.namespace)
                if id_tag is not None:
                    target_text = id_tag.text

                # Method
                method_tag = event_tag.find("ns:notificationMethod", self.namespace)
                if method_tag is not None:
                    method_text = method_tag.text

        return {"target": target_text, "method": method_text}

    # GET SD Error Exception
    def getsderr(self):
        req = ISAPI(f"http://{self.ip}/ISAPI/Event/triggers/diskerror", self.password)
        response = str(req.getapi())
        root = ET.ElementTree(ET.fromstring(response)).getroot()
        method_text = None
        list_tag = root.find("ns:EventTriggerNotificationList", self.namespace)
        if list_tag is not None:
            event_tag = list_tag.find("ns:EventTriggerNotification", self.namespace)
            if event_tag is not None:
                # Method tag
                method_tag = event_tag.find("ns:notificationMethod", self.namespace)
                if method_tag is not None:
                    method_text = method_tag.text

        return method_text

    # GET Illegal Access Exception
    def getillaccess(self):
        req = ISAPI(f"http://{self.ip}/ISAPI/Event/triggers/illaccess", self.password)
        response = str(req.getapi())
        root = ET.ElementTree(ET.fromstring(response)).getroot()
        method_text = None
        list_tag = root.find("ns:EventTriggerNotificationList", self.namespace)
        if list_tag is not None:
            event_tag = list_tag.find("ns:EventTriggerNotification", self.namespace)
            if event_tag is not None:
                # Method tag
                method_tag = event_tag.find("ns:notificationMethod", self.namespace)
                if method_tag is not None:
                    method_text = method_tag.text

        return method_text

    # GET SD Quota
    def getquota(self):
        req = ISAPI(f"http://{self.ip}/ISAPI/ContentMgmt/Storage/quota", self.password)
        response = str(req.getapi())
        root = ET.ElementTree(ET.fromstring(response)).getroot()
        picture_text = None
        video_text = None

        quota_tag = root.find("ns:diskQuota", self.namespace)
        if quota_tag is not None:
            # Images quota ratio
            picture_tag = quota_tag.find("ns:pictureQuotaRatio", self.namespace)
            if picture_tag is not None:
                picture_text = picture_tag.text

            # Videos quota ratio
            video_tag = quota_tag.find("ns:videoQuotaRatio", self.namespace)
            if video_tag is not None:
                video_text = video_tag.text

        return {"picture": picture_text, "video": video_text}

    # GET SD Info
    def getsd(self):
        req = ISAPI(f"http://{self.ip}/ISAPI/ContentMgmt/Storage/hdd", self.password)
        response = str(req.getapi())
        root = ET.ElementTree(ET.fromstring(response)).getroot()
        # capacity_text = None
        state_text = None

        # Revisar esta variable. Puede cambiar según Firmware
        xml_namespace = None

        if self.model == "DS-2CD2183G2-IU":
            xml_namespace = {"ns": "http://www.hikvision.com/ver10/XMLSchema"}
        elif self.model == "DS-2CD1143G2-IUF":
            xml_namespace = self.namespace

        hdd_tag = root.find("ns:hdd", xml_namespace)
        if hdd_tag is not None:
            # Formating Status
            state_tag = hdd_tag.find("ns:status", xml_namespace)
            if state_tag is not None:
                state_text = state_tag.text

            # SD Capacity
            # capacity_tag = hdd_tag.find('ns:capacity', xml_namespace)
            # if capacity_tag is not None:
            #    capacity_text = capacity_tag.text

        return {"state": state_text}  #'capacity': capacity_text

    # GET Calendar
    def getcalendar(self):
        req = ISAPI(f"http://{self.ip}/ISAPI/ContentMgmt/record/tracks", self.password)
        response = str(req.getapi())
        root = ET.ElementTree(ET.fromstring(response)).getroot()

        enabled_text = None
        pre_text = None
        post_text = None
        over_text = None
        expiration_text = None
        duration_text = None
        day_list = []
        start_list = []
        end_list = []
        mode_list = []

        start_dict = zip(day_list, start_list)
        end_dict = zip(day_list, end_list)
        mode_dict = zip(day_list, mode_list)

        exp_flag = False
        custom_flag = False
        loop_flag = False

        for track_tag in root.findall(".//ns:Track", self.namespace):
            if not loop_flag:
                # Overwriting files
                loop_tag = track_tag.find("ns:LoopEnable", self.namespace)
                if loop_tag is not None:
                    over_text = loop_tag.text
                    loop_flag = True

            if not exp_flag:
                # 30 Days Deletion
                duration_tag = track_tag.find("ns:Duration", self.namespace)
                if duration_tag is not None:
                    duration_text = duration_tag.text
                # Enabled Deletion
                expiration_tag = track_tag.find("ns:durationEnabled", self.namespace)
                if expiration_tag is not None:
                    expiration_text = expiration_tag.text
                exp_flag = True

            if not custom_flag:
                # Schedule Enabled
                custom_ext_lst = track_tag.find(
                    "ns:CustomExtensionList", self.namespace
                )
                if custom_ext_lst is not None:
                    custom_ext = custom_ext_lst.find(
                        "ns:CustomExtension", self.namespace
                    )
                    if custom_ext is not None:
                        # Enabled Scheduler
                        enabled_tag = custom_ext.find(
                            "ns:enableSchedule", self.namespace
                        )
                        if enabled_tag is not None:
                            enabled_text = enabled_tag.text
                        # Pre-Record seconds
                        pre_tag = custom_ext.find(
                            "ns:PreRecordTimeSeconds", self.namespace
                        )
                        if pre_tag is not None:
                            pre_text = pre_tag.text
                        # Post-Record seconds
                        post_tag = custom_ext.find(
                            "ns:PostRecordTimeSeconds", self.namespace
                        )
                        if post_tag is not None:
                            post_text = post_tag.text
                        custom_flag = True

            # Track List
            track_sch_tag = track_tag.find("ns:TrackSchedule", self.namespace)
            if track_sch_tag is not None:
                block_list_tag = track_sch_tag.find(
                    "ns:ScheduleBlockList", self.namespace
                )
                if block_list_tag is not None:
                    block_tag = block_list_tag.find("ns:ScheduleBlock", self.namespace)
                    if block_tag is not None:
                        for sch_action_tag in block_tag.findall(
                            "ns:ScheduleAction", self.namespace
                        ):
                            # Start Time
                            start_tag = sch_action_tag.find(
                                "ns:ScheduleActionStartTime", self.namespace
                            )
                            if start_tag is not None:
                                # Start Day
                                day_tag = start_tag.find("ns:DayOfWeek", self.namespace)
                                if day_tag is not None:
                                    day_text = day_tag.text
                                    day_list.append(day_text)
                                # Start Hour
                                time_tag = start_tag.find(
                                    "ns:TimeOfDay", self.namespace
                                )
                                if time_tag is not None:
                                    start_text = time_tag.text
                                    start_list.append(start_text)

                            # End Time
                            end_tag = sch_action_tag.find(
                                "ns:ScheduleActionEndTime", self.namespace
                            )
                            if end_tag is not None:
                                time_tag = end_tag.find("ns:TimeOfDay", self.namespace)
                                if time_tag is not None:
                                    end_text = time_tag.text
                                    end_list.append(end_text)

                            # Action
                            action_tag = sch_action_tag.find(
                                "ns:Actions", self.namespace
                            )
                            if action_tag is not None:
                                mode_tag = action_tag.find(
                                    "ns:ActionRecordingMode", self.namespace
                                )
                                if mode_tag is not None:
                                    mode_text = mode_tag.text
                                    mode_list.append(mode_text)

        return {
            "enabled": enabled_text,
            "advanced": {
                "overwrite": over_text,
                "prerecord": pre_text,
                "postrecord": post_text,
                "expiration": expiration_text,
                "duration": duration_text,
            },
            "schedule": {
                "start": dict(start_dict),
                "end": dict(end_dict),
                "mode": dict(mode_dict),
            },
        }

    # GET device S/N
    def getsn(self):
        req = ISAPI(f"http://{self.ip}/ISAPI/System/deviceInfo", self.password)
        response = str(req.getapi())
        root = ET.ElementTree(ET.fromstring(response))
        sn_text = None
        sn_tag = root.find("ns:subSerialNumber", self.namespace)
        if sn_tag is not None:
            sn_text = sn_tag.text
        return sn_text

    # -------------------------------------------------------------------------
    # CONFIGURATIONS
    def putname(self, name):  # Modify camera name
        req = ISAPI(f"http://{self.ip}/ISAPI/System/deviceInfo", self.password)
        data = f"<deviceName>{name}</deviceName>"
        parameter = req.putapi(data)
        return parameter

    def putime(self):  # Configure "Time Settings"
        # NTP Configuration
        ntp_req = ISAPI(f"http://{self.ip}/ISAPI/System/time/ntpServers", self.password)
        with open(f"{self.directory}ntp.xml", "r") as f:
            ntp_xml = f.read()
            f.close()
        ntp_req.putapi(ntp_xml)

        # DST Configuration
        time_req = ISAPI(f"http://{self.ip}/ISAPI/System/time", self.password)
        with open(f"{self.directory}dst.xml", "r") as f:
            time_xml = f.read()
            f.close()
        time_req.putapi(time_xml)

        # Time request
        h_req = ISAPI(f"http://{self.ip}/ISAPI/System/time/localTime", self.password)
        return h_req.getapi()

    def putosd(self, name):  # Modifiy OSD
        # Change OSD name
        osd_req = ISAPI(
            f"http://{self.ip}/ISAPI/System/Video/inputs/channels/1", self.password
        )
        # osd_data = f'<name>{name}</deviceName>'

        osd_tree = ET.parse(f"{self.directory}osd.xml")
        osd_root = osd_tree.getroot()

        # Here we write the new named given to the function to a new XML file
        for osname in osd_root.iter(f"{self.xmlschema}name"):
            osname.text = f"{name}"
            osd_tree.write(f"{self.directory}osdcp.xml")

        # Now we call to a function that removes the namespace from the XML file
        self.remove_namespace(osd_root, osd_tree, self.xmlschema)
        osd_tree.write(f"{self.directory}osdcp.xml")

        # Save all the changes to the XML file before sending to the PUT request
        with open(f"{self.directory}osdcp.xml", "r") as f:
            osd_xml = f.read()
            f.close()
        osd_conf = osd_req.putapi(osd_xml)

        # Change overlay settings (Date Format and Hide Week)
        over_req = ISAPI(
            f"http://{self.ip}/ISAPI/System/Video/inputs/channels/1/overlays",
            self.password,
        )
        with open(f"{self.directory}overlay.xml", "r") as f:
            over_xml = f.read()
            f.close()
        over_conf = over_req.putapi(over_xml)
        return (osd_conf, over_conf)

    def putmail(self, name, sys_id):  # Modify mail configurations
        req = ISAPI(f"http://{self.ip}/ISAPI/System/network/mailing/1", self.password)

        tree = ET.parse(f"{self.directory}mail.xml")
        root = tree.getroot()

        for parent in root.iter(f"{self.xmlschema}sender"):
            for sender in parent.iter(f"{self.xmlschema}name"):
                sender.text = f"{name} {sys_id}"
                tree.write(f"{self.directory}mailcp.xml")

        self.remove_namespace(root, tree, self.xmlschema)
        tree.write(f"{self.directory}mailcp.xml")

        with open(f"{self.directory}mailcp.xml", "r") as f:
            data_xml = f.read()
            f.close()

        config = req.putapi(data_xml)
        return config

    def putsec(self):  # Configure "Security" settings
        websec_req = ISAPI(
            f"http://{self.ip}/ISAPI/Security/webCertificate", self.password
        )
        with open(f"{self.directory}security.xml", "r") as f:
            sec_xml = f.read()
            f.close()
        websec_conf = websec_req.putapi(sec_xml)

        rtspsec_req = ISAPI(
            f"http://{self.ip}/ISAPI/Streaming/channels/101", self.password
        )
        with open(f"{self.directory}rtspsec.xml", "r") as f:
            rtspsec_xml = f.read()
            f.close()
        rtsp_conf = rtspsec_req.putapi(rtspsec_xml)

        return (websec_conf, rtsp_conf)

    def putnet(self):  # DNS Configuration
        # Discovery Mode configuration
        discmode_req = ISAPI(
            f"http://{self.ip}/ISAPI/System/discoveryMode", self.password
        )
        with open(f"{self.directory}discovery.xml", "r") as f:
            discmode_xml = f.read()
            f.close()
        discmode_conf = discmode_req.putapi(discmode_xml)

        # Fill DNS fields
        dns_req = ISAPI(
            f"http://{self.ip}/ISAPI/System/Network/interfaces/1", self.password
        )
        dns_tree = ET.parse(f"{self.directory}dns.xml")
        dns_root = dns_tree.getroot()

        # Set the IP camera field with it's own IP
        for camip in dns_root.iter(f"{self.xmlschema}ipAddress"):
            camip.text = f"{self.ip}"
            dns_tree.write(f"{self.directory}dnscp.xml")

        self.remove_namespace(dns_root, dns_tree, self.xmlschema)
        dns_tree.write(f"{self.directory}dnscp.xml")

        # Parsing another time the new XML File
        dnscp_tree = ET.parse(f"{self.directory}dnscp.xml")
        dnscp_root = dnscp_tree.getroot()

        # Change the previous writings to correct the Gateway
        for parent1 in dnscp_root.iter("DefaultGateway"):
            for routip in parent1.iter("ipAddress"):
                routip.text = f"{self.gateway}"
                dnscp_tree.write(f"{self.directory}dnscp.xml")

        # Setting Primary DNS
        for parent2 in dnscp_root.iter("PrimaryDNS"):
            for mdns in parent2.iter("ipAddress"):
                mdns.text = "8.8.8.8"
                dnscp_tree.write(f"{self.directory}dnscp.xml")

        # Setting the secondary DNS
        for parent3 in dnscp_root.iter("SecondaryDNS"):
            for sdns in parent3.iter("ipAddress"):
                sdns.text = "8.8.4.4"
                dnscp_tree.write(f"{self.directory}dnscp.xml")

        with open(f"{self.directory}dnscp.xml", "r") as f:
            dns_xml = f.read()
            f.close()

        dns_conf = dns_req.putapi(dns_xml)

        return (discmode_conf, dns_conf)

    def putvideo(self, name):  # Configure video parameters
        # Configure Main-Stream video
        mainvid_req = ISAPI(
            f"http://{self.ip}/ISAPI/Streaming/channels/101", self.password
        )
        mainvid_tree = ET.parse(f"{self.directory}mstream.xml")
        mainvid_root = mainvid_tree.getroot()

        for mvid in mainvid_root.iter(f"{self.xmlschema}channelName"):
            mvid.text = f"{name}"
            mainvid_tree.write(f"{self.directory}mstreamcp.xml")

        self.remove_namespace(mainvid_root, mainvid_tree, self.xmlschema)
        mainvid_tree.write(f"{self.directory}mstreamcp.xml")

        with open(f"{self.directory}mstreamcp.xml", "r") as f:
            mainvid_xml = f.read()
            f.close()

        mainvid_conf = mainvid_req.putapi(mainvid_xml)

        # Configure Sub-Stream video
        subvid_req = ISAPI(
            f"http://{self.ip}/ISAPI/Streaming/channels/102", self.password
        )
        subvid_tree = ET.parse(f"{self.directory}sstream.xml")
        subvid_root = subvid_tree.getroot()

        for svid in subvid_root.iter(f"{self.xmlschema}channelName"):
            svid.text = f"{name}"
            subvid_tree.write(f"{self.directory}sstreamcp.xml")

        self.remove_namespace(subvid_root, subvid_tree, self.xmlschema)
        subvid_tree.write(f"{self.directory}sstreamcp.xml")

        with open(f"{self.directory}sstreamcp.xml", "r") as f:
            subvid_xml = f.read()
            f.close()

        subvid_conf = subvid_req.putapi(subvid_xml)

        return (mainvid_conf, subvid_conf)

    def putevents(self):  # Configure Motion Detection and Exceptions
        # Motion Detection
        motion_req = ISAPI(
            f"http://{self.ip}/ISAPI/System/Video/inputs/channels/1/motionDetection",
            self.password,
        )
        with open(f"{self.directory}motion.xml", "r") as f:
            motion_xml = f.read()
            f.close()
        motion_conf = motion_req.putapi(motion_xml)

        # Motion Recording Trigger
        trigger_req = ISAPI(
            f"http://{self.ip}/ISAPI/Event/triggers/VMD-1", self.password
        )
        with open(f"{self.directory}vmdtrigger.xml", "r") as f:
            trigger_xml = f.read()
            f.close()
        trigger_conf = trigger_req.putapi(trigger_xml)

        # HDD Error Exception
        hddexcep_req = ISAPI(
            f"http://{self.ip}/ISAPI/Event/triggers/diskerror", self.password
        )
        with open(f"{self.directory}disktrigger.xml", "r") as f:
            hddexcep_xml = f.read()
            f.close()
        hddexcep_conf = hddexcep_req.putapi(hddexcep_xml)

        # Ilegal Login Exception
        logexcep_req = ISAPI(
            f"http://{self.ip}/ISAPI/Event/triggers/illaccess", self.password
        )
        with open(f"{self.directory}illtrigger.xml", "r") as f:
            logexcep_xml = f.read()
            f.close()
        logexcep_conf = logexcep_req.putapi(logexcep_xml)

        # Motion Detection Schedule
        schedule_req = ISAPI(
            f"http://{self.ip}/ISAPI/Event/schedules/motionDetections/VMD_video1",
            self.password,
        )
        with open(f"{self.directory}schtrigger.xml", "r") as f:
            schedule_xml = f.read()
            f.close()
        schedule_conf = schedule_req.putapi(schedule_xml)

        return (motion_conf, trigger_conf, schedule_conf, hddexcep_conf, logexcep_conf)

    def putschedule(self):  # Configure recording calendar
        sch_req = ISAPI(
            f"http://{self.ip}/ISAPI/ContentMgmt/record/tracks", self.password
        )
        with open(f"{self.directory}calendar.xml", "r") as f:
            sch_xml = f.read()
            f.close()
        sch_conf = sch_req.putapi(sch_xml)

        return sch_conf

    def sd_formatter(self):  # Format camera SD card
        # Establish the image/video quota
        quota_req = ISAPI(
            f"http://{self.ip}/ISAPI/ContentMgmt/Storage/quota", self.password
        )
        with open(f"{self.directory}quota.xml", "r") as f:
            quota_xml = f.read()
            f.close()
        quota_conf = quota_req.putapi(quota_xml)

        # Format the card
        format_req = ISAPI(
            f'http://{self.ip}/ISAPI/ContentMgmt/Storage/hdd/1/format?formatType="EXT4"',
            self.password,
        )
        format_conf = format_req.putapi("")
        return (quota_conf, format_conf)

    def upfirmware(self):  # Firmware Updater
        # Check camera Firmware version
        req = ISAPI(f"http://{self.ip}/ISAPI/System/deviceInfo", self.password)
        req_get = req.getapi()
        root = ET.fromstring(req_get.text)

        for x in root.iter(f"{self.xmlschema}firmwareVersion"):
            version = x.text

        # Check local Firmware
        local_version_file = open(
            f"{self.act_dir}/firmwares/{self.model}/Version.txt", "r"
        )
        for ver in local_version_file.readlines():
            local_version_list = ver.split(".")

        cam_ver_str = version.replace("V", "")
        cam_ver_list = cam_ver_str.split(".")

        up_req = ISAPI(f"http://{self.ip}/ISAPI/System/updateFirmware", self.password)

        with open(f"{self.act_dir}/firmwares/{self.model}/digicap.dav", "rb") as f:
            firmware = f.read()
            f.close()

        if cam_ver_list[0] < local_version_list[0]:
            up_req.putapi(firmware)
            return "Actualizando..."
        elif cam_ver_list[0] > local_version_list[0]:
            return "NUEVO FIRMWARE!!!"
        elif cam_ver_list[0] == local_version_list[0]:
            if cam_ver_list[1] < local_version_list[1]:
                up_req.putapi(firmware)
                return "Actualizando..."
            elif cam_ver_list[1] > local_version_list[1]:
                return "NUEVO FIRMWARE!!!"
            elif cam_ver_list[1] == local_version_list[1]:
                if cam_ver_list[2] < local_version_list[2]:
                    up_req.putapi(firmware)
                    return "Actualizando..."
                elif cam_ver_list[2] > local_version_list[2]:
                    return "NUEVO FIRMWARE!!!"
                elif cam_ver_list[2] == local_version_list[2]:
                    return "FIRMWARE ACTUALIZADO"

    def reboot(self):  # Camera Reboot
        req = ISAPI(f"http://{self.ip}/ISAPI/System/reboot", self.password)
        reboot = req.putapi("")
        return reboot

    def configurate(self, name, sys_name):  # Execute all configurations
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
            return f"Configurada camara {name}"
        except Exception as e:
            return f"ERROR [{e}]"
