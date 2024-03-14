from dotenv import load_dotenv
import os
import json
import matplotlib.pyplot as plt
import rasterio
from rasterio.windows import from_bounds
import imageio
import numpy as np

# Load JSON data
current_script_directory = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(current_script_directory, "coordinates.json")

with open(json_file_path, 'r') as f:
    data = json.load(f)

# Assuming 'Coordinates' is a list of [x, y] pairs
coordinates = data['Coordinates']

# Calculate bounding box
xmin = min([coord[0] for coord in coordinates])
xmax = max([coord[0] for coord in coordinates])
ymin = min([coord[1] for coord in coordinates])
ymax = max([coord[1] for coord in coordinates])

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
    # Determine the window to read based on the bounding box
    window = from_bounds(xmin, ymin, xmax, ymax, src.transform)

    # Read the data within the bounding box
    red = src.read(1, window=window)
    green = src.read(2, window=window)
    blue = src.read(3, window=window)

    # Stack bands
    rgb = np.dstack((red, green, blue))

if rgb.size > 0:
    # Utilize matplotlib to display the RGB image
    plt.imshow(rgb)
    plt.axis('on')  # Remove axis
    plt.show()

    # Save the figure as an RGB image
    figure_path = os.path.join(output_folder, "rgb_cog_image.png")
    plt.imsave(figure_path, rgb)
    
    # Generate tif file
    data_path = os.path.join(output_folder, "rgb_cog_image_data.tif")
    imageio.imwrite(data_path, (rgb * 255).astype(np.uint8))
else:
    print("The specified bounding box does not intersect with the COG file data.")
    
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