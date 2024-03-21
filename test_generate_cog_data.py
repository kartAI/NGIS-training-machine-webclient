# test_generate_cog_data.py
import os
import unittest
from unittest.mock import patch, MagicMock, call
import numpy as np
import application.ortoCOG

class TestGenerateCogData(unittest.TestCase):

    @patch("application.ortoCOG.os.getenv")
    @patch("application.ortoCOG.load_dotenv")
    @patch("application.ortoCOG.util.read_file")
    @patch("application.ortoCOG.rasterio.open")
    @patch("application.ortoCOG.imageio.imwrite")
    @patch("application.ortoCOG.os.path.isdir")
    @patch("application.ortoCOG.os.makedirs")
    def test_generate_cog_data_success(self, mock_makedirs, mock_isdir, mock_imageio, mock_rasterio_open, mock_read_file, mock_load_dotenv, mock_getenv):
        # Setup mock return values for environment variables
        mock_getenv.side_effect = lambda key: {
            "AZURE_STORAGE_ACCESS_KEY": "fake_key", 
            "AZURE_STORAGE_ACCOUNT_NAME": "fake_account"
        }.get(key, None)
        mock_isdir.return_value = False

        # Setup mock return values for util.read_file to provide coordinates and config
        mock_read_file.side_effect = [
            {"Coordinates": [[0, 0], [10, 10]]},  # Mock coordinates to ensure it's not empty
            {"Config": {"tile_size": 256, "image_resolution": 0.2}}  # Mock config including image_resolution
        ]

        # Mock rasterio's open function behavior
        src_mock = MagicMock()
        # Mock 3-channel image data, assuming 256x256 image size for simplicity
        src_mock.read.return_value = np.random.rand(256, 256, 3)  
        mock_rasterio_open.return_value.__enter__.return_value = src_mock

        # Prepare file paths dictionary as would be passed in real function call
        file_paths = {
            "coordinates": "path/to/coordinates.json",
            "config": "path/to/config.json",
            "root": "/fake/root"
        }

        # Call the function under test
        result = generate_cog_data(file_paths)

        # Assertions to verify the expected behavior and function calls
        self.assertTrue(result)

        # Verifying that os.getenv was called with expected arguments
        mock_getenv.assert_has_calls([
            call('AZURE_STORAGE_ACCESS_KEY'),
            call('AZURE_STORAGE_ACCOUNT_NAME')
        ], any_order=True)

        # Verify that other mocked functions are called as expected
        mock_load_dotenv.assert_called_once()
        mock_read_file.assert_called()
        mock_rasterio_open.assert_called()
        mock_imageio.assert_called()
        mock_makedirs.assert_called_with(os.path.join(file_paths["root"], "tiles", "orto"), exist_ok=True)

if __name__ == "__main__":
    unittest.main()
