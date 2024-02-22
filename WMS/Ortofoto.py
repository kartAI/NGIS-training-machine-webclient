import os
import requests
from datetime import datetime
import urllib.parse
from dotenv import load_dotenv
import json
from WMS import util

def generate_orto_picture():
    # Finner path til .env filen som ligger i ngisopenapi mappen
    current_script_directory = os.path.dirname(os.path.abspath(__file__))
    env_file_path = os.path.join(current_script_directory, "..", "ngisopenapi", ".env")
    coordinates_file_path = os.path.join(current_script_directory, 'resources', 'coordinates.json')
    
    # Laster .env fra riktig path
    load_dotenv(env_file_path)

    # Henter API nøkkelen fra .env
    api_key = os.getenv('NK_WMS_API_KEY')

    # Definerer WMS url
    wms_url = 'https://waapi.webatlas.no/wms-orto/'

    # Leser inn koordinatene fra JSON-filen
    coordinates = util.read_file(coordinates_file_path)['Coordinates']

    # Beregner bbox fra koordinatene gitt i applikasjonen
    bbox = util.create_bbox(coordinates)

    # Setter directory for lagring av bilde
    images_directory = "rawphotos"

    # Lager hele pathen i samme mappe
    images_directory_path = os.path.join(current_script_directory, images_directory)

    # Angi hvilke layers, bbox og hva enn du er interessert i
    params = {
        "api_key": api_key,
        "request": "GetMap",
        "width" : "1600",
        "height": "1600",
        "layers": "ortofoto",
        "srs": "EPSG:25832",
        'format': 'image/png',  # Fil format
        'bbox': bbox,  # Oppdaterer bbox med de nye verdiene
    }

    encoded_params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)

    # Build and print the full URL
    full_url = f"{wms_url}?{encoded_params}"

    # Headers som legger en browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    # Oppretter en get request til WMS serveren gjennom url og api nøkkel
    response = requests.get(full_url, headers=headers)  # Ensure the request is made to `full_url`
    if response.status_code == 200:
        file_name = f"orto.png"
        
        # Hele fil pathen
        image_path = os.path.join(images_directory_path, file_name)

        with open(image_path, 'wb') as file:
            file.write(response.content)
        print(f"Bildet ble lagret i {image_path}.")
        return 1
    else:
        print(f"Kunne ikke lagre bilde, statuskode: {response.status_code}")
        print(f"Error: {response.reason}" )
        return 0
