#Import Pillow library for working with images
from PIL import Image
import os
import shutil
import json
from fastapi import HTTPException


def split_image(image_path, output_folder, tile_size):
    '''
    Splits an image (tested with .jpeg, .jpg, .tiff formats) into smaller tiles based on a desired size
    
    Args:
    image_path (str): The path to the image 
    output_folder (str): The path to the output folder
    tile_size (int): Desired size of the tiles 
    
    Returns:
    int: Number of tiles created
    '''
    #Defines the accepted (tested) filetypes that can be split
    acceptedFileTypes = ["jpeg", "jpg", "png", "tiff"]

    #Checks if the file is of the correct type, otherwise raises an error
    if(image_path.split(".")[1] not in acceptedFileTypes):
        return "Filetype not supported"
    

    #Using the Image class from the Pillow library to open the Image
    image = Image.open(image_path)

    #Get the size of the image
    width, height = image.size 

    #Find out how many tiles there are in each direction using floor division
    horizontal_tiles = width // tile_size
    vertical_tiles = height // tile_size

    #Loop through the amount of tiles in both directions and split the image up based on the desired tile size 
    for i in range(horizontal_tiles):
        for j in range(vertical_tiles):
            #Define the corners of each tile 
            left_top = i * tile_size
            left_bottom = j * tile_size
            right_top = (i+1) * tile_size
            right_bottom = (j+1) * tile_size

            #Crop the image based on the tile corners
            tile = image.crop((left_top, left_bottom, right_top, right_bottom))

            #Save the tile to the output folder
            tile.save(f"{output_folder}/tile_{i}_{i}.png")

    #Return the amount of horizontal_tiles created
    print(f"{image_path} split successfully, created {horizontal_tiles} tiles")
    return horizontal_tiles


def split_files(image_path, output_folder, tiles, training_fraction, validation_fraction):
    '''
    Splits a set of tiles and sorts them according to machine learning specifications
    
    Args:
    image_path (str): The path to where the images are stored 
    output_folder (str): The path to the output folder
    tiles (int): The amount of tiles that need to be handled
    training_fraction (int): The amount of tiles that will be used for training
    validation (int): The amount of tiles that will be used for validation
    
    '''

    #Calculate the amount of files for each fraction
    training_files = int(training_fraction)/100 * int(tiles)
    validation_files = int(validation_fraction)/100 * int(tiles)

    #Copy the files into the right places
    for i in range(0, tiles):
        if(i < training_files):
            os.path.join(image_path, "orto", f"tile_{i}_{i}.png")
            os.path.join(output_folder, "train", "images")
            os.path.join(output_folder, "train", "mask")
            try:
                shutil.copy2(os.path.join(image_path, "orto", f"tile_{i}_{i}.png"),   os.path.join(output_folder, "train", "images"))
                shutil.copy2( os.path.join(image_path, "fasit", f"tile_{i}_{i}.png"),   os.path.join(output_folder, "train", "masks"))
            except:
                print("Something went wrong with copying...")
                return
        else:
            try:
                shutil.copy2(os.path.join(image_path, "orto", f"tile_{i}_{i}.png"),   os.path.join(output_folder, "val", "images"))
                shutil.copy2( os.path.join(image_path, "fasit", f"tile_{i}_{i}.png"),   os.path.join(output_folder, "val", "masks"))
            except:
                print("Something went wrong with copying...")
                return


def setup_WMS_folders():
    '''
    Sets up the folders to store image data for the WMS part of the application
    '''
    folders_to_make = [os.path.join("WMS", "email", "train", "images"),
    os.path.join("WMS", "email", "train", "masks"),
    os.path.join("WMS", "email", "val", "images"),
    os.path.join("WMS", "email", "val", "masks"),
    os.path.join("WMS", "rawphotos"),
    os.path.join("WMS", "tiles", "fasit"),
    os.path.join("WMS", "tiles", "orto")]
    for folder in folders_to_make:
            os.makedirs(folder, exist_ok=True)


 

def teardown_WMS_folders():
    '''
    Deletes the folders that are used for image storage by the WMS part of the application
    '''
    try:
        folders_to_delete = [os.path.join("WMS", "email"),
    os.path.join("WMS", "rawphotos"),
    os.path.join("WMS", "tiles")]
        for folder in folders_to_delete:
            shutil.rmtree(folder)
    except:
        print("Folders are already deleted!")


def read_file(file_path):
    '''
    Reads a json file and returns the json contents
    Args:
    file_path (str): The path to the file that you want to read
    '''
    file = open(file_path)
    return json.load(file)

def write_file(file_path, data):
    '''
    Writes json to a file
    Args:
    file_path (str): The path to the file that you want to read
    data: The data you want to write to the file, should be in json format.
    '''
    try:
        with open(file_path, "w") as file:
            json.dump(data, file)  
            return 1
    except Exception as e:
      raise HTTPException(status_code=500, detail=f"Failed to write config to json file: {str(e)}")
    
def create_bbox(coordinates):
    '''
    Creates a bbox based on coordiantess
    Args:
    coordinates (array): An array of the coordinates you want to convert to bbox
    Return:
    The requested bbox 
    '''
    min_x = min(coord[0] for coord in coordinates)
    min_y = min(coord[1] for coord in coordinates)
    max_x = max(coord[0] for coord in coordinates)
    max_y = max(coord[1] for coord in coordinates)
    return f'{min_x},{min_y},{max_x},{max_y}'