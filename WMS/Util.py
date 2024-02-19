#Import Pillow library for working with images
from PIL import Image
import os
import shutil


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
    print("done");

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

    #Return the amount of tiles created
    return horizontal_tiles + vertical_tiles


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

    try:
         #Generate output folder
        os.mkdir(output_folder + "/")

        #Generate subfolders based on the standard
        folders = ["train", "val", "/train/images", "/train/masks", "/val/images", "/val/masks"]
        for folder in folders:
            path = os.path.join(output_folder + "/" + folder)
            os.mkdir(path)
    except: 
        print("Something went wrong with generating the folders...")


    #Calculate the amount of files for each fraction
    training_files = int(training_fraction)/100 * int(tiles)
    validation_files = int(validation_fraction)/100 * int(tiles)

    #Copy the files into the right places
    for i in range(0, tiles):
        if(i < training_files):
            try:
                shutil.copy2(image_path + f"/orto/tile_{i}_{i}.png", output_folder + "/train/images")
                shutil.copy2(image_path + f"/fasit/tile_{i}_{i}.png", output_folder + "/train/masks")
            except:
                print("Something went wrong with copying...")
        else:
            try:
                shutil.copy2(image_path + f"/orto/tile_{i}_{i}.png", output_folder + "/val/images")
                shutil.copy2(image_path + f"/fasit/tile_{i}_{i}.png", output_folder + "/val/masks")
            except:
                print("Something went wrong with copying...")

    #Delete the files, we dont need them anymore
    for i in range(0, tiles):
        try:
            os.remove(image_path + f"/orto/tile_{i}_{i}.png")
            os.remove(image_path + f"/fasit/tile_{i}_{i}.png")
        except:
            print("Couldn't delete")


