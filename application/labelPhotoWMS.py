from typing import List
import requests
import os
import urllib.parse
import requests
from application import util

def generate_label_data(file_paths):
    '''
    This function is used to generate label photos for machine learning
    Args:
    file_paths (dict): The file paths to the user session folders
    Returns: 
    bool: True if generation of photos was successful, false otherwise
    '''

    # Finds the path to the coordinates file
    coordinates_file_path = file_paths["coordinates"]
    config_file_path = file_paths["config"]

    # Reads the coordinates from the coordinates-JSON file
    coordinates = util.read_file(coordinates_file_path)['Coordinates']
    config = util.read_file(config_file_path)["Config"]
    print("Starting the process of generating label photos with coordinates: " + str(coordinates) + " and config settings: " + str(config))

    # Directory where the image will be saved
    images_directory = "fasit"
    images_directory_path = os.path.join(file_paths["root"], "tiles", images_directory)

    print("Images will be saved to: " + str(images_directory_path))

    # Calculates the preferred image size for each call and the array of bboxes to be used to making the calls
    preferred_image_size = [config["tile_size"], config["tile_size"]]
    bboxes = util.create_bbox_array(coordinates, config)

    # Get the bounding boxes for each image
    i = 0
    amountToMake = len(bboxes)
    for bbox in bboxes:
        x0, y0, x1, y1 = bbox
        # Generate a url for each bounding box
        label_url = get_label_url(config["layers"],["#000000", "#000000", "#000000"], [x0, y0, x1, y1], preferred_image_size)
        headers = {
         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

        # Uses the request library to make a request to the url
        response = requests.get(label_url, headers=headers)
        # Check if the response from the server was OK
        if response.status_code == 200:
            # Define the file name and path for the image
            file_name = f"tile_{i}.tif"
            image_path = os.path.join(images_directory_path, file_name)
            
            # Save the image
            with open(image_path, 'wb') as file:
                file.write(response.content)
            print(f"Image tile_{i} was saved to {image_path}.")
            i += 1
            if(i == amountToMake):
                print("Generated all the label images and saved them to " + images_directory_path)
                return True
        else:
            # If something went wrong, print the status code and explanation
            print(f"Could not save the image, statuscode: {response.status_code}")
            print(f"Error in creating validation photo: {response.reason}" )
            return False
        
def generate_label_data_colorized(file_paths):
    '''
    This function is used to generate label photos for machine learning.

    Args:
    - file_paths (dict): A dictionary containing the file paths for the coordinates and config files.

    Returns: 
    - bool: True if generation of photos was successful, false otherwise
    '''
    
    # Finds the path to the coordinates file
    current_script_directory = os.path.dirname(os.path.abspath(__file__))
    coordinates_file_path = file_paths["coordinates"]
    config_file_path = file_paths["config"]

    # Reads the coordinates from the coordinates-JSON file
    coordinates = util.read_file(coordinates_file_path)['Coordinates']
    config = util.read_file(config_file_path)["Config"]
    print("Starting the process of generating label photos with coordinates: " + str(coordinates) + " and config settings: " + str(config))

    # Directory where the image will be saved
    images_directory = "colorized"
    images_directory_path = os.path.join(file_paths["root"], "email", images_directory)
    print("Images will be saved to: " + str(images_directory_path))

    # Calculates the preferred image size for each call and the array of bboxes to be used to making the calls
    preferred_image_size = [config["tile_size"], config["tile_size"]] # The size of the image, retrieved from config.json
    bboxes = util.create_bbox_array(coordinates, config) # The bounding boxes for the images, retrieved from coordinates.json

    # Get the bounding boxes for each image and generate the colorized label images
    i = 0
    amountToMake = len(bboxes)
    for bbox in bboxes:
        x0, y0, x1, y1 = bbox
        # Generate a url for each bounding box
        label_url = get_label_url(config["layers"],config["colors"], [x0, y0, x1, y1], preferred_image_size)
        headers = {
         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

        # Uses the request library to make a request to the url
        response = requests.get(label_url, headers=headers)
        # Check if the response from the server was OK
        if response.status_code == 200:
            # Define the file name and path for the image
            file_name = f"colorized_tile_{i}.png"
            image_path = os.path.join(images_directory_path, file_name)
            
            # Save the image
            with open(image_path, 'wb') as file:
                file.write(response.content)
            print(f"Image tile_{i} was saved to {image_path}.")
            i += 1
            if(i == amountToMake):
                print("Generated all the label images (Colorized) and saved them to " + images_directory_path)
                return True
        else:
            # If something went wrong, print the status code and explanation
            print(f"Could not save the image, statuscode: {response.status_code}")
            print(f"Error in creating validation photo: {response.reason}" )
            return False
        

# Generate a URL for the WMS request
def get_label_url(layers: List[str],colors: List[str],  bbox: List[float], image_size: List[float]) -> str:
    """Returns a url for a map with the given layers and bounding box.

    Args:
        layers (list(str)): List of layers to include in the map.
        bbox (list(float)): List of coordinates for the bounding box. [minx, miny, maxx, maxy]

    Returns:
        str: Url for the map.
    """
    base_url = "https://openwms.statkart.no/skwms1/wms.fkb"
    bbox_str = ",".join([str(x) for x in bbox])
    layers_str = ",".join(layers)
    sld_layers = generate_SLD_layers(layers, colors)

    # WMS Parameters
    wms_params = {
        'SERVICE': 'WMS',
        'VERSION': '1.3.0',
        'REQUEST': 'GetMap',
        'BBOX': bbox_str,
        'CRS': 'EPSG:25832',
        'WIDTH': image_size[1],
        'HEIGHT': image_size[0],
        'LAYERS': layers_str,
        'STYLES': '',
        'FORMAT': 'image/png',
        'DPI': '96',
        'MAP_RESOLUTION': '96',
        'FORMAT_OPTIONS': 'dpi:96',
        'TRANSPARENT': 'false',
        'sld_body': sld_layers
    }


    # Encode the parameters and add them to the base url
    encoded_params = urllib.parse.urlencode(wms_params, quote_via=urllib.parse.quote)
    full_url = f"{base_url}?{encoded_params}"
    # print(full_url)
    return full_url

# Generate SLD layers for the WMS request
def generate_SLD_layers(layers: List[str], colors: List[str]):
    sld_body = '''
<sld:StyledLayerDescriptor version="1.0.0" xmlns:sld="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd">
'''
    
    # Generate a NamedLayer block for each layer
    for i in range(len(layers)):
        sld_body += f'''
    <sld:NamedLayer>
        <sld:Name>{layers[i].strip()}</sld:Name>
        <sld:UserStyle>
            <sld:FeatureTypeStyle>
                <sld:Rule>
                    <sld:MinScaleDenominator>0</sld:MinScaleDenominator>
                    <sld:MaxScaleDenominator>999999999</sld:MaxScaleDenominator>
                    <PolygonSymbolizer>
                        <Fill>
                            <CssParameter name="fill">{colors[i].strip()}</CssParameter>
                        </Fill>
                    </PolygonSymbolizer>
                </sld:Rule>
            </sld:FeatureTypeStyle>
        </sld:UserStyle>
    </sld:NamedLayer>
'''
    
    # Close the SLD body
    sld_body += '</sld:StyledLayerDescriptor>'
    return sld_body