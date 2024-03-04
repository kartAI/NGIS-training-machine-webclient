import os
import json
import subprocess
import shutil
import smtplib
import ssl
import zipfile
from zipfile import ZipFile
import base64
import sendgrid
import asyncio
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Response
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from deleteFolder import delete_all_folders
from WMS import util
from WMS import ortoPhotoWMS
from WMS import labelPhotoWMS
from pydantic import BaseModel
from fastapi import HTTPException, FastAPI, Response, Depends
from uuid import UUID, uuid4
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.session_verifier import SessionVerifier
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
import random
import time
import uuid
from fastapi.responses import FileResponse



# Class for the FastAPI. Will contain all our methods for updating values and starting scripts


class Input(BaseModel):
    input: list
    

class ConfigInput(BaseModel):
    data_parameters: list
    layers: list
    colors: list
    tile_size: int
    image_resolution: float

# Import and create instance of the FastAPI framework
app = FastAPI()

# Adds and sets permissions for middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


'''
 SESSION MANAGEMENT SYSTEM
'''
@app.post("/setCookie")
def set_session_cookie(response: Response, session_id: str = None): # Sets session ID in cookie
    if session_id is None:
        session_id = str(random.randint(0, 1000000000000000))
    response.set_cookie(key="session_id", value=session_id,httponly=True, samesite='Lax') # httponly=True is done for security reasons, unaccessable to javascript.
    return {"Session_id": session_id}

def get_session_id(request: Request): # Returns session ID
    return request.cookies.get("session_id", None)

@app.post("/cookies")
def read_main(request: Request, response: Response):
    session_id = get_session_id(request)  # Corrected function call
    print(session_id)
    if not session_id:
        set_session_cookie(response)
        return {"message": True}
    return {"message": False}

# Paths to the relevant files and directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REGION_FILE = os.path.join(
    BASE_DIR, "kartAI", "training_data", "regions", "small_building_region.json")
CONFIG_FILE = os.path.join(
    BASE_DIR, "kartAI", "config", "dataset", "kartai.json")


# Code block for updating test/validation/building


@app.post("/update_training")
async def update_training(input: list):
    if len(input) != 3:
        return {"status": "error", "message": "input must have exactly 3 elements"}

    with open(CONFIG_FILE, "r") as file:
        data = json.load(file)
    

# Ensure that the "ProjectArguments" key exists in the JSON object
    if "ProjectArguments" not in data:
        data["ProjectArguments"] = {}

    # Updates training and validation with the first variables in the input list
    data["ProjectArguments"]["training_fraction"] = int(input[0])
    data["ProjectArguments"]["validation_fraction"] = int(input[1])

    # Update the ImageSets part of the JSON with the third value in the input list
    data["ImageSets"][1]["rules"] = [
        {
            "type": "PixelValueAreaFraction",
            "values": [1],
            "more_than": float(input[2])/100
        }
    ]

    with open(CONFIG_FILE, "w") as file:
        json.dump(data, file)

    return {"status": "success"}

# Code block for updating


@app.post("/update_coord.js")
async def update_coordinates(coords: Input):
    coordinates = coords.input
    with open(REGION_FILE, "r") as file:
        data = json.load(file)
    data["coordinates"] = [coordinates]
    with open(REGION_FILE, "w") as file:
        json.dump(data, file)
    return {"status": "success"}

# Deletes the folders locally after email is sent


@app.post("/delete_folders")
async def delete_folders():
    delete_all_folders()
    return {"message": "Deletion of folders successful."}



@app.post("/update_coordinates")
async def update_coordinates(input: list):
    with open(REGION_FILE, "r") as file:
        data = json.load(file)
    data["coordinates"] = [input]
    with open(REGION_FILE, "w") as file:
        json.dump(data, file)
    return {"status": "success"}

# Mount the different directories for static files
static_dirs = ["frontend", "frontend/resources", "frontend/scripts"]
for dir_name in static_dirs:
    app.mount(f"/{dir_name}", StaticFiles(directory=dir_name), name=dir_name)

templates = Jinja2Templates(directory="frontend/pages")


@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/{page}.html", response_class=HTMLResponse)
async def read_page(request: Request, page: str):
    return templates.TemplateResponse(f"{page}.html", {"request": request})


@app.get("/favicon.ico")
async def favicon():
    return Response(content="", media_type="image/x-icon")

# Start the training script


@app.post("/startTraining")
async def start_training():
    try:
        subprocess.check_call(['python', 'start.py'])
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return {"message": "Failed to start training process"}

    return {"message": "Training process started successfully"}

# Collect and lists up files before sending the email


@app.get("/get_files")
async def get_files():
    folder_path = os.path.join(BASE_DIR, "kartAI", "training_data",
                               "Training_data", "3857_563000.0_6623000.0_100.0_100.0", "512")
    files = [f for f in os.listdir(
        folder_path) if f.endswith(('.tif', '.json', '.vrt'))]
    num_files = len(files)
    if num_files == 0:
        folder_summary = "No files found!"
    else:
        folder_summary = f"{num_files} file(s) selected: <br><br> {', '.join(files)}"
    return {"folder_summary": folder_summary}


def zip_folder(folder_path, zip_file, folder_prefix):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.join(
                folder_prefix, os.path.relpath(file_path, folder_path))
            zip_file.write(file_path, arcname)


@app.post("/send_zip_file")
async def send_zip_file(request: Request):
    # Extract email from request
    email = {}
    if request.body:
        email = await request.json()

    if not email:
        print("No email specified")
        return {"message": "No email specified"}

    # Get the absolute path of the training data folder
    training_data_folder = os.path.join(
        BASE_DIR, "kartAI", "training_data", "Training_data")
    folder_2 = os.path.join(
        BASE_DIR, "kartAI", "training_data", "created_datasets")
    folder_3 = os.path.join(BASE_DIR, "kartAI", "training_data", "OrtofotoWMS")

    # Create a zip file containing the training data folders and their contents
    selected_files = []
    zipf = zipfile.ZipFile("All_Data.zip", "w", zipfile.ZIP_DEFLATED)
    zip_folder(training_data_folder, zipf, "Training_data")
    zip_folder(folder_2, zipf, "created_datasets")
    zip_folder(folder_3, zipf, "OrtofotoWMS")

    zipf.close()

    print(
        f"Size of the zip file before sending: {os.path.getsize('All_Data.zip')} bytes")

    # Generate the summary of selected files
    num_files = len(selected_files)
    files_str = f"{num_files} files"
    if num_files == 1:
        files_str = "1 file"
    elif num_files == 0:
        files_str = "no files"
    else:
        files_str = f"{num_files} files"

    selected_files_summary = f"The following {files_str} will be sent: {' | '.join(selected_files)}"

    # Send the email with the zip file as an attachment
    message = Mail(
        from_email="KartAi-no-reply@hotmail.com",
        to_emails=email["email"],
        subject="Training data",
        html_content=f"<strong>The ordered training data is attached</strong>"

    )

    with open("All_Data.zip", "rb") as f:
        attachment = f.read()
    # Encode the attachment in base64 and attach it to the email message
    encoded_file = base64.b64encode(attachment).decode()

    attachedFile = Attachment(
        FileContent(encoded_file),
        FileName('All_Data.zip'),
        FileType('application/zip'),
        Disposition('attachment')
    )

    message.attachment = attachedFile

    # Loads the .env-file
    dotenv_path = os.path.join(
        os.path.dirname(__file__), 'ngisopenapi', '.env')
    load_dotenv(dotenv_path)

    # Collects the API_KEY from the .env-file
    api_key = os.getenv('API_KEY')
    # Send the email using SendGrid API
    try:
        sg = sendgrid.SendGridAPIClient(api_key=api_key)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

    # Delete the zip file that is temporary stored
    os.remove("All_Data.zip")

    return {"message": "Email was sent successfully!"}


'''
    HER BEGYNNER WMS TING
'''


#Defines the filepaths for where the coordiantes and config will be stored
def get_paths(session_id):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    return {"coordinates": os.path.abspath(os.path.join(BASE_DIR, "datasets", "dataset_" + str(session_id), "coordinates.json")), "config": os.path.abspath(os.path.join(BASE_DIR, "datasets", "dataset_" + str(session_id), "config.json")), "root": os.path.abspath(os.path.join(BASE_DIR, "datasets", "dataset_" + str(session_id)))}



@app.post("/setupUserSessionFolders")
async def setup_session_folders(request: Request, response: Response):
    '''
    Sets up the folders to be used for storing images and etc for this user for this session
    '''
    session_id = get_session_id(request);
    if session_id == None:
        set_session_cookie(response, None)
        return FileResponse(os.path.join("frontend", "pages", "home.html"))
    else:
        print(f"Existing session, session_id: {session_id}")
        session_id = request.cookies.get("session_id", None)
        util.setup_user_session_folders(session_id)



#Route for updating the coordinate file in the WMS/Resources folder
@app.post("/updateWMSCoordinateFile")
async def update_wms_coordinate_file(input: Input, request: Request):
    '''
    Updates the Coordinate file for WMS requests
    
    Args:
    input (Input): An object of the Input class with the required fields. 
    
    Returns:
    A message if the coordinates were updated successfully
    '''
    session_id = request.cookies.get("session_id", None)
    coordinate_path = get_paths(session_id)["coordinates"]
    data = {"Coordinates": input.input}
    if(util.write_file(coordinate_path, data)):
        return {"Message": "Coordinates were updated successfully"}

#Route for updating the coordinate file in the WMS/Resources folder
@app.post("/updateWMSConfigFile")
async def update_wms_config_file(configInput: ConfigInput, request: Request):
    '''
    Updates the Config file for WMS requests
    
    Args:
    configInput (ConfigInput): An object of the ConfigInput class with the required fields. 
    
    Returns:
    A message if the config was updated successfully
    '''
    data = {"Config": {
        "data_parameters": configInput.data_parameters,
        "layers": configInput.layers,
        "colors": configInput.colors,
        "tile_size": configInput.tile_size,
        "image_resolution": configInput.image_resolution
    }}
    session_id = request.cookies.get("session_id", None)
    config_path = get_paths(session_id)["config"]
    if(util.write_file(config_path, data)):
        return {"Message": "Config was updated successfully"}


@app.post("/generatePhotos")
async def generatePhotos(request: Request):
    '''
    Makes requests to the WMSes and splits the resulting images into a valid configuration for machine learning
    
    Returns:
    A message informing if there was an error or if everything went successfully
    '''

    #Read config from the file
    session_id = request.cookies.get("session_id", None)
    paths = get_paths(session_id)
    config = util.read_file(paths["config"])["Config"];

    if labelPhotoWMS.generate_label_data(paths) is not True or ortoPhotoWMS.generate_training_data(paths) is not True or labelPhotoWMS.generate_label_data_colorized(paths) is not True:
        print("Something went wrong with generating the data")
        return {"Message": "Something went wrong with generating the data"}
    else:
        labelTiles = 0
        for path in os.listdir(os.path.join(paths["root"],"tiles", "fasit")):
            if os.path.isfile(os.path.join(paths["root"],"tiles", "fasit", path)):
                labelTiles += 1
        trainingTiles = 0
        for path in os.listdir(os.path.join(paths["root"],"tiles", "orto")):
            if os.path.isfile(os.path.join(paths["root"],"tiles", "orto", path)):
                trainingTiles += 1

        if(labelTiles != trainingTiles):
            return {"Message": "Amount of tiles do not match, please try again"}
        
        util.split_files(os.path.join(paths["root"], "tiles"), os.path.join(paths["root"],"email"), labelTiles, config["data_parameters"][0], config["data_parameters"][1])
        return 0

# Her begynner fil zipping og epost sending for WMS/Fasit
    
# Finner path til .env filen som ligger i ngisopenapi mappen
env_file_path = os.path.join("ngisopenapi", ".env")

# Laster .env fra riktig path
load_dotenv(env_file_path)
    
def send_email_with_attachment(to_emails, subject, content, attachment_path):
    """Define email sending through SendGrid"""

    if not os.path.exists(attachment_path):
        raise FileNotFoundError(f"Attachment '{attachment_path}' not found.")


    message = Mail(
        from_email='victbakk@gmail.com', # Sender epost api
        to_emails=to_emails, # Til epost som blir lagt inn, tror den er definert som "email" i koden.
        subject=subject,
        html_content=content
    )

    with open(attachment_path, 'rb') as f:
        data = f.read()
    encoded_file = base64.b64encode(data).decode()

    attachedFile = Attachment(
        FileContent(encoded_file),
        FileName(os.path.basename(attachment_path)),
        FileType('application/zip'),
        Disposition('attachment')
    )
    message.attachment = attachedFile

    try:
        sg = SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))  # Henter API nøkkel
        response = sg.send(message)
        # Prints response below
        print(f"Email sent. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

def zip_files(directory_path: str = os.path.join("WMS", "email/"), zip_name: str = 'attachments.zip'):
    """Zip all files in the specified directory and save them to a zip file."""
    with ZipFile(zip_name, 'w') as zipf:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, arcname=os.path.relpath(file_path, directory_path))

@app.post("/sendEmail")
async def send_zipped_files_email(request : Request):

        # Extract email from request
    email = {}
    if request.body:
        email = await request.json()
    """Zip and send email to endpoint"""
    zip_files()  # Zipper alle filer i WMS/email/
    
    send_email_with_attachment(
        to_emails=email["email"],
        subject="Here are your zipped files",
        content="<strong>Zip file holding the requested data.</strong>",
        attachment_path="attachments.zip"
    )
    
    # Sletter zip etter sending
    os.remove("attachments.zip")
    #Sletter alle de midlertidige mappene for WMS
    util.teardown_WMS_folders()
    
    return {"message": "Email sent successfully with zipped files."}
