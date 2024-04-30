import unittest
import os
import shutil
from PIL import Image
import util
from util import write_file, setup_user_session_folders, teardown_user_session_folders, split_files, read_file, create_bbox_array, create_bbox
from fastapi.exceptions import HTTPException
from unittest.mock import mock_open, patch
import json

class TestSplitFiles(unittest.TestCase):

    '''
    Test Class for the split files function in util
    '''

    def __init__(self, *args, **kwargs):
        self.test_session_id = 1
        self.files_to_make = 100
        self.trainingFraction = 50
        self.validationFraction = 50
        self.output_folder = os.path.join("datasets", f"dataset_{str(self.test_session_id)}", "email")
        self.image_folder = os.path.join("datasets", f"dataset_{self.test_session_id}", "tiles")
        super(TestSplitFiles, self).__init__(*args, **kwargs)

    def setUp(self):
        setup_user_session_folders(self.test_session_id)
        for i in range(self.files_to_make):
            f = open(os.path.join(self.image_folder, "orto", f"file_{i}.txt"), "x").close()
            f = open(os.path.join(self.image_folder, "fasit", f"file_{i}.txt"), "x").close()
   
    def tearDown(self):
        teardown_user_session_folders(self.test_session_id)

    def test_split_files_success(self):
        result = split_files(self.image_folder, self.output_folder, self.trainingFraction)
        self.assertEqual(result, True)
    
    def test_split_files_fail_wrong_input(self):
        result = split_files("", self.output_folder, self.trainingFraction)
        self.assertEqual(result, False)

    def test_split_files_wrong_output(self):
        result = split_files(self.image_folder, "", self.trainingFraction)
        self.assertEqual(result, False)
    

    if __name__ == "main":
        unittest.main()


class TestSetupUserFolders(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self.test_session_id = 1
        super(TestSetupUserFolders, self).__init__(*args, **kwargs)

    def tearDown(self):
        teardown_user_session_folders(self.test_session_id)

    def test_setup_success(self):
        result = setup_user_session_folders(self.test_session_id)
        self.assertEqual(result, True)
    

class TestReadFile(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self.data = {"key": "value"}
        self.filename = "file.json"
        super(TestReadFile, self).__init__(*args, **kwargs)

    def tearDown(self):
        os.remove(self.filename)

    def setUp(self):
        open(self.filename, "x").close()
        write_file(self.filename, self.data)

    def test_read_file_success(self):
        result = read_file(self.filename)
        self.assertEqual(result, self.data)

    def test_read_file_wrong_path(self):
        with self.assertRaises(HTTPException) as context:
            read_file(self.filename + ".txt")
        self.assertEqual(context.exception.status_code, 500)
        self.assertTrue(f"Could not find file: {str(self.filename)}" in str(context.exception.detail))



class TestBBOXArray(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.coordinateFile =  [[1000, 1000], [2000, 1000], [2000, 2000], [1000, 2000], [1000, 1000]]
        self.coordinateFile_notSquare =  [[1000, 1000], [2000, 1000], [2000, 2000], [1000, 1000]]
        self.config = {"label_source": "WMS", "orto_source": "WMS", "data_parameters": ["100", "0", "80"], "layers": ["Bygning", "Veg", "Bru"], "colors": ["#563d7c", "#563d7c", "#563d7c"], "tile_size": 500, "image_resolution": 0.2}
        super(TestBBOXArray, self).__init__(*args, **kwargs)

    def test_create_bbox_array(self):
        result = create_bbox_array(self.coordinateFile, self.config)
        self.assertEqual(len(result), 100)
    
    def test_create_bbox_array_polygon(self):
        result = create_bbox_array(self.coordinateFile_notSquare, self.config)
        self.assertEqual(len(result), 64)   

class TestSingleBBOX(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.coordinateFile =  [[1000, 1000], [2000, 1000], [2000, 2000], [1000, 2000], [1000, 1000]]
        self.config = {"label_source": "WMS", "orto_source": "WMS", "data_parameters": ["100", "0", "80"], "layers": ["Bygning", "Veg", "Bru"], "colors": ["#563d7c", "#563d7c", "#563d7c"], "tile_size": 500, "image_resolution": 0.2}
        super(TestSingleBBOX, self).__init__(*args, **kwargs)

    def test_create_bbox_success(self):
        result = create_bbox(self.coordinateFile)
        self.assertEqual(result["minx"], 1000)

        # Write file test 

class TestWriteFile(unittest.TestCase):
    @patch("util.open", new_callable=mock_open)
    @patch("util.json.dump")
    def test_write_file_success(self, mock_dump, mock_file):
        """Test successful JSON write to file."""
        data = {"key": "value"}
        file_path = "test.json"
        result = write_file(file_path, data)
        mock_file.assert_called_once_with(file_path, "w")
        mock_dump.assert_called_once_with(data, mock_file())
        self.assertEqual(result, 1)

    @patch("util.open", mock_open(), create=True)
    @patch("util.json.dump", side_effect=Exception("Mock exception"))
    def test_write_file_exception(self, mock_dump):
        """Test handling of exceptions during file write."""
        data = {"key": "value"}
        file_path = "test.json"
        with self.assertRaises(HTTPException) as context:
            write_file(file_path, data)
        self.assertEqual(context.exception.status_code, 500)
        self.assertTrue("Failed to write config to json file:" in str(context.exception.detail))

if __name__ == '__main__':
    unittest.main()