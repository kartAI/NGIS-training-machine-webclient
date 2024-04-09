from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import rasterio
from rasterio.windows import from_bounds
import numpy as np
import imageio
from application import util


# Function to generate COG data
def generate_cog_data(file_paths):
    # Finds the current path of the script
    current_script_directory = os.path.dirname(os.path.abspath(__file__))
    coordinates_file_path = file_paths["coordinates"] # Path to the coordinates file
    config_file_path = file_paths["config"] # Path to the config file
    
    #Reads the coordinates from the coordinates-JSON file
    coordinates = util.read_file(coordinates_file_path)['Coordinates'] # Reads the coordinates file
    config = util.read_file(config_file_path)["Config"] # Reads the config file


    preferred_image_size = [config["tile_size"], config["tile_size"]] # Pixels per tile, recommendend is 500
    bboxes = util.create_bbox_array(coordinates, config) # Generates bounding boxes from util script
 
    # Generate smaller bounding boxes from the initial large bounding box
    bboxes = util.create_bbox_array(coordinates, config)

    # Loads hidden values in script
    env_file_path = os.path.join(current_script_directory, "..", "application", ".env")

    # Utilize dotenv to load necessary environment variables, if not already configured in the environment
    load_dotenv(env_file_path)

    # Set GDAL environment variables for Azure Blob Storage access using values stored in environment variables
    os.environ['AZURE_STORAGE_ACCOUNT'] = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')
    os.environ['AZURE_STORAGE_ACCESS_KEY'] = os.getenv('AZURE_STORAGE_ACCESS_KEY')

    # Construct the URL for the COG file within Azure Blob Storage using GDAL's virtual file system handler for Azure
    container_name = "cogurl2024"
    file_name = "agdertelemarkmosaictif.tif"
    cog_url = f"/vsiaz/{container_name}/{file_name}" 


    # Directory where the image will be saved
    images_directory = "orto"
    images_directory_path = os.path.join(file_paths["root"], "tiles", images_directory)

    # Open and visualize the COG file using rasterio
    with rasterio.open(cog_url) as src:
        # Loop through each smaller bounding box
        for index, bbox in enumerate(bboxes): # Enumerate the bounding boxes
            window = from_bounds(*bbox, transform=src.transform) # Create a window from the bounding box
            rgb = np.dstack([src.read(i+1, window=window) for i in range(3)]) # Read the RGB bands for the bounding box

            if rgb.size > 0:
                # Save the figure as an RGB image for each bounding box
                figure_path = os.path.join(images_directory_path, f"rgb_cog_image_{index}.png")
                plt.imsave(figure_path, rgb)
                # Generate tif file
                data_path = os.path.join(images_directory_path, f"rgb_cog_image_data_{index}.tif")
                imageio.imwrite(data_path, (rgb * 255).astype(np.uint8))
                # Print the path to the saved image
                
            else: 
                print(f"The bounding box {index} does not intersect with the COG file data.") # Print if the bounding box does not intersect with the COG file data
    return True

        