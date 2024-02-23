import os
import requests
import urllib.parse
from dotenv import load_dotenv
from WMS import util

def generate_orto_picture():
    '''
    This function is used to generate a photo using Norkart's WMS with orthophoto capabilities. 
    Returns: 
    True (Bool) if the image was generated
    False (Bool) otherwise
    '''

    #Defines the URL for the WMS to be used
    wms_url = 'https://waapi.webatlas.no/wms-orto/'

    #Finds the path to the enviornment file in the NGISopenAPI directory and the path to the coordinates file
    current_script_directory = os.path.dirname(os.path.abspath(__file__))
    env_file_path = os.path.join(current_script_directory, "..", "ngisopenapi", ".env")
    coordinates_file_path = os.path.join(current_script_directory, 'resources', 'coordinates.json')
    
    #Loads environment variables from the right file
    load_dotenv(env_file_path)

    #Reads the coordinates from the coordinates-JSON file
    coordinates = util.read_file(coordinates_file_path)['Coordinates']

    #Calculates a bbox based on the coordinates
    bbox = util.create_bbox(coordinates)

    #Directory where the image will be saved
    images_directory = "rawphotos"
    images_directory_path = os.path.join(current_script_directory, images_directory)

    #Parameters for the WMS call
    params = {
        "api_key": os.getenv('NK_WMS_API_KEY'),
        "request": "GetMap",
        "width" : "1600",
        "height": "1600",
        "layers": "ortofoto",
        "srs": "EPSG:25832",
        'format': 'image/png',  
        'bbox': bbox, 
    }

    # Build the full URL with the parameters and headers
    encoded_params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    full_url = f"{wms_url}?{encoded_params}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    #Uses the request library to make a request to the url
    response = requests.get(full_url, headers=headers)  # Ensure the request is made to `full_url`
    
    #Check if the response from the server was OK
    if response.status_code == 200:
        #Define the file name and path for the image
        file_name = f"orto.png"
        image_path = os.path.join(images_directory_path, file_name)
       
        #Save the image
        with open(image_path, 'wb') as file:
            file.write(response.content)
        print(f"Bildet ble lagret i {image_path}.")
        return True
    else:
        #If something went wrong, print the status code and explanation
        print(f"Kunne ikke lagre ortofoto-bilde, statuskode: {response.status_code}")
        print(f"Error in creating ortophoto: {response.reason}" )
        return False
