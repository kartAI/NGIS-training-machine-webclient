from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch
import pytest


#Import test client
client = TestClient(app)

#Test to test the update wms coordinate file function
def test_update_wms_coordinate_file():
    response = client.post(
        "/updateWMSCoordinateFile",
        headers = {'Content-Type': 'application/json'},
        json={"input": [1,2,4,4]}
    )

    #Check that the responses are okay
    assert response.status_code == 200
    assert response.json() == {"Message": "Coordinates were updated successfully"}


#Test to test the update wms config file function
def test_update_wms_config_file():
    response = client.post(
        "/updateWMSConfigFile",
        headers = {'Content-Type': 'application/json'},
        json={"data_parameters": [0.4, 0.4, 0.4], "layers": ["Bygning"], "colors": ["#000000"]}
    )

    #Check that the responses are okay
    assert response.status_code == 200
    assert response.json() == {"Message": "Config was updated successfully"}

# Zip test

@pytest.fixture
def mock_send_email_with_attachment():
    with patch("your_module.send_email_with_attachment") as mock:
        # You can set up the mock here if needed, e.g., mock.return_value = something
        yield mock

@pytest.fixture
def mock_zip_files():
    with patch("your_module.zip_files") as mock:
        # Mock any specifics of zip_files here, e.g., ensure it doesn't actually create a zip file
        yield mock

@pytest.fixture
def mock_os_remove():
    with patch("os.remove") as mock:
        # Prevent actual file deletion during tests
        yield mock

def test_send_zipped_files_email(mock_send_email_with_attachment, mock_zip_files, mock_os_remove):
    response = client.post("/send-email/")
    assert response.status_code == 200
    assert response.json() == {"message": "Email sent successfully with zipped files."}
    mock_send_email_with_attachment.assert_called_once()
    mock_zip_files.assert_called_once()
    mock_os_remove.assert_called_once_with("attachments.zip")




    
