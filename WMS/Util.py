#Import Pillow library for working with images
from PIL import Image


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
    if(image_path.split(".")[2] not in acceptedFileTypes):
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
            tile.save(f"{output_folder}/tile_{i}_{j}.jpeg")

    #Return the amount of tiles created to be used for testing purposes
    return horizontal_tiles + vertical_tiles

