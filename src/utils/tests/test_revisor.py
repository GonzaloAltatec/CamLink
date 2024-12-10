import pytest
import json
from pathlib import Path
from ...routers.reviser import (
    device_access,
    device_calendar,
    device_mail,
    device_mstream,
    device_name,
    device_ntp,
    device_dst,
    device_overlay,
    device_quota,
    device_record,
    device_sderror,
    device_security,
    device_dns,
    device_sstream,
    device_motion,
    device_sd,
)


@pytest.fixture
def mocker_data():
    data = {
        "id": 53256,
        "name": "C1N1",
        "installation": "4585",
        "user": "admin",
        "password": "1234",
        "ip": "192.215.200.16",
        "port": 80,
        "model": "DS-2CD2183G2-IU",
    }

    return data


@pytest.fixture
def mock_device(mocker, mocker_data):
    return mocker.patch("src.routers.reviser.models.device", return_value=mocker_data)


@pytest.mark.asyncio
async def test_device(mocker, mock_device):
    conf_path = (
        Path("src") / "utils" / "configurations" / f"{mock_device()['model']}.json"
    )

    with open(conf_path, "r") as f:
        conf = json.load(f)

    mock_hik = mocker.patch("src.routers.reviser.Hik", autospec=True)
    instance = mock_hik.return_value

    # Mocked Name
    instance.getname.return_value = "C1N1"
    name_result = await device_name(mock_device())
    assert name_result == "Okey"
    instance.getname.assert_called_once()

    # Mocked NTP
    instance.getntp.return_value = {
        "server": conf["ntp"]["server"],
        "sync": conf["ntp"]["sync"],
    }
    ntp_result = await device_ntp(mock_device())
    assert ntp_result == "Okey"
    instance.getntp.assert_called_once()

    # Mocked DST
    instance.getdst.return_value = {
        "mode": conf["dst"]["mode"],
        "timezone": conf["dst"]["timezone"],
    }
    dst_result = await device_dst(mock_device())
    assert dst_result == "Okey"
    instance.getdst.assert_called_once()

    # Mocked Security
    instance.getsec.return_value = {
        "web_sec": conf["security"]["web"],
        "rtsp_sec": conf["security"]["rtsp"],
    }
    dst_result = await device_security(mock_device())
    assert dst_result == "Okey"
    instance.getsec.assert_called_once()

    # Mocked DNS
    instance.getdns.return_value = {
        "primary": conf["dns"]["primary"],
        "secondary": conf["dns"]["secondary"],
    }
    dst_result = await device_dns(mock_device())
    assert dst_result == "Okey"
    instance.getdns.assert_called_once()

    # Mocked Mail
    instance.getmail.return_value = {
        "name": f"{mock_device()['name']} {mock_device()['installation']}",
        "sender": conf["mail"]["sender"],
        "server": conf["mail"]["server"],
        "port": conf["mail"]["port"],
        "receiver": conf["mail"]["receiver"],
        "email": conf["mail"]["email"],
    }
    dst_result = await device_mail(mock_device())
    assert dst_result == "Okey"
    instance.getmail.assert_called_once()

    # Mocked Main-Stream
    instance.getmstream.return_value = {
        "name": mock_device()["name"],
        "encoding": conf["mstream"]["encoding"],
        "plus": conf["mstream"]["plus"],
        "width": conf["mstream"]["width"],
        "height": conf["mstream"]["height"],
        "bitrate": conf["mstream"]["bitrate"],
        "average": conf["mstream"]["average"],
        "fps": conf["mstream"]["fps"],
    }
    mstream_result = await device_mstream(mock_device())
    assert mstream_result == "Okey"
    instance.getmstream.assert_called_once()

    # Mocked Sub-Stream
    instance.getsstream.return_value = {
        "name": mock_device()["name"],
        "encoding": conf["sstream"]["encoding"],
        "width": conf["sstream"]["width"],
        "height": conf["sstream"]["height"],
        "bitrate": conf["sstream"]["bitrate"],
        "fps": conf["sstream"]["fps"],
    }
    sstream_result = await device_sstream(mock_device())
    assert sstream_result == "Okey"
    instance.getsstream.assert_called_once()

    # Mocked Overlays
    instance.getoverlay.return_value = {
        "week": conf["overlays"]["week"],
        "format": conf["overlays"]["format"],
    }
    overlay_result = await device_overlay(mock_device())
    assert overlay_result == "Okey"
    instance.getoverlay.assert_called_once()

    # Mocked Motion
    instance.getmotion.return_value = {
        "enabled": conf["motion"]["enabled"],
        "grid": conf["motion"]["grid"],
        "sensitivity": conf["motion"]["sensitivity"],
        "target": conf["motion"]["target"],
    }
    motion_result = await device_motion(mock_device())
    assert motion_result == "Okey"
    instance.getmotion.assert_called_once()

    # Mocked Motion
    instance.getrecord.return_value = {
        "target": conf["record"]["target"],
        "method": conf["record"]["method"],
    }
    record_result = await device_record(mock_device())
    assert record_result == "Okey"
    instance.getrecord.assert_called_once()

    # Mocked SD Error
    instance.getsderr.return_value = conf["exceptions"]["disk"]
    sderror_result = await device_sderror(mock_device())
    assert sderror_result == "Okey"
    instance.getsderr.assert_called_once()

    # Mocked Illegal Access
    instance.getillaccess.return_value = conf["exceptions"]["login"]
    access_result = await device_access(mock_device())
    assert access_result == "Okey"
    instance.getillaccess.assert_called_once()

    # Mocked SD Quota
    instance.getquota.return_value = {
        "picture": conf["quota"]["picture"],
        "video": conf["quota"]["video"],
    }
    quota_result = await device_quota(mock_device())
    assert quota_result == "Okey"
    instance.getquota.assert_called_once()

    # Mocked SD Info
    instance.getsd.return_value = {"state": conf["sd"]["state"]}
    sd_result = await device_sd(mock_device())
    assert sd_result == "Okey"
    instance.getsd.assert_called_once()

    # Mocked Calendar
    instance.getcalendar.return_value = {
        "enabled": conf["calendar"]["enabled"],
        "advanced": {
            "overwrite": conf["calendar"]["advanced"]["overwrite"],
            "prerecord": conf["calendar"]["advanced"]["prerecord"],
            "postrecord": conf["calendar"]["advanced"]["postrecord"],
            "expiration": conf["calendar"]["advanced"]["expiration"],
            "duration": conf["calendar"]["advanced"]["duration"],
        },
        "schedule": {
            "start": {
                "Monday": conf["calendar"]["schedule"]["Monday"]["start"],
                "Tuesday": conf["calendar"]["schedule"]["Tuesday"]["start"],
                "Wednesday": conf["calendar"]["schedule"]["Wednesday"]["start"],
                "Thursday": conf["calendar"]["schedule"]["Thursday"]["start"],
                "Friday": conf["calendar"]["schedule"]["Friday"]["start"],
                "Saturday": conf["calendar"]["schedule"]["Saturday"]["start"],
                "Sunday": conf["calendar"]["schedule"]["Sunday"]["start"],
            },
            "end": {
                "Monday": conf["calendar"]["schedule"]["Monday"]["end"],
                "Tuesday": conf["calendar"]["schedule"]["Tuesday"]["end"],
                "Wednesday": conf["calendar"]["schedule"]["Wednesday"]["end"],
                "Thursday": conf["calendar"]["schedule"]["Thursday"]["end"],
                "Friday": conf["calendar"]["schedule"]["Friday"]["end"],
                "Saturday": conf["calendar"]["schedule"]["Saturday"]["end"],
                "Sunday": conf["calendar"]["schedule"]["Sunday"]["end"],
            },
            "mode": {
                "Monday": conf["calendar"]["schedule"]["Monday"]["mode"],
                "Tuesday": conf["calendar"]["schedule"]["Tuesday"]["mode"],
                "Wednesday": conf["calendar"]["schedule"]["Wednesday"]["mode"],
                "Thursday": conf["calendar"]["schedule"]["Thursday"]["mode"],
                "Friday": conf["calendar"]["schedule"]["Friday"]["mode"],
                "Saturday": conf["calendar"]["schedule"]["Saturday"]["mode"],
                "Sunday": conf["calendar"]["schedule"]["Sunday"]["mode"],
            },
        },
    }
    calendar_result = await device_calendar(mock_device())
    assert calendar_result == "Okey"
    instance.getcalendar.assert_called_once()
