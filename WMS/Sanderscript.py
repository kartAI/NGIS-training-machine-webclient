#Dette scriptet genererer treningsdata
import os
import urllib.parse
import requests
from WMS import util

def generate_wms_picture():
    '''
    This function is used to generate a photo using a WMS. 
    Returns: 
    True (Bool) if the image was generated
    False (Bool) otherwise
    '''

    #Defines the URL for the WMS to be used
    base_url = "https://openwms.statkart.no/skwms1/wms.fkb"
    
    #Finds the path to the coordinates file
    current_script_directory = os.path.dirname(os.path.abspath(__file__))
    coordinates_file_path = os.path.join(current_script_directory, 'resources', 'coordinates.json')

    #Reads the coordinates from the coordinates-JSON file
    coordinates = util.read_file(coordinates_file_path)['Coordinates']

    #Calculates a bbox based on the coordinates
    bbox = util.create_bbox(coordinates)

      #Directory where the image will be saved
    images_directory = "rawphotos"
    images_directory_path = os.path.join(current_script_directory, images_directory)

    #Parameters for the WMS call
    wms_params = {
        'SERVICE': 'WMS',
        'VERSION': '1.3.0',
        'REQUEST': 'GetMap',
        'BBOX': bbox,
        'CRS': 'EPSG:25832',
        'WIDTH': '1600',
        'HEIGHT': '1600',
        'LAYERS': '',
        'STYLES': '',
        'FORMAT': 'image/png',
        'DPI': '96',
        'MAP_RESOLUTION': '96',
        'FORMAT_OPTIONS': 'dpi:96',
        'TRANSPARENT': 'false',
        'sld_body': ''
    }

    #Layers to be put in the request url
    layer_names = "bygning"
    wms_params['LAYERS'] = layer_names

    sld_body = '''
        <sld:StyledLayerDescriptor version="1.0.0" xmlns:sld="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd">
             '''
    
    #Generates a new SLD layer for each layer defined above
    for layer_name in layer_names.split(','):
        sld_body += f'''
    <sld:NamedLayer>
        <sld:Name>{layer_name.strip()}</sld:Name>
        <sld:UserStyle>
            <sld:FeatureTypeStyle>
                <sld:Rule>
                    <sld:MinScaleDenominator>0</sld:MinScaleDenominator>
                    <sld:MaxScaleDenominator>999999999</sld:MaxScaleDenominator>
                    <PolygonSymbolizer>
                        <Fill>
                            <CssParameter name="fill">#000000</CssParameter>
                        </Fill>
                    </PolygonSymbolizer>
                </sld:Rule>
            </sld:FeatureTypeStyle>
        </sld:UserStyle>
    </sld:NamedLayer>
'''

    sld_body += '</sld:StyledLayerDescriptor>'
    
    #Adds the sld parameters to the wms parameters
    wms_params['sld_body'] = sld_body
    
    #Build the full URL with the parameters and headers
    encoded_params = urllib.parse.urlencode(wms_params, quote_via=urllib.parse.quote)
    full_url = f"{base_url}?{encoded_params}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    #Uses the request library to make a request to the url
    response = requests.get(full_url, headers=headers)

    #Check if the response from the server was OK
    if response.status_code == 200:
        #Define the file name and path for the image
        file_name = f"fasit.png"
        image_path = os.path.join(images_directory_path, file_name)
        
        #Save the image
        with open(image_path, 'wb') as file:
            file.write(response.content)
        print(f"Bildet ble lagret i {image_path}.")
        return True
    else:
        #If something went wrong, print the status code and explanation
        print(f"Kunne ikke lagre fasit-bilde, statuskode: {response.status_code}")
        print(f"Error in creating validation photo: {response.reason}" )
        return False
        