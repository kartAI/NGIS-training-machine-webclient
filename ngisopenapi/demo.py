import sys
import requests
from dotenv import load_dotenv
load_dotenv()
import os
import json 
import uuid
import transfer
from tran_api import convert_bbox_3857_to_5972
from shapely.geometry import Polygon, MultiPoint
from api import NgisOpenApi

#Get the necessary connections for the api using dotenv
def get_api():
    url = os.getenv('NGISAPI_URL')
    user = os.getenv('NGISAPI_USER')
    password = os.getenv('NGISAPI_PASS')
    return NgisOpenApi(url, user, password, "KartAITest")

#Function for saving a json file
def save_json(data, filename):
    file_path = os.getenv('f_path') + filename
    f = open(file_path, "w")
    f.write(json.dumps(data))
    f.close()

#Main function for running the demo script
def main() -> int:
    api = get_api()

    #Dataset id for the dataset used in NGIS
    dataset_id = '63cb2b40-1461-4a9a-90c1-446ef0ee42f4'
    
    print("Get features")

    #Block of code for extracting coordinates from kartAI
    with open('..\\kartAI\\training_data\\regions\\small_building_region.json') as f:
        data = json.load(f)
    coordinates = [(point[0], point[1]) for point in data['coordinates'][0]]
    polygon = Polygon(coordinates)
    #Converts the polygon from kartAI to a bounding box
    bbox = polygon.bounds
    #Converts the epsg of the coordinates
    converted_bbox = convert_bbox_3857_to_5972(bbox)
    #Adjustments to the format of the list of coordinates
    NGIS_bbox = ",".join(str(coord) for coord in converted_bbox)
    print(NGIS_bbox)
    
    #Gives the file a random name to avoid duplication and defines it as geojson
    filename = str(uuid.uuid4()) + ".geojson"
    
    #Calls the api.get_features method to get the features from the NGIS API.
    res = api.get_features(dataset_id, NGIS_bbox, "Bygning")
    print(f'Got {len(res["features"])} features. Saving to {filename}')
    
    #Saves the features from NGIS to a geojson file
    save_json(res, filename)
    
    #Uses the transfer_geojson function to insert the features to the PostgreSQL databse
    transfer.transfer_geojson(filename)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())