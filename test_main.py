from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, MagicMock
import tempfile
import zipfile
from pathlib import Path
import pytest
import os
from WMS import util
from main import zip_files

#Import test client
client = TestClient(app)

#Test to test the update wms coordinate file function
def test_update_wms_coordinate_file():
    response = client.post(
        "/updateWMSCoordinateFile",
        headers = {'Content-Type': 'application/json'},
        json={"input": [[590520.940446737, 6642297.41275084], [590447.7385157445, 6645291.231015151], [595512.1041708611, 6645418.546416945], [595589.4060306272, 6642424.79659557], [590520.940446737, 6642297.41275084]]}
    )

    #Check that the responses are okay
    assert response.status_code == 200
    assert response.json() == {"Message": "Coordinates were updated successfully"}


#Test to test the update wms config file function
def test_update_wms_config_file():
    response = client.post(
        "/updateWMSConfigFile",
        headers = {'Content-Type': 'application/json'},
        json={"data_parameters": [0.4, 0.6, 1], "layers": ["Bygning"], "colors": ["#000000"]}
    )

    #Check that the responses are okay
    assert response.status_code == 200
    assert response.json() == {"Message": "Config was updated successfully"}

#Test to test the generate photos function
def test_generatePhotos():
    response = client.post("/generatePhotos")
    assert response.headers["content-type"] == "application/json"
    assert len(response.content) > 0 

   # with open("NGIS-training-machine-webclient/WMS/rawphotos", "wb") as f:
    #    f.write(response.content)

    #Check that the responses are okay
    assert response.status_code == 200
    util.teardown_WMS_folders()
    cleanup_test_data()

def cleanup_test_data():
    pass

    # sendEmail test

@patch('main.send_email_with_attachment')
@patch('main.zip_files')
@patch('os.remove')
@patch('main.util.teardown_WMS_folders')
def test_send_zipped_files_email(mock_teardown, mock_remove, mock_zip, mock_send_email):
    # Mock the behavior of external dependencies
    mock_zip.return_value = None
    mock_send_email.return_value = None
    mock_remove.return_value = None
    mock_teardown.return_value = None

    # Simulate a request with a JSON payload containing the email
    response = client.post("/sendEmail", json={"email": "test@example.com"})

    # Assertions to verify the endpoint behavior
    assert response.status_code == 200
    assert response.json() == {"message": "Email sent successfully with zipped files."}

    # Verify that the mocked functions were called as expected
    mock_zip.assert_called_once_with()  # Add any arguments if your function requires them
    mock_send_email.assert_called_once_with(
        to_emails="test@example.com",
        subject="Here are your zipped files",
        content="<strong>Zip file holding the requested data.</strong>",
        attachment_path="attachments.zip"
    )
    mock_remove.assert_called_once_with("attachments.zip")
    mock_teardown.assert_called_once()

# Test for /zip_files

@pytest.fixture
def temp_dir_with_files():
    # Create a temporary directory using pytest's built-in tmp_path fixture
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create some test files in the temporary directory
        for i in range(3):
            with open(Path(tmpdir) / f"test_file_{i}.txt", "w") as f:
                f.write(f"This is test file {i}")
        # Yield the temporary directory path to the test function
        yield tmpdir

def test_zip_files(temp_dir_with_files):
    # The temporary directory and files are setup
    tmpdir = temp_dir_with_files

    # The name of the zip file to be created
    zip_name = os.path.join(tmpdir, 'test.zip')

    # Call the function to be tested
    zip_files(directory_path=tmpdir, zip_name=zip_name)

    # Assert: Check the zip file exists
    assert os.path.exists(zip_name)

    # Verify the zip file contains the expected files
    with zipfile.ZipFile(zip_name, 'r') as zipf:
        zipped_files = zipf.namelist()
        expected_files = [f"test_file_{i}.txt" for i in range(3)]

        # Verify all expected files are in the zipped file
        for expected_file in expected_files:
            assert expected_file in zipped_files