import pytest
from unittest.mock import MagicMock
from ...utils.db.models import device

def test_device_okey(mocker):
    mock_odoo = mocker.patch('src.utils.db.models.Odoo', autospec=True)
    instance = mock_odoo.return_value
    instance.element_ids.return_value = [53256, 53407]
    instance.element_data.return_value = [
        {"name": "NOMBRE", "valor": "C1N1"},
        {"name": "USUARIO", "valor": "admin"},
        {"name": "PASSWORD", "valor": "1234"},
        {"name": "DIRECCION IP", "valor": "192.215.200.16"},
        {"name": "PUERTO HTTP", "valor": "80"},
        {"name": "product_id", "valor": "CVCCV"}
    ]
    instance.element_sys.return_value = '4585'

    mock_hik = mocker.patch('src.utils.db.models.Hik', autospec=True)
    hik_instance = mock_hik.return_value
    hik_instance.getmodel.return_value = 'DS-2CD2183G2-IU'

    result = device(id=53256)

    expected = {
        'id': 53256,
        'name': 'C1N1',
        'installation': '4585',
        'user': 'admin',
        'password': '1234',
        'ip': '192.215.200.16',
        'port': 80,
        'model': 'DS-2CD2183G2-IU'
    }

    assert result == expected
    instance.element_data.assert_called_with(53256)
    instance.element_sys.assert_called_once()
    hik_instance.getmodel.assert_called_once()

def test_device_model_not_found(mocker):
    # Mockear Odoo con datos válidos
    mock_odoo = mocker.patch("src.utils.db.models.Odoo", autospec=True)
    instance = mock_odoo.return_value
    instance.element_ids.return_value = [53407]
    instance.element_data.return_value = [
        {"name": "product_id", "valor": "CVCCV"},
        {"name": "DIRECCION IP", "valor": "192.215.2000.1"},
        {"name": "PASSWORD", "valor": "1234"}
    ]

    # Mockear Hik para devolver None
    mock_hik = mocker.patch("src.utils.db.models.Hik", autospec=True)
    hik_instance = mock_hik.return_value
    hik_instance.getmodel.return_value = None

    # Probar que se lanza una excepción HTTP
    with pytest.raises(Exception) as exc_info:
        device(id=53407)
    assert "Device model not found" in str(exc_info.value)
