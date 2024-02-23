import unittest
import os
import shutil
from PIL import Image
from WMS import util


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

    #Tests the split_image method of util
    def test_split_image_functionality(self):
        result = util.split_image("image.png", "output", 512)
        self.assertEqual(result, 2)

     #Tests the split_image method of util
    def test_split_image_wrong_file(self):
        result = util.split_image("image.txt", "output", 512)
        self.assertEqual(result, "Filetype not supported")

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
