import os
import urllib.parse
import json
import requests
from datetime import datetime

def generate_wms_picture():
    # URL til WMS 
    base_url = "https://openwms.statkart.no/skwms1/wms.fkb"
    
    # Korrekt path til script
    current_script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Path for fasitfoto
    images_directory_path = os.path.join(current_script_directory, "Fasitfoto")
    
    # Sjekker om fasitfoto allerede eksisterer 
    os.makedirs(images_directory_path, exist_ok=True)

    # Leser koordinater fra JSON
    coordinates_file_path = os.path.join(current_script_directory, 'resources', 'coordinates.json')
    with open(coordinates_file_path) as file:
        data = json.load(file)
        coordinates = data['Coordinates']

    # Genererer BBOX data fra gitte koordinater i coordinates.json
    min_x = min(coord[0] for coord in coordinates)
    min_y = min(coord[1] for coord in coordinates)
    max_x = max(coord[0] for coord in coordinates)
    max_y = max(coord[1] for coord in coordinates)
    bbox = f'{min_x},{min_y},{max_x},{max_y}'

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

    # Spør som en input hvilket "Layers brukeren vil se"
    layer_names = input("Enter LAYERS (layer names, comma-separated if multiple, Current layers are: veg,bru,bygning): ")
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
    
    # Enkoder parametre inkl SLD body 
    encoded_params = urllib.parse.urlencode(wms_params, quote_via=urllib.parse.quote)

    # Bygger og printer URLen med de riktige definerte WMS parameterene
    full_url = f"{base_url}?{encoded_params}"
    print("Generated URL:")
    print(full_url)

    # Headers som lager en browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(full_url, headers=headers)

    if response.status_code == 200:
        # Genererer et filnavn basert på dato og tid bildet ble hentet på
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"output_{timestamp}.png"

        # Hele filen sin path
        image_path = os.path.join(images_directory_path, file_name)

        with open(image_path, 'wb') as file:
            file.write(response.content)
        print(f"Bilde ble lagret i {image_path}.")
    else:
        print(f"Kunne ikke lagre bilde, statuskode: {response.status_code}")

generate_wms_picture()
