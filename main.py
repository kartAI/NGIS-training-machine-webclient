import os
import json
import subprocess
import shutil
import smtplib
import ssl
import zipfile
import base64
import sendgrid
import asyncio
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Response
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from deleteFolder import delete_all_folders

# Class for the FastAPI. Will contain all our methods for updating values and starting scripts


class Input(BaseModel):
    input: list


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
    dotenv_path = os.path.join(os.path.dirname(__file__), 'ngisopenapi', '.env')
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
