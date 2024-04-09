from typing import List
import requests
import os
import urllib.parse
from application import util
from dotenv import load_dotenv
from pyproj import Transformer

# Function to fetch satellite images from Copernicus/Sentinel Hub WMS
def fetch_satellite_images(file_paths):
    '''
    Fetches satellite images from Copernicus WMS over Norway, reprojecting the coordinates to EPSG:25832.
    Returns:
    bool: True if the fetching of images was successful, false otherwise.
    '''
    # Find the path to the .env file and the coordinates and config files
    current_script_directory = os.path.dirname(os.path.abspath(__file__))
    env_file_path = os.path.join(current_script_directory, "..", "application", ".env")
    coordinates_file_path = file_paths["coordinates"]
    config_file_path = file_paths["config"]
    
    # Load the environment variables from the .env file
    load_dotenv(env_file_path)
    
    # Read the coordinates and config from the files
    coordinates = util.read_file(coordinates_file_path)['Coordinates']
    config = util.read_file(config_file_path)["Config"]
    print("Starting the process of fetching satellite images with coordinates: " + str(coordinates) + " and config settings: " + str(config))
    
    # Directory where the image will be saved
    images_directory = "satellite"
    images_directory_path = os.path.join(file_paths["root"], "tiles", images_directory)
    print("Satellite images will be saved to: " + images_directory_path)
    
    # Calculate the preferred image size for each call and the array of bboxes to be used to make the calls
    preferred_image_size = [config["tile_size"], config["tile_size"]]
    bboxes = util.create_bbox_array(coordinates, config)
    
    # Coordinate system transformer to reproject from EPSG:3857 to EPSG:25832
    transformer = Transformer.from_crs("EPSG:3857", "EPSG:25832", always_xy=True)
    
    i = 0
    for bbox in bboxes:
        # Reproject the coordinates from EPSG:3857 to EPSG:25832
        x0, y0 = transformer.transform(bbox[0], bbox[1])
        x1, y1 = transformer.transform(bbox[2], bbox[3])
        transformed_bbox = [x0, y0, x1, y1]
        
        image_url = get_image_url(transformed_bbox, preferred_image_size)
        
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(image_url, headers=headers)
        if response.status_code == 200:
            file_name = f"copernicus_tile_{i}.png"
            image_path = os.path.join(images_directory_path, file_name)
            with open(image_path, 'wb') as file:
                file.write(response.content)
            print(f"Copernicus tile_{i} was saved to {image_path}.")
            i += 1
        else:
            print(f"Could not save the image, status code: {response.status_code}")
            print(f"Error fetching Copernicus satellite image: {response.reason}")
            return False
            
    print("Fetched all satellite images and saved them to " + images_directory_path)
    return True

# Function to construct a URL to fetch a satellite image from Copernicus/Sentinel Hub WMS
def get_image_url(bbox: List[float], image_size: List[float]) -> str:
    """
    Constructs a URL to fetch an image from Copernicus WMS with the given bounding box and image size, 
    assuming the bbox is already in the correct CRS for the request.
    
    Args:
        bbox (List[float]): The coordinates for the bounding box in the CRS of the WMS service.
        image_size (List[float]): The desired size of the image [width, height].
    
    Returns:
        str: The constructed URL to fetch the image.
    """
    # Base URL for the Copernicus/Sentinel Hub WMS service
    base_url = 'https://services.sentinel-hub.com/ogc/wms/047a60db-cc17-4926-a898-d2ea54d3602e'
    bbox_str = ",".join([str(x) for x in bbox])
    
    # Parameters for the WMS request
    wms_params = {
        "request": "GetMap",
        "layers": "NATURAL-COLOR",
        "styles": "",
        "MAXCC": 20,
        "format": "image/jpeg",
        "transparent": "true",
        "version": "1.3.0",
        "crs": "EPSG:25832",
        "bbox": bbox_str,
        "width": str(image_size[0]),
        "height": str(image_size[1]),
        "service": "WMS",
    }
    
    # Encode the parameters and construct the full URL
    encoded_params = urllib.parse.urlencode(wms_params, quote_via=urllib.parse.quote)
    full_url = f"{base_url}?{encoded_params}"
    return full_url
