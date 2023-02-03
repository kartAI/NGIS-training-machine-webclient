import sys
import requests
from dotenv import load_dotenv
load_dotenv()
import os
import json 
import uuid
import transfer


from api import NgisOpenApi

def get_api():
    url = os.getenv('NGISAPI_URL')
    user = os.getenv('NGISAPI_USER')
    password = os.getenv('NGISAPI_PASS')
    return NgisOpenApi(url, user, password, "KartAITest")


def save_json(data, filename):
    file_path = "C:\\temp\\" + filename
    f = open(file_path, "w")
    f.write(json.dumps(data))
    f.close()
def main() -> int:
    api = get_api()

    dataset_id = '63cb2b40-1461-4a9a-90c1-446ef0ee42f4'

    '''
    print("Get datasets")
    print(api.get_datasets())
    '''

    '''
    print("Get dataset")
    print(api.get_dataset_info(dataset_id))
    '''

    
    print("Get features")
    bbox = "584080.3856561417,6638847.17958132,584237.6979578076,6639009.613057086"
    filename = str(uuid.uuid4()) + ".geojson"
    res = api.get_features(dataset_id, bbox, "Bygning")
    print(f'Got {len(res["features"])} features. Saving to {filename}')
    save_json(res, filename)
    
    transfer.transfer_geojson(filename)

    return 0

if __name__ == '__main__':
    sys.exit(main())