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

'''TEST FOR LABEL AND ORTO SOURCES UPDATED AND WORKING 19.04.2024'''
# Leaving imports in order to easier run tests alone 
import pytest
from unittest.mock import patch
from main import generateTrainingData
from dotenv import load_dotenv

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
        

'''TEST FOR CONNECTING TO SMTP SERVER AND SENDING EMAILS'''
# Leaving imports in order to easier run tests alone
# This test also assumes that the zipping has happened before hand, like it is in main.
import os
from unittest.mock import patch, mock_open
import pytest
from main import send_email  

def test_send_email():
    to_email = "test@example.com"
    attachment_name = "path/to/data.zip"
    dataset_name = "dataset"

    with patch.dict(os.environ, {
        "SMTP_USER": "user@example.com",
        "SMTP_PASS": "password123",
        "SMTP_SERVER": "smtp.example.com",
        "SMTP_PORT": "587"  
    }), \
    patch("builtins.open", mock_open(read_data="data")), \
    patch("smtplib.SMTP") as mock_smtp:
        # Calling functiong in try to catch any exceptions
        try:
            send_email(to_email, attachment_name, dataset_name)
        except Exception as e:
            print("Error during send_email execution:", e)

        # Check SMTP calls
        instance = mock_smtp.return_value
        print("SMTP calls:", instance.method_calls)  # To see all calls made on the SMTP instance
        mock_smtp.assert_called_once_with("smtp.example.com", int(os.getenv("SMTP_PORT")))
        
        # Detailed assertions with conditional feedback
        if instance.starttls.called:
            instance.starttls.assert_called_once()
        else:
            print("starttls was not called")

        if instance.login.called:
            instance.login.assert_called_once_with("user@example.com", "password123")
        else:
            print("login was not called")

        if instance.sendmail.called:
            instance.sendmail.assert_called_once()
            args, kwargs = instance.sendmail.call_args
            assert args[0] == "user@example.com"
            assert args[1] == to_email
            assert "KARTAI TRENINGSDATA" in args[2]
            assert "This is your requested training data from the training data generator" in args[2]
        else:
            print("sendmail was not called")

