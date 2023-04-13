import os
import json
import subprocess
import shutil
import smtplib
import ssl
import zipfile
import base64
import sendgrid
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

class Coordinates(BaseModel):
    coordinates: list

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REGION_FILE = os.path.join(
    BASE_DIR, "kartAI", "training_data", "regions", "small_building_region.json")

@app.post("/update_coord.js")
async def update_coordinates(coords: Coordinates):
    coordinates = coords.coordinates
    with open(REGION_FILE, "r") as file:
        data = json.load(file)
    data["coordinates"] = [coordinates]
    with open(REGION_FILE, "w") as file:
        json.dump(data, file)
    return {"status": "success"}


@app.post("/update_coordinates")
async def update_coordinates(coordinates: list):
    with open(REGION_FILE, "r") as file:
        data = json.load(file)
    data["coordinates"] = [coordinates]
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
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/{page}.html", response_class=HTMLResponse)
async def read_page(request: Request, page: str):
    return templates.TemplateResponse(f"{page}.html", {"request": request})


@app.get("/favicon.ico")
async def favicon():
    return Response(content="", media_type="image/x-icon")

@app.post("/startTraining")
async def start_training():
    try:
        subprocess.check_call(['python', 'start.py'])
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return {"message": "Failed to start training process"}

    return {"message": "Training process started successfully"}


@app.get("/get_files")
async def get_files():
    folder_path = r"C:/Users/nikla/OneDrive/Skrivebord/Bachelor/Bachelor/kartAI/training_data/OrtofotoWMS/3857_563000.0_6623000.0_100.0_100.0/512"
    files = [f for f in os.listdir(folder_path) if f.endswith('.tif')]
    num_files = len(files)
    if num_files == 0:
        folder_summary = "Ingen filer funnet!"
    else:
        folder_summary = f"{num_files} fil(er) valgt: <br><br> {', '.join(files)}"
    return {"folder_summary": folder_summary}


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
    training_data_folder = r"C:/Users/nikla/OneDrive/Skrivebord/Bachelor/Bachelor/kartAI/training_data/OrtofotoWMS/3857_563000.0_6623000.0_100.0_100.0/512"

    # Create a zip file
    zipf = zipfile.ZipFile("OrtofotoWMS.zip", "w", zipfile.ZIP_DEFLATED)

    # Add all the .tif files in the training data folder to the zip file
    selected_files = []
    for file_name in os.listdir(training_data_folder):
        if file_name.endswith(".tif"):
            file_path = os.path.join(training_data_folder, file_name)
            zipf.write(file_path, file_name)
            selected_files.append(file_name)

    # Close the zip file
    zipf.close()

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
        from_email="no-reply-KartAI@hotmail.com",
        to_emails=email["email"],
        subject="Training data",
        html_content=f"<strong>Vedlagt ligger treningsdataen som er bestilt.</strong>"

    )

    with open("OrtofotoWMS.zip", "rb") as f:
        attachment = f.read()

    encoded_file = base64.b64encode(attachment).decode()

    attachedFile = Attachment(
        FileContent(encoded_file),
        FileName('OrtofotoWMS.zip'),
        FileType('application/zip'),
        Disposition('attachment')
    )

    message.attachment = attachedFile

    try:
        sg = sendgrid.SendGridAPIClient(
            api_key='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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

    # Delete the zip file
    os.remove("OrtofotoWMS.zip")

    return {"message": "E-post ble sendt!"}
