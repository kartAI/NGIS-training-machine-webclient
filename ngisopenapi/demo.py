import json
from api import NgisOpenApi
from shapely.geometry import Polygon, MultiPoint
from tran_api import convert_bbox_3857_to_5972
import transfer
import uuid
import os
import sys
import requests
from dotenv import load_dotenv
load_dotenv()

# Get the necessary connections for the api using dotenv


def get_api():
    try:
        url = os.getenv('NGISAPI_URL')
        user = os.getenv('NGISAPI_USER')
        password = os.getenv('NGISAPI_PASS')
        return NgisOpenApi(url, user, password, "KartAITest")
    except Exception as e:
        print(f"Error getting API: {e}")
        sys.exit(1)

# Function for saving a json file


def save_json(data, filename):
    try:
        file_path = os.getenv('f_path') + filename
        with open(file_path, "w") as f:
            f.write(json.dumps(data))
    except Exception as e:
        print(f"Error saving JSON file: {e}")
        sys.exit(1)
# Main function for running the demo script


def main() -> int:
    api = get_api()

    # Dataset id for the dataset used in NGIS Open-API
    dataset_id = '63cb2b40-1461-4a9a-90c1-446ef0ee42f4'

    # Get the directory of the current file
    file_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the parent directory of the file directory
    parent_dir = os.path.dirname(file_dir)

    # Define the path to the region file
    region_file = os.path.join(
        parent_dir, "kartAI", "training_data", "regions", "small_building_region.json")

    # Block of code for extracting coordinates from kartAI
    try:
        with open(region_file) as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: The specified file could not be found in:", region_file)
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Failed to decode the file as JSON.")
        sys.exit(1)
    except Exception as e:
        print("An unexpected error occurred:", e)
        sys.exit(1)

    coordinates = [(point[0], point[1]) for point in data['coordinates'][0]]
    polygon = Polygon(coordinates)
    # Converts the polygon from kartAI to a bounding box
    try:
        bbox = polygon.bounds
    except Exception as e:
        print("Error in converting polygon to bounding box.", e)
        sys.exit(1)
    # Converts the epsg of the coordinates
    try:
        converted_bbox = convert_bbox_3857_to_5972(bbox)
    except Exception as e:
        print("Error in converting epsg of bounding box coordinates.", e)
        sys.exit(1)
    # Adjustments to the format of the list of coordinates
    NGIS_bbox = ",".join(str(coord) for coord in converted_bbox)

    # Gives the file a random name to avoid duplication and defines it as geojson
    filename = str(uuid.uuid4()) + ".geojson"

    # Calls the api.get_features method to get the features from the NGIS Open-API.
    print("Get features")
    try:
        res = api.get_features(dataset_id, NGIS_bbox, "Bygning")
        print(f'Got {len(res["features"])} features. Saving to {filename}')
    except Exception as e:
        print("Error in gathering features:", e)
        sys.exit(1)

    # Saves the features from NGIS to a geojson file
    save_json(res, filename)

    # Uses the transfer_geojson function to insert the features to the PostgreSQL database
    transfer.transfer_geojson(filename)

    return 0


if __name__ == '__main__':
    sys.exit(main())
