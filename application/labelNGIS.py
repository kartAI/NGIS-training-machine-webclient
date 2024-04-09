from dotenv import load_dotenv
import os
import re
import itertools
import sys  
import requests
from ngisopenapi.api import NgisOpenApi


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


def getNGIS():
    #Get the enviornment variables
    current_script_directory = os.path.dirname(os.path.abspath(__file__))
    temp_env = ".env"
    env_file_path = os.path.join(current_script_directory, "..", "application", ".env")

    #Loads environment variables from the right file
    load_dotenv(env_file_path)

    url=os.getenv("NGISAPI_URL")
    user=os.getenv("NGISAPI_USER")
    passs=os.getenv("NGISAPI_PASS")

    r = requests.get(f"{url}/datasets/", auth=(user, passs), headers={"X-Client-Product-Version":"KartAITest"})

    print(r.json())
    return r.json()

    api = get_api()
    print(api.url)
    print(api.user)
    print(api.password)
    print(api.get_datasets())
 
