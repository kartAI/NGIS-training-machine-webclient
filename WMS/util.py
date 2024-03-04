#Import Pillow library for working with images
from PIL import Image
import os
import shutil
import json
from fastapi import HTTPException


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
                shutil.copy2(os.path.join(image_path, "orto", f"tile_{i}.png"),   os.path.join(output_folder, "train", "images"))
                shutil.copy2( os.path.join(image_path, "fasit", f"tile_{i}.png"),   os.path.join(output_folder, "train", "masks"))
            except:
                print("Something went wrong with copying...")
                return
        else:
            try:
                shutil.copy2(os.path.join(image_path, "orto", f"tile_{i}.png"),   os.path.join(output_folder, "val", "images"))
                shutil.copy2( os.path.join(image_path, "fasit", f"tile_{i}.png"),   os.path.join(output_folder, "val", "masks"))
            except:
                print("Something went wrong with copying...")
                return


def setup_user_session_folders(session_id):
    '''Sets up folders for a new user session'''
    if not os.path.exists("datasets"):
        os.mkdir("datasets")
    #Setup the main folder 
    main_folder_name = "dataset_" + str(session_id)
    os.makedirs(os.path.join("datasets", main_folder_name), exist_ok=True)
    coordinates_path = os.path.join("datasets", main_folder_name, "coordinates.json")
    config_path = os.path.join("datasets", main_folder_name, "config.json")
    if not os.path.exists(coordinates_path):
        open(coordinates_path, "x")
    if not os.path.exists(config_path):
        open(config_path, "x")
    setup_WMS_folders(os.path.join("datasets", main_folder_name))


def setup_WMS_folders(file_path):
    '''
    Sets up the folders to store image data for the WMS part of the application
    '''
    folders_to_make = [os.path.join(file_path, "email", "train", "images"),
    os.path.join(file_path, "email", "train", "masks"),
    os.path.join(file_path, "email", "val", "images"),
    os.path.join(file_path, "email", "val", "masks"),
    os.path.join(file_path, "email", "colorized"),
    os.path.join(file_path, "rawphotos"),
    os.path.join(file_path, "tiles", "fasit"),
    os.path.join(file_path, "tiles", "orto")]
    for folder in folders_to_make:
            os.makedirs(folder, exist_ok=True)


def teardown_user_session_folders(session_id):
    shutil.rmtree(os.path.join("datasets", "dataset_" + str(session_id)))
 


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

def create_bbox_array(coordinates, config):
    min_x = min(coord[0] for coord in coordinates)
    min_y = min(coord[1] for coord in coordinates)
    max_x = max(coord[0] for coord in coordinates)
    max_y = max(coord[1] for coord in coordinates)

    starting_point = [min_x, min_y]
    ending_point = [max_x, max_y]

    preferred_image_size = [config["tile_size"], config["tile_size"]]
    resolution = config["image_resolution"] # meters per pixel
    bbox_size = [preferred_image_size[0]*resolution, preferred_image_size[1]*resolution]
    # Get the number of images needed to cover the area
    num_images_x = int((ending_point[0] - starting_point[0]) / bbox_size[0])
    num_images_y = int((ending_point[1] - starting_point[1]) / bbox_size[1])
    
    
    bboxes = []
    for x in range(num_images_x):
        for y in range(num_images_y):
            x0 = starting_point[0] + (x * bbox_size[0])
            y0 = starting_point[1] + (y * bbox_size[1])
            x1 = starting_point[0] + ((x + 1) * bbox_size[0])
            y1 = starting_point[1] + ((y + 1) * bbox_size[1])
            
            bboxes.append([x0, y0, x1, y1])
    return bboxes