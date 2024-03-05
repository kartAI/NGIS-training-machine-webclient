from typing import List
import requests
import os
import urllib.parse
import requests
from application import util
from dotenv import load_dotenv

def generate_training_data(file_paths):
    '''
    This function is used to generate a photo using Norkart's WMS with orthophoto capabilities. 
    Returns: 
    bool: True if generation of photos was successful, false otherwise
    '''

    #Finds the path to the enviornment file in the NGISopenAPI directory and the path to the coordinates file
    current_script_directory = os.path.dirname(os.path.abspath(__file__))
    env_file_path = os.path.join(current_script_directory, "..", "ngisopenapi", ".env")
    coordinates_file_path = file_paths["coordinates"]
    config_file_path = file_paths["config"]

    #Loads environment variables from the right file
    load_dotenv(env_file_path)

    #Reads the coordinates and config from the files
    coordinates = util.read_file(coordinates_file_path)['Coordinates']
    config = util.read_file(config_file_path)["Config"]

    #Directory where the image will be saved
    images_directory = "orto"
    images_directory_path = os.path.join(file_paths["root"], "tiles", images_directory)

    #Calculates the preferred image size for each call and the array of bboxes to be used to making the calls
    preferred_image_size = [config["tile_size"], config["tile_size"]]
    bboxes = util.create_bbox_array(coordinates, config)

    # Get the bounding boxes for each image
    i = 0
    amountToMake = len(bboxes)
    for bbox in bboxes:
        x0, y0, x1, y1 = bbox
        #Generate a url for each bounding box
        image_url = get_image_url([x0, y0, x1, y1], preferred_image_size)
        headers = {
         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

        #Uses the request library to make a request to the url
        response = requests.get(image_url, headers=headers)
        #Check if the response from the server was OK
        if response.status_code == 200:
            #Define the file name and path for the image
            file_name = f"tile_{i}.png"
            image_path = os.path.join(images_directory_path, file_name)
            
            #Save the image
            with open(image_path, 'wb') as file:
                file.write(response.content)
            print(f"Bildet ble lagret i {image_path}.")
            i += 1
            if(i == amountToMake):
                return True
        else:
            #If something went wrong, print the status code and explanation
            print(f"Kunne ikke lagre orto-bilde, statuskode: {response.status_code}")
            print(f"Error in creating orto photo: {response.reason}" )
            return False


def get_image_url(bbox: List[float], image_size: List[float]) -> str:
    """Returns a url for a map with the given layers and bounding box.

    Args:
        layers (list(str)): List of layers to include in the map.
        bbox (list(float)): List of coordinates for the bounding box. [minx, miny, maxx, maxy]

    Returns:
        str: Url for the map.
    """
    base_url = 'https://waapi.webatlas.no/wms-orto/'
    bbox_str = ",".join([str(x) for x in bbox])

        #Parameters for the WMS call
    wms_params = {
        "api_key": os.getenv('NK_WMS_API_KEY'),
        "request": "GetMap",
        "width" : image_size[1],
        "height": image_size[0],
        "layers": "ortofoto",
        "srs": "EPSG:25832",
        'format': 'image/png',  
        'bbox': bbox_str, 
    }

    encoded_params = urllib.parse.urlencode(wms_params, quote_via=urllib.parse.quote)
    full_url = f"{base_url}?{encoded_params}"

    return full_url

