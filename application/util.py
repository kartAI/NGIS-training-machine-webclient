#Import Pillow library for working with images
from PIL import Image
import os
import shutil
import json
from fastapi import HTTPException
from shapely.geometry import Polygon, MultiPoint
import shapely 


def split_files(image_path, output_folder, training_fraction):
    '''
    Splits a set of tiles and sorts them according to machine learning specifications
    
    Args:
    image_path (str): The path to where the images are stored 
    output_folder (str): The path to the output folder
    tiles (int): The amount of tiles that need to be handled
    training_fraction (int): The amount of tiles that will be used for training
    validation_fraction (int): The amount of tiles that will be used for validation
    
    Returns:
    bool: True if all files were moved successfully, False otherwise
    '''

    if(not os.path.exists(os.path.join(image_path, "orto")) or not os.path.exists(os.path.join(image_path, "fasit")) or not os.path.exists(output_folder)):
        return False
    
    training_tiles = os.listdir(os.path.join(image_path, "orto"))
    validation_tiles = os.listdir(os.path.join(image_path, "fasit"))

    # Calculate the amount of files for each fraction
    total_tiles = len(training_tiles) + len(validation_tiles)
    training_files = int(training_fraction)/100 * total_tiles  
    
    training_tiles_moved = 0
    validation_tiles_moved = 0

    print("Starting the process of distributing the files according to your settings.")

    for i in range(0, len(training_tiles)):
        if(i < training_files):
            destination = os.path.join(output_folder, "train", "images")
        else:
            destination = os.path.join(output_folder, "val", "images")
        try:
            shutil.copy2(os.path.join(image_path, "orto", training_tiles[i]), destination)
            training_tiles_moved += 1
        except:
            print("Couldn't copy training data correctly")

    for i in range(0, len(validation_tiles)):
        if(i < training_files):
            destination = os.path.join(output_folder, "train", "masks")
        else:
            destination = os.path.join(output_folder, "val", "masks")
        try:
            shutil.copy2(os.path.join(image_path, "fasit", validation_tiles[i]), destination)
            validation_tiles_moved += 1
        except:
            print("Couldn't copy validation data correctly")

    if(validation_tiles_moved == len(validation_tiles) and training_tiles_moved == len(training_tiles)):
        print("Finished distributing files successfully!")
        return True
    else:
        print("Something went wrong with distributing the files")
        return False
        




def setup_user_session_folders(session_id):
    '''Sets up folders for a new user session'''
    # If the datasets folder does not exist, create a new one
    if not os.path.exists("datasets"):
        os.mkdir("datasets")
    # Setup the main folder
    main_folder_name = "dataset_" + str(session_id)
    os.makedirs(os.path.join("datasets", main_folder_name), exist_ok=True)
    # Setup the files for coordinates and config for each user session
    coordinates_path = os.path.join("datasets", main_folder_name, "coordinates.json")
    config_path = os.path.join("datasets", main_folder_name, "config.json")

    if not os.path.exists(coordinates_path):
        open(coordinates_path, "x").close()
    if not os.path.exists(config_path):
        open(config_path, "x").close()

    # Setup the files that will contain images and etc
    folders_to_make = [os.path.join("datasets", main_folder_name, "email", "train", "images"),
    os.path.join("datasets", main_folder_name, "email", "train", "masks"),
    os.path.join("datasets", main_folder_name, "email", "val", "images"),
    os.path.join("datasets", main_folder_name, "email", "val", "masks"),
    os.path.join("datasets", main_folder_name, "email", "colorized"),
    os.path.join("datasets", main_folder_name, "tiles", "fasit"),
    os.path.join("datasets", main_folder_name, "tiles", "orto")]
    
  
    # Create the folders
    for folder in folders_to_make:
            os.makedirs(folder, exist_ok=True)

    #Path for the metadata file.
    metadata_path = os.path.join("datasets", main_folder_name,"email", "metadata.json")
    if not os.path.exists(metadata_path):
        open(metadata_path, "x").close()
    
    
    # Check if all folders were created
    allCreated = True
    for folder in folders_to_make:
        if not os.path.exists(folder):
            allCreated = False

    return allCreated

# Utilizes shutil library to remove the folders
def teardown_user_session_folders(dataset_name, session_id):
    shutil.rmtree(os.path.join("datasets", "dataset_" + str(session_id)))
 


def read_file(file_path):
    '''
    Reads a json file and returns the json contents
    Args:
    file_path (str): The path to the file that you want to read
    '''
    if(os.path.exists(file_path)):
        file = open(file_path)
        data = json.load(file)
        file.close()
        return data
    else:
        raise HTTPException(status_code=500, detail=f"Could not find file: {str(file_path)}")
        

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
    
def create_bbox_array(coordinates, config):
    '''
    Creates a bbox based on coordiantess
    Args:
    coordinates (array): An array of the coordinates you want to convert to bbox
    config (dict): Configuration settings including tile size and image resolution.
    Return:
    The requested bbox or if there are not enough coordinates it returns false
    '''

    if(len(coordinates) < 4):
        return False

    #Create one big bbox that covers the entire polygon
    polygon = Polygon(coordinates)
    bigBox = polygon.envelope
    bigBoxCoords = list(bigBox.exterior.coords)
    # Calculate bounds for the bounding boxes
    min_x = min(coord[0] for coord in bigBoxCoords)
    min_y = min(coord[1] for coord in bigBoxCoords)
    max_x = max(coord[0] for coord in bigBoxCoords)
    max_y = max(coord[1] for coord in bigBoxCoords)
    # Define starting and ending points
    starting_point = [min_x, min_y]
    ending_point = [max_x, max_y]
    # Configure tile size and resolution
    preferred_image_size = [config["tile_size"], config["tile_size"]] # Pixels per time, recommendend is 500
    resolution = config["image_resolution"] # Meters per pixel, recommended is 0.2
    bbox_size = [preferred_image_size[0]*resolution, preferred_image_size[1]*resolution]
    
    # Determine the number of images required to cover the area
    num_images_x = int((ending_point[0] - starting_point[0]) / bbox_size[0])
    num_images_y = int((ending_point[1] - starting_point[1]) / bbox_size[1])
    
    # Generate bounding boxes
    bboxes = []
    for x in range(num_images_x):
        for y in range(num_images_y):
            x0 = starting_point[0] + (x * bbox_size[0])
            y0 = starting_point[1] + (y * bbox_size[1])
            x1 = starting_point[0] + ((x + 1) * bbox_size[0])
            y1 = starting_point[1] + ((y + 1) * bbox_size[1])
            
            coords = [[x0, y0], [x0 + bbox_size[0], y0],[x0, y0 + bbox_size[1]], [x1, y1]]
            bbox = Polygon(coords)
            if(bbox.intersects(polygon)):
                bboxes.append([x0, y0, x1, y1])
    return bboxes

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
    return {"minx": min_x, "miny":min_y, "maxx":max_x, "maxy":max_y}


def bbox_overlap(bbox1, bbox2):
    """
    Check if two bounding boxes overlap.
    
    Parameters:
        bbox1 (tuple): Coordinates of the first bounding box in the format (x1, y1, x2, y2),
                       where (x1, y1) represent the top-left corner and (x2, y2) represent the bottom-right corner.
        bbox2 (tuple): Coordinates of the second bounding box in the same format as bbox1.
    
    Returns:
        bool: True if the bounding boxes overlap, False otherwise.
    """
    polygon1 = Polygon(bbox1)
    polygon2 = Polygon(bbox2)
    return polygon1.intersects(polygon2)
    
