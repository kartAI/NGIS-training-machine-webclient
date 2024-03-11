from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import rasterio
import imageio

#Loads hidden values in script
current_script_directory = os.path.dirname(os.path.abspath(__file__))
env_file_path = os.path.join(current_script_directory, "..", "ngisopenapi", ".env")

# Utilize dotenv to load necessary environment variables, if not already configured in the environment
load_dotenv(env_file_path)

# Set GDAL environment variables for Azure Blob Storage access using values stored in environment variables
os.environ['AZURE_STORAGE_ACCOUNT'] = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')
os.environ['AZURE_STORAGE_ACCESS_KEY'] = os.getenv('AZURE_STORAGE_ACCESS_KEY')

# Construct the URL for the COG file within Azure Blob Storage using GDAL's virtual file system handler for Azure
storage_account_name = "cogurl"
container_name = "cogurl2024"
file_name = "agdertelemarkmosaictif.tif"
cog_url = f"/vsiaz/{container_name}/{file_name}"

# Ensure cogFolder exists
output_folder = os.path.join(current_script_directory, "cogFolder")
os.makedirs(output_folder, exist_ok=True)

# Open and visualize the COG file using rasterio and matplotlib
with rasterio.open(cog_url) as src:
    # Assume the COG file is single-band; modify accordingly for multi-band images
    band1 = src.read(1)
    
    # Utilize matplotlib to display the image
    plt.imshow(band1, cmap='gray')
    # Save the figure
    figure_path = os.path.join(output_folder, "visualized_cog_image.png")
    plt.savefig(figure_path)
    plt.show()

    # Save the image data directly (need to close popup in order for generation to work)
    data_path = os.path.join(output_folder, "cog_image_data.tif")
    imageio.imwrite(data_path, band1)