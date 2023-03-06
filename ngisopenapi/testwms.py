import requests
from dotenv import load_dotenv
load_dotenv()
import os

wms_url = os.getenv("WMS_URL")
username = os.getenv("WMS_USER")
password = os.getenv("WMS_PASS")
bbox = "10.600884,59.901260,10.602922,59.902256"

params = {
    "service": "WMS",
    "version": "1.1.1",
    "request": "GetMap",
    "layers": "ortofoto",
    "styles": "",
    "format": "image/jpeg",
    "bbox": bbox,
    "width": 512,
    "height": 512,
    "srs": "EPSG:4326",
    "username": username,
    "password": password
}

response = requests.get(wms_url, params=params, stream=True)

if response.status_code == 200:
    with open("C:/Users/Sondre/Documents/Bachelor-geojson/image.jpg", "wb") as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)
    print("Image downloaded successfully.")
else:
    print("WMS connection failed with status code: {}".format(response.status_code))
