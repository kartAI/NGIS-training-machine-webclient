from fastapi.testclient import TestClient
from main import app
import unittest
from unittest.mock import patch, MagicMock, mock_open
import tempfile
import zipfile
from main import zip_files
from main import send_email
from pathlib import Path
import pytest
import os
from application import util
from main import zip_files
import numpy as np
from application.ortoCOG import generate_cog_data
from rasterio.transform import from_origin
from main import generateTrainingData
from dotenv import load_dotenv


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

    #Check that the responses are okay
    assert response.status_code == 200
    util.teardown_WMS_folders()
    cleanup_test_data()

def cleanup_test_data():
    pass

    # sendEmail test
from unittest.mock import patch
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
def temp_dir_with_files(tmp_path):
    # Create some test files in the temporary directory
    for i in range(3):
        file_path = tmp_path / f"test_file_{i}.txt"
        file_path.write_text(f"This is test file {i}")
    
    # Yield the temporary directory path to the test function
    yield tmp_path

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

  # Send email with attachment mock test

@patch('builtins.open', mock_open(read_data=b"data"))
@patch('os.path.exists', return_value=True)
@patch('main.SendGridAPIClient')
def test_send_email_with_attachment(mock_sendgrid_client, mock_exists):
    # Mock the os.path.exists to always return True
    mock_exists.return_value = True

    # Mock SendGridAPIClient's behavior
    mock_sendgrid_response = MagicMock()
    mock_sendgrid_response.status_code = 202  # SendGrid returns 202 for successful sends
    mock_sendgrid_client.return_value.send.return_value = mock_sendgrid_response

    # Parameters for send_email_with_attachment
    to_emails = "test@example.com"
    subject = "Test Subject"
    content = "Test Content"
    attachment_path = "path/to/test_attachment.zip"

    # Call the function to be tested
    send_email_with_attachment(to_emails, subject, content, attachment_path)

    # Assert: Check that os.path.exists was called with the attachment path
    mock_exists.assert_called_once_with(attachment_path)

    # Verify SendGridAPIClient was instantiated with the dummy API key
    mock_sendgrid_client.assert_called_once()

    # Verify the send method was called on the SendGrid client
    assert mock_sendgrid_client.return_value.send.called
    
    ''' COG TEST'''
    
class TestGenerateCogData(unittest.TestCase):
    @patch('application.ortoCOG.os.getenv')
    @patch('application.ortoCOG.load_dotenv')
    @patch('application.ortoCOG.util.read_file')
    @patch('application.ortoCOG.util.create_bbox_array')
    @patch('application.ortoCOG.rasterio.open')
    @patch('application.ortoCOG.imageio.imwrite')
    @patch('application.ortoCOG.plt.imsave')
    @patch('application.ortoCOG.os.path.isdir')
    @patch('application.ortoCOG.os.makedirs')
    def test_generate_cog_data_success(self, mock_makedirs, mock_isdir, mock_plt_imsave, mock_imageio, mock_rasterio_open, mock_create_bbox_array, mock_read_file, mock_load_dotenv, mock_getenv):
        mock_getenv.side_effect = lambda key: {
            'AZURE_STORAGE_ACCESS_KEY': 'fake_key',
            'AZURE_STORAGE_ACCOUNT_NAME': 'fake_account'
        }.get(key, None)
        mock_isdir.return_value = False
        mock_read_file.side_effect = [
            {'Coordinates': [[0, 0], [10, 10]]},
            {'Config': {'tile_size': 256, 'image_resolution': 0.2}} #Mock coord and config files
        ]
        mock_create_bbox_array.return_value = [[0, 0, 10, 10]]  #Simplified bounding box

        src_mock = MagicMock()
        src_mock.read.return_value = np.ones((256, 256, 3)) * 0.5
        mock_rasterio_open.return_value.__enter__.return_value = src_mock
        src_mock.transform = from_origin(0, 0, 1, 1)

        file_paths = {
            'coordinates': 'path/to/coordinates.json',
            'config': 'path/to/config.json',
            'root': '/fake/root'
        }

        result = generate_cog_data(file_paths)

        self.assertTrue(result)
        mock_imageio.assert_called()

if __name__ == '__main__':
    unittest.main()
    

load_dotenv()

@pytest.mark.parametrize("label_return_values, expected", [
    ((True, True), True),
    ((True, False), False),
    ((False, True), False),
    ((False, False), False)
])
def test_generate_training_data_wms_label(label_return_values, expected):
    paths = {
        "coordinates": "dummy_coordinate_path.json",
        "config": "dummy_config_path.json",
    }
    label_source = "WMS"
    orto_source = "None" 

    with patch('application.labelPhotoWMS.generate_label_data', return_value=label_return_values[0]), \
         patch('application.labelPhotoWMS.generate_label_data_colorized', return_value=label_return_values[1]):
        assert generateTrainingData(paths, label_source, orto_source) == expected

@pytest.mark.parametrize("label_return_values, expected", [
    ((True, True), True),
    ((True, False), False),
    ((False, True), False),
    ((False, False), False)
])

def test_generate_training_data_wms_label(label_return_values, expected):
    paths = {
        "coordinates": "dummy_coordinate_path.json",
        "config": "dummy_config_path.json",
    }
    label_source = "WMS"
    orto_source = "None"  # Assuming orto_source does not affect the outcome here

    with patch('application.labelPhotoWMS.generate_label_data', return_value=label_return_values[0]), \
         patch('application.labelPhotoWMS.generate_label_data_colorized', return_value=label_return_values[1]):
        assert generateTrainingData(paths, label_source, orto_source) == expected

@pytest.mark.parametrize("return_value, expected", [
    (True, True),
    (False, False)
])
def test_generate_training_data_fgb_label(return_value, expected):
    paths = {
        "coordinates": "dummy_coordinate_path.json",
        "config": "dummy_config_path.json",
    }
    label_source = "FGB"
    orto_source = "None"  # No orto source interaction in this test

    with patch('application.labelFGB.generate_label_data', return_value=return_value):
        assert generateTrainingData(paths, label_source, orto_source) == expected
        
@pytest.mark.parametrize("return_value, expected", [
    (True, True),
    (False, False)
])
def test_generate_training_data_wms_orto(return_value, expected):
    paths = {
        "coordinates": "dummy_coordinate_path.json",
        "config": "dummy_config_path.json",
    }
    label_source = "None"  # No label source interaction in this test
    orto_source = "WMS"

    with patch('application.ortoPhotoWMS.generate_training_data', return_value=return_value):
        assert generateTrainingData(paths, label_source, orto_source) == expected

@pytest.mark.parametrize("return_value, expected", [
    (True, True),
    (False, False)
])
def test_generate_training_data_cog_orto(return_value, expected):
    paths = {
        "coordinates": "dummy_coordinate_path.json",
        "config": "dummy_config_path.json",
    }
    label_source = "None"  # No label source interaction in this test
    orto_source = "COG"

    with patch('application.ortoCOG.generate_cog_data', return_value=return_value):
        assert generateTrainingData(paths, label_source, orto_source) == expected

@pytest.mark.parametrize("return_value, expected", [
    (True, True),
    (False, False)
])
def test_generate_training_data_sat_orto(return_value, expected):
    paths = {
        "coordinates": "dummy_coordinate_path.json",
        "config": "dummy_config_path.json",
        "root": "dummy_root_directory"  
    }
    label_source = "None"
    orto_source = "SAT"

    with patch('application.satWMS.fetch_satellite_images', return_value=return_value):
        result = generateTrainingData(paths, label_source, orto_source)
        assert result == expected, f"Expected {expected}, got {result}"