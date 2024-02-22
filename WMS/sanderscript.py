#Dette scriptet genererer treningsdata
import os
import urllib.parse
import json
import requests
from datetime import datetime
from WMS import util

def generate_wms_picture():

    # URL til WMS 
    base_url = "https://openwms.statkart.no/skwms1/wms.fkb"
    
    # Bruker riktig path til scriptet
    current_script_directory = os.path.dirname(os.path.abspath(__file__))

    # Leser koordinatene fra JSON-filen
    coordinates_file_path = os.path.join(current_script_directory, 'resources', 'coordinates.json')
    coordinates = util.read_file(coordinates_file_path)['Coordinates']

    # Beregner bbox fra koordinatene gitt i json fila
    bbox = util.create_bbox(coordinates)

    # Velger et sted å lagre bildene
    images_directory = "rawphotos"

    # Lagrer alt i mappen definert
    images_directory_path = os.path.join(current_script_directory, images_directory)

    # WMS parametere, de tomme feltene blir definert videre i koden
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

    layer_names = "bygning"
    wms_params['LAYERS'] = layer_names

    # Starter SLD body
    sld_body = '''
        <sld:StyledLayerDescriptor version="1.0.0" xmlns:sld="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd">
             '''
    
    # Genererer en "NamedLayer" blokk av kode for hvert layer
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
    
    # Lukker SLD bodyen
    sld_body += '</sld:StyledLayerDescriptor>'
    
    # Putter SLD stylingen inn i wms_params
    wms_params['sld_body'] = sld_body
    
    # Encode parameters, including SLD body
    encoded_params = urllib.parse.urlencode(wms_params, quote_via=urllib.parse.quote)

    # Bygger og printer URLen med de riktige definerte WMS parameterene
    full_url = f"{base_url}?{encoded_params}"

    # Headers som lager en browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(full_url, headers=headers)
    if response.status_code == 200:
        file_name = f"fasit.png"

    # Hele fil pathen
        image_path = os.path.join(images_directory_path, file_name)

        with open(image_path, 'wb') as file:
            file.write(response.content)
        print(f"Bildet ble lagret i {image_path}.")
        return True
    else:
        print(f"Kunne ikke lagre fasit-bilde, statuskode: {response.status_code}")
        print(f"Error in creating validation photo: {response.reason}" )
        return False
        