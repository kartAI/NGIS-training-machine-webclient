# Use an official Python runtime as a parent image
FROM continuumio/miniconda3

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install the necessary packages
RUN conda create -n app_env && \
    /bin/bash -c "source activate app_env && \
    conda install -c conda-forge python-dotenv requests psycopg2 gdal matplotlib tensorflow azure-storage-blob imageio && \
    pip install fastapi uvicorn && \
    source deactivate"


# Set up the environment
ENV PATH /opt/conda/envs/app_env/bin:$PATH

# Make port 80 available to the world outside this container
EXPOSE 80

# Makes the docker container not shutting down
CMD ["tail", "-f", "/dev/null"]

