import os
from zipfile import ZipFile
import base64
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Response
from fastapi import HTTPException, FastAPI, Response, Depends
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from application import util
from application import ortoPhotoWMS
from application import labelPhotoWMS
from application import ortoCOG
from pydantic import BaseModel
from uuid import UUID, uuid4
import random
from fastapi.responses import FileResponse



# Class for the FastAPI. Will contain all our methods for updating values and starting scripts


#Class for the coordinate inputs in the application
class Input(BaseModel):
    input: list
    
#Class for the input for the config file in the application
class ConfigInput(BaseModel):
    data_parameters: list
    layers: list
    colors: list
    tile_size: int
    image_resolution: float

#Class for datasource input
class DataSourceInput(BaseModel):
    label_source: str
    orto_source: str

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
SETUP FASTAPI 
'''

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


'''
 SESSION MANAGEMENT SYSTEM
'''
@app.post("/setCookie")
def set_session_cookie(response: Response, session_id: str = None): # Sets session ID in cookie
    '''
    Sets a cookie for the current session
    Args:
    response (Response): The response object that the session is attached to, this is handled by FastAPI
    session_id (str): The ID of the session you want to attach the cookie to
    
    Returns:
    The ID of the session the cookie was attached to
    '''
    if session_id is None:
        session_id = str(random.randint(0, 1000000000000000))
    response.set_cookie(key="session_id", value=session_id,httponly=True, samesite='Lax') # httponly=True is done for security reasons, unaccessable to javascript.
    print(f"Session cookie set successfully for session_id {session_id}")
    return {"Session_id": session_id}

def get_session_id(request: Request): # Returns session ID
    '''
    Returns the session ID for the current session from the cookies
    Args:
    response (Response): The response object that the session is attached to, this is handled by FastAPI
    
    Returns:
    The session ID that was requested if it exists, otherwise None
    '''
    return request.cookies.get("session_id", None)

@app.post("/cookies")
def read_main(request: Request, response: Response):
    '''
    This function is a fastAPI route that sets the session_id and session_id cookie 
    Args:
    request (Request): The request object that the cookie is attached to, this is handled by FastAPI
    response (Response): The response object that the session is attached to, this is handled by FastAPI
    
    Returns:
    message (bool): True if the cookie was set successfully, false otherwise
    '''
    session_id = get_session_id(request)  # Corrected function call
    if not session_id:
        set_session_cookie(response)
        return {"message": True}
    return {"message": False}


'''
    APPLIATION SPECIFIC ROUTES
'''

#Defines the filepaths for where the coordiantes and config will be stored
def get_paths(session_id):
    '''
    This function dynamically returns the path of the user's folders based on the session id
    Args:
    session_id (str): The id for the session you want to return folder paths for.
    
    Returns:
    (Set) A set of key value pairs where the key is the name of the path you want and the value is the path itself
    '''
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    return {"coordinates": os.path.abspath(os.path.join(BASE_DIR, "datasets", "dataset_" + str(session_id), "coordinates.json")), "config": os.path.abspath(os.path.join(BASE_DIR, "datasets", "dataset_" + str(session_id), "config.json")), "root": os.path.abspath(os.path.join(BASE_DIR, "datasets", "dataset_" + str(session_id)))}


@app.post("/setupUserSessionFolders")
async def setup_session_folders(request: Request, response: Response):
    '''
    Sets up the folders to be used for storing images and etc for this user for this session
    Args:
    request (Request): The request object that the cookie is attached to, this is handled by FastAPI
    response (Response): The response object that the session is attached to, this is handled by FastAPI
    
    '''
    session_id = get_session_id(request);
    if session_id == None:
        set_session_cookie(response, None)
        print("Cookie not set, returning to home")
        return FileResponse(os.path.join("frontend", "pages", "home.html"))
    else:
        print(f"Existing session, session_id: {session_id}")
        session_id = request.cookies.get("session_id", None)
        if(util.setup_user_session_folders(session_id)):
            print(f"All folders were created successfully for session: {session_id}")
        else:
            print(f"Error creating folders for session: {session_id}")
            return {"message": "Something went wrong when setting up the application, please delete your cookie settings and try again!"}



#Route for updating the coordinate file in the WMS/Resources folder
@app.post("/updateCoordinateFile")
async def update_coordinate_file(input: Input, request: Request):
    '''
    Updates the Coordinate file for WMS requests
    
    Args:
    input (Input): An object of the Input class with the required fields. 
    request (Request): The request object that the cookie is attached to, this is handled by FastAPI
    
    Returns:
    A message if the coordinates were updated successfully
    '''
    session_id = request.cookies.get("session_id", None)
    coordinate_path = get_paths(session_id)["coordinates"]
    data = {"Coordinates": input.input}
    if(util.write_file(coordinate_path, data)):
        return {"success_message": "Coordinates were updated successfully"}
    else:
        return {"error_message": "Could not add your chosen coordinates, please try again!"}
    
#Route for updating the config file with the data source choices
@app.post("/updateDataSources")
async def update_data_source(dataSourceInput: DataSourceInput, request: Request):
    '''
    Updates the Config file with data sources
    
    Args:
    dataSourceInput (DataSourceInput): An object of the DataSourceInput class with the required fields. 
    request (Request): The request object that the cookie is attached to, this is handled by FastAPI
    
    Returns:
    A message if the config was updated successfully
    '''

    data = {"Config": {
        "label_source": dataSourceInput.label_source,
        "orto_source": dataSourceInput.orto_source,
        "data_parameters": "",
        "layers": "",
        "colors": "",
        "tile_size": "",
        "image_resolution": ""
    }}
    session_id = request.cookies.get("session_id", None)
    config_path = get_paths(session_id)["config"]
    if(util.write_file(config_path, data)):
        return {"success-message": "Data sources updated successfully!"}
    else:
        return {"error-message": "Could not update your data sources, please try again!"}


#Route for updating the coordinate file in the WMS/Resources folder
@app.post("/updateConfigFile")
async def update_config_file(configInput: ConfigInput, request: Request):
    '''
    Updates the Config file for WMS requests
    
    Args:
    configInput (ConfigInput): An object of the ConfigInput class with the required fields. 
    request (Request): The request object that the cookie is attached to, this is handled by FastAPI
    
    Returns:
    A message if the config was updated successfully
    '''
    session_id = request.cookies.get("session_id", None)
    config_path = get_paths(session_id)["config"]
    label_source = util.read_file(config_path)["Config"]["label_source"]
    orto_source = util.read_file(config_path)["Config"]["orto_source"]

    data = {"Config": {
        "label_source": label_source, 
        "orto_source": orto_source,
        "data_parameters": configInput.data_parameters,
        "layers": configInput.layers,
        "colors": configInput.colors,
        "tile_size": configInput.tile_size,
        "image_resolution": configInput.image_resolution
    }}
   
    if(util.write_file(config_path, data)):
        return {"Message": "Config was updated successfully"}
    else:
        return {"error_message": "Could not update your application settings, please try again!"}


@app.post("/generatePhotos")
async def generatePhotos(request: Request):
    '''
    Makes requests to the WMSes and splits the resulting images into a valid configuration for machine learning

    Args:
    request (Request): The request object that the cookie is attached to, this is handled by FastAPI
    
    Returns:
    A message informing if there was an error or if everything went successfully
    '''

    #Read config from the file
    session_id = request.cookies.get("session_id", None)
    paths = get_paths(session_id)
    config = util.read_file(paths["config"])["Config"];
    label_source = config["label_source"]
    orto_source = config["orto_source"]

    if generateTrainingData(paths, label_source, orto_source) is not True: #labelPhotoWMS.generate_label_data(paths) is not True or ortoCOG.generate_cog_data(paths) is not True or ortoPhotoWMS.generate_training_data(paths) is not True or labelPhotoWMS.generate_label_data_colorized(paths) is not True:
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
        
        zip_files(os.path.join(paths["root"]), f"Dataset_{session_id}.zip")
        return 0
    
def generateTrainingData(paths, label_source, orto_source):
    all_ran = True
    if(label_source == "WMS"):
        if labelPhotoWMS.generate_label_data(paths) is not True:
            print("Label photo (Non-colorized) failed")
            all_ran = False
        if labelPhotoWMS.generate_label_data_colorized(paths) is not True:
            print("Label photo (Colorized) failed")
            all_ran = False
    if(orto_source == "WMS"):
        if ortoPhotoWMS.generate_training_data(paths) is not True:
            print("Ortophoto failed")
            all_ran = False
 
    elif(orto_source == "COG"):
        if ortoCOG.generate_cog_data(paths) is not True:
            print("COG photo  failed")
            all_ran = False

    
    return all_ran

    

@app.get("/downloadFile")
async def download_file(request: Request):
    '''
    FastAPI route that allows a user to download a zip file for their session
    
    Args:
    request (Request): The request object that the cookie is attached to, this is handled by FastAPI
    
    Returns:
    file (FileResponse): The file the user requested, ready for download
    '''

    session_id = request.cookies.get("session_id", None)
    paths = get_paths(session_id)
    headers = {'Content-Disposition': f'attachment; filename="Dataset_{session_id}.zip"'}
    return FileResponse(os.path.join(paths["root"], f"Dataset_{session_id}.zip") ,headers= headers)

@app.post("/deleteFile")
async def delete_files(request: Request):
    '''
    FastAPI route that deletes a user's files after downloading
    
    Args:
    request (Request): The request object that the cookie is attached to, this is handled by FastAPI
    
    '''
    session_id = request.cookies.get("session_id", None)
    util.teardown_user_session_folders(session_id)


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

def zip_files(directory_path: str, zip_name: str = 'attachments.zip'):
    """Zip all files in the specified directory and save them to a zip file."""
    with ZipFile(os.path.join(directory_path, zip_name), 'w') as zipf:
        for root, dirs, files in os.walk(os.path.join(directory_path, "email")):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, arcname=os.path.relpath(file_path, os.path.join(directory_path, "email")))

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
    
    session_id = request.cookies.get("session_id", None)
    util.teardown_user_session_folders(session_id)
    
    return {"message": "Email sent successfully with zipped files."}
