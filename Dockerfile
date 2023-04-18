# Use the osgeo/gdal base image
FROM osgeo/gdal:ubuntu-small-latest

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install the necessary packages using pip
RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install python-dotenv requests psycopg2-binary matplotlib tensorflow azure-storage-blob imageio fastapi uvicorn sendgrid jinja2 pyproj shapely

# Make port 80 available to the world outside this container
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
