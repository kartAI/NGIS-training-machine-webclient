import unittest
import os
import shutil
from PIL import Image
import util
from util import write_file
from fastapi.exceptions import HTTPException
from unittest.mock import mock_open, patch
import json

#Test class for the utilities library
class TestUtil(unittest.TestCase):

    #Setup for testing
    def setUp(self):
        image = Image.new("RGB", (1024, 1024))
        image.save("image.png");
        os.mkdir("output")
        file = open("test.json", "a")
        file.write('{"Test Content": 1}')
        file.close()
    
    #Teardown after testing
    def tearDown(self):
        os.remove("image.png")
        shutil.rmtree("output")
        os.remove("test.json")

    #Test for the setup of WMS folders
    def test_setup_WMS_folders(self):
        util.setup_WMS_folders()

        #Assumes all folders are created by the function
        allCreated = True

        folders_to_check = [os.path.join("WMS", "email", "train", "images"),
        os.path.join("WMS", "email", "train", "masks"),
        os.path.join("WMS", "email", "val", "images"),
        os.path.join("WMS", "email", "val", "masks"),
        os.path.join("WMS", "rawphotos"),
        os.path.join("WMS", "tiles", "fasit"),
        os.path.join("WMS", "tiles", "orto")]
       
       #If a folder is not created by the function it will fail the test
        for folder in folders_to_check:
            if not os.path.exists(folder):
                allCreated = False
       
        self.assertEqual(allCreated, True)
        
        #Removes the temp folders created for the test 
        shutil.rmtree("WMS")

    #Test for the setup of WMS folders
    def test_setup_WMS_folders_if_folder_exists(self):
        #Creates a folder that will be created by the function
        os.makedirs(os.path.join("WMS", "email", "train", "images"))
        util.setup_WMS_folders()

        #Assumes all folders are created by the function
        allCreated = True

        folders_to_check = [os.path.join("WMS", "email", "train", "images"),
        os.path.join("WMS", "email", "train", "masks"),
        os.path.join("WMS", "email", "val", "images"),
        os.path.join("WMS", "email", "val", "masks"),
        os.path.join("WMS", "rawphotos"),
        os.path.join("WMS", "tiles", "fasit"),
        os.path.join("WMS", "tiles", "orto")]
       
       #If a folder is not created by the function it will fail the test
        for folder in folders_to_check:
            if not os.path.exists(folder):
                allCreated = False
       
        self.assertEqual(allCreated, True)
        
        #Removes the temp folders created for the test 
        shutil.rmtree("WMS")


    #Test for the teardown WMS folders function
    def test_teardown_WMS_folders(self):
        #Run the create function to create folders
        util.setup_WMS_folders()

        #Run the delete function
        util.teardown_WMS_folders()

        #Assumes all folders are deleted by the function
        allDeleted = True 

        folders_to_check = [os.path.join("WMS", "email"),
        os.path.join("WMS", "rawphotos"),
        os.path.join("WMS", "tiles")]

        #If a folder is not deleted by the function it will fail the test
        for folder in folders_to_check:
            if os.path.exists(folder):
                allDeleted = False
        
        self.assertEqual(allDeleted, True)

        shutil.rmtree("WMS")

    #Test for the readfile function
    def test_read_file(self):
        result = util.read_file("test.json")
        self.assertEqual(result, {'Test Content': 1})
    


    if __name__ == "main":
        unittest.main()

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