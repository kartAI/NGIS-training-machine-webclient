from dotenv import load_dotenv
import os
import json
import matplotlib.pyplot as plt
import rasterio
from rasterio.windows import from_bounds
import numpy as np
import imageio

# Define the function to create smaller bounding boxes
def create_bbox_array(coordinates, config):
    """
    Creates a bbox based on coordinates
    Args:
    coordinates (array): An array of the coordinates you want to convert to bbox
    config (dict): Configuration containing tile_size and image_resolution
    Return:
    A list of smaller bounding boxes
    """
    min_x = min(coord[0] for coord in coordinates)
    min_y = min(coord[1] for coord in coordinates)
    max_x = max(coord[0] for coord in coordinates)
    max_y = max(coord[1] for coord in coordinates)

    starting_point = [min_x, min_y]
    ending_point = [max_x, max_y]

    preferred_image_size = [config["tile_size"], config["tile_size"]]
    resolution = config["image_resolution"]  # meters per pixel
    bbox_size = [preferred_image_size[0]*resolution, preferred_image_size[1]*resolution]
    # Get the number of images needed to cover the area
    num_images_x = int((ending_point[0] - starting_point[0]) / bbox_size[0])
    num_images_y = int((ending_point[1] - starting_point[1]) / bbox_size[1])
    
    bboxes = []
    for x in range(num_images_x):
        for y in range(num_images_y):
            x0 = starting_point[0] + (x * bbox_size[0])
            y0 = starting_point[1] + (y * bbox_size[1])
            x1 = x0 + bbox_size[0]
            y1 = y0 + bbox_size[1]
            
            bboxes.append([x0, y0, x1, y1])
    return bboxes

# Configuration for creating smaller images
config = {
    "tile_size": 500,  # pixels
    "image_resolution": 0.2  # meters per pixel, adjust as needed
}

# Load JSON data for initial bounding box
current_script_directory = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(current_script_directory, "coordinates.json")

with open(json_file_path, 'r') as f:
    data = json.load(f)

# Assuming 'Coordinates' is a list of [x, y] pairs
coordinates = data['Coordinates']

# Generate smaller bounding boxes from the initial large bounding box
bboxes = create_bbox_array(coordinates, config)

# Loads hidden values in script
env_file_path = os.path.join(current_script_directory, "..", "ngisopenapi", ".env")

# Utilize dotenv to load necessary environment variables, if not already configured in the environment
load_dotenv(env_file_path)

# Set GDAL environment variables for Azure Blob Storage access using values stored in environment variables
os.environ['AZURE_STORAGE_ACCOUNT'] = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')
os.environ['AZURE_STORAGE_ACCESS_KEY'] = os.getenv('AZURE_STORAGE_ACCESS_KEY')

# Construct the URL for the COG file within Azure Blob Storage using GDAL's virtual file system handler for Azure
container_name = "cogurl2024"
file_name = "agdertelemarkmosaictif.tif"
cog_url = f"/vsiaz/{container_name}/{file_name}"

# Ensure cogFolder exists
output_folder = os.path.join(current_script_directory, "cogFolder")
os.makedirs(output_folder, exist_ok=True)

# Open and visualize the COG file using rasterio
with rasterio.open(cog_url) as src:
    # Loop through each smaller bounding box
    for index, bbox in enumerate(bboxes):
        window = from_bounds(*bbox, transform=src.transform)
        rgb = np.dstack([src.read(i+1, window=window) for i in range(3)])

        if rgb.size > 0:
            # Save the figure as an RGB image for each bounding box
            figure_path = os.path.join(output_folder, f"rgb_cog_image_{index}.png")
            plt.imsave(figure_path, rgb)
            # Generate tif file
            data_path = os.path.join(output_folder, f"rgb_cog_image_data_{index}.tif")
            imageio.imwrite(data_path, (rgb * 255).astype(np.uint8))
               
        else:
            print(f"The bounding box {index} does not intersect with the COG file data.")

    
    '''
        DEBUG PRINT 
    # Open and visualize the COG file
with rasterio.open(cog_url) as src:
    print(f"COG File CRS: {src.crs}")
    print(f"COG File Bounds: {src.bounds}")
    
    # Determine the window to read based on the bounding box
    window = from_bounds(xmin, ymin, xmax, ymax, src.transform)
    print(f"Calculated Window: {window}")
    
    # Read the data within the bounding box
    red = src.read(1, window=window)
    green = src.read(2, window=window)
    blue = src.read(3, window=window)
    '''
