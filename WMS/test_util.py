import unittest
import os
import shutil
from PIL import Image
import util


#Test class for the utilities library
class TestUtil(unittest.TestCase):

    #Setup for testing
    def setUp(self):
        image = Image.new("RGB", (1024, 1024))
        image.save("image.png");
        os.mkdir("output")
    
    #Teardown after testing
    def tearDown(self):
        os.remove("image.png")
        shutil.rmtree("output")

    #Tests the split_image method of util
    def test_split_image_functionality(self):
        a = util.split_image("image.png", "output", 512)
        self.assertEquals(a, 4)

     #Tests the split_image method of util
    def test_split_image_wrong_file(self):
        a = util.split_image("image.txt", "output", 512)
        self.assertEquals(a, "Filetype not supported")
    


    if __name__ == "main":
        unittest.main()
