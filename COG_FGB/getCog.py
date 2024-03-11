import os
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions

# More imports inc...

from dotenv import load_dotenv

#Loads hidden values in script
current_script_directory = os.path.dirname(os.path.abspath(__file__))
env_file_path = os.path.join(current_script_directory, "..", "ngisopenapi", ".env")

load_dotenv(env_file_path) # Retrives hidden values

# Retrieves login information from azure web
account_name = 'cogurl'
account_key = os.getenv('AZURE_STORAGE_KEY')
container_name = 'cogurl2024'

#Client interaction with blob storage
connect_str = 'DefaultEndpointsProtocol=https;AccountName=' + account_name + ';AccountKey=' + account_key + ';EndpointSuffix=core.windows.net'
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

#Connect to blob storage
container_client = blob_service_client.get_container_client(container_name)

# SAS (shared access signature) connection for future