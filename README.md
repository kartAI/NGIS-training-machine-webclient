Once this project is set up correctly you will have the option to order training data for machine learning.

## Steps to use the application

1. Run the application or visit https://ngis.azurewebsites.net/

2. Click "Get Started".

3. Choose your data sources and how you want to input coordinates. You can either draw on the map, write coordinates yourself or upload a GeoJSON file.

4. Decide the data parameters for "training", "validation" and "building percentage".

5. Choose which layers you would like to include and the image settings for the data you are retrieving. (Optional: Enter an email adress to get the data sent to your email)

6. (Optional: Enter an email address to get the data sent to you)

7. Click "Order" and wait for your data to be downloaded.

8. Download your data on the next page, or check your email for a zip file.

  
  

# To run this project locally follow these steps:
## Setup environment variables 

1. In the "Application" folder of your projects create a file that you name ".env"
2. Paste the following variables into the .env file
	"SENDGRID_API_KEY" = ""
	"NK_WMS_API_KEY" = ""
	"OSM_DB_PWD" : "",
	"AZURE_STORAGE_ACCESS_KEY' = ""
	"AZURE_STORAGE_ACCOUNT_NAME' = ""
	"NGISAPI_URL"=""
	"NGISAPI_USER"=""
	"NGISAPI_PASS"=""
	"db_host"=""
	"db_name=""
	"db_user=""
	"db_pass=""
3. Fill in the empty variables, 

## Localhost 

1. Open Anaconda prompt and navigate to the root folder of this project.

2. Paste this into anaconda prompt: conda create -n bachelor2023 python=3.7

3. Paste this into anaconda prompt: conda activate bachelor2023

4. Paste this into anaconda prompt: pip install -r requirements.txt

5. Two of the packages would not install from the requirements.txt so you have to do it manually. Paste this in into anaconda prompt (one at a time):

   conda install libgdal

   conda install gdal

   You will be asked to downgrade the packages (y/n), write "y".  

6. Paste this into anaconda prompt: uvicorn main:app --reload

7. Click on the http link, and the project will open on a localhost on your computer.

## Docker
  

1. Open anaconda prompt, and navigate to the root folder of the project.

2. Open the Docker program on your computer. Dont go to the next step before Docker is ready to use.

3. Paste this into anaconda prompt: "docker build -t docker_env ." this will start building the Docker image.

4. After the docker image is built successfully, paste this command in the anaconda prompt: "docker run -p 8000:8000 docker_env".

5. Open Docker again, and click on the port number on the running contaner.

6. You will now be able to use the project through Docker.
