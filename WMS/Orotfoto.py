import os
import requests
from datetime import datetime
import urllib.parse
from dotenv import load_dotenv

# Finner path til .env filen som ligger i ngisopenapi mappen
current_script_directory = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_script_directory, '..', 'ngisopenapi'))
env_file_path = os.path.join(project_root, '.env')

# Laster .env fra riktig path
load_dotenv(env_file_path)

# Henter API nøkkelen fra .env
api_key = os.getenv('NK_WMS_API_KEY')

# Definerer WMS url
wms_url = 'https://waapi.webatlas.no/wms-orto/'

# Setter directory for lagring av bilde
images_directory = "ortofoto_images"

# Lager hele pathen i samme mappe
images_directory_path = os.path.join(os.path.dirname(__file__), images_directory)

# Sjekker om filen eksisterer
os.makedirs(images_directory_path, exist_ok=True)

# Angi hvilke layers, bbox og hva enn du er interessert i
params = {
    "api_key": api_key,
    "request": "GetMap",
    "width" : "1600",
    "height": "1600",
    "layers": "ortofoto",
    "srs": "EPSG:25832",
    'format': 'image/png',  # Fil format
    'bbox': '751773.690167,7456391.139281,751983.690167,7456601.139281',
}

encoded_params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)

# Build and print the full URL
full_url = f"{wms_url}?{encoded_params}"
print("Generated URL:")
print(full_url)

# Headers som legger en browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Oppretter en get request til WMS serveren gjennom url og api nøkkel
response = requests.get(full_url, headers=headers)  # Ensure the request is made to `full_url`

if response.status_code == 200:
    # Genererer et filnavn basert på dato og tid bildet ble hentet på
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"output_{timestamp}.png"
    
    # Hele fil pathen
    image_path = os.path.join(images_directory_path, file_name)
    
    with open(image_path, 'wb') as file:
        file.write(response.content)
    print(f"Bildet ble lagret i {image_path}.")
else:
    print(f"Kunne ikke lagre bilde, statuskode: {response.status_code}")
