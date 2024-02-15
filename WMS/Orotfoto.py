import os
from dotenv import load_dotenv
import requests
from datetime import datetime

# Laster inn environment fra .env filen
load_dotenv()

# Laster API nøkkel
api_key = os.getenv("NK_WMS_API_KEY")

# Definerer WMS url
wms_url = 'https://waapi.webatlas.no/wms-orto/'

# Directory for lagrede bilder
images_directory = "ortofoto_images"

# Hele pathen til directory for bilder
images_directory_path = os.path.join(os.path.dirname(__file__), images_directory)

# Angi hvilke layers, bbox og hva enn du er interessert i
params = {
    'service': 'WMS',
    'request': 'GetMap',
    'layers': 'bygning, veg, bru',
    'bbox': '86862.34650433670322,6466039.970492540859,87579.68362640209671,6466748.95569468569',
    'width': '800',
    'height': '600',
    'srs': 'EPSG:25832',
    'format': 'image/png',  # Fil format
    'apikey': api_key  # Henter API nøkkel
}

# Oppretter en get request til WMS serveren gjennom url og api nøkkel
response = requests.get(wms_url, params=params)

if response.status_code == 200:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  # Legger til tid og dato filen ble opprettet på for å gjøre den unik
    file_name = f"output_{timestamp}.png"
    
    # Hele pathen til bildefilen
    image_path = os.path.join(images_directory_path, file_name)
    
    with open(image_path, 'wb') as file:
        file.write(response.content)
    print(f"Bildet ble lagret i {image_path}.") # Om det går feilfritt så blir denne kjørt
else:
    print(f"Kunne ikke lagre bilde, statuskode: {response.status_code}") # Error, 403 er access denied, annet så må man søke seg opp.
