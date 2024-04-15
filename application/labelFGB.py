import geopandas as gpd
import rasterio
from rasterio.features import rasterize
from rasterio.transform import from_bounds
import json
from rasterio.crs import CRS
from shapely.geometry import box, shape 
import os
from application import util  
import shutil


def generate_label_data(file_paths):

    '''
    This function is used to generate label photos for machine learning
    Args:
    file_paths (dict): The file paths to the user session folders
    Returns: 
    bool: True if generation of photos was successful, false otherwise
    '''
    
    # Finds the path to the coordinates file
    coordinates_file_path = file_paths["coordinates"]
    config_file_path = file_paths["config"]

    # Reads the coordinates from the coordinates-JSON file
    coordinates = util.read_file(coordinates_file_path)['Coordinates']
    config = util.read_file(config_file_path)["Config"]
    print("Starting the process of generating label photos with coordinates: " + str(coordinates) + " and config settings: " + str(config))

    # Directory where the image will be saved
    images_directory = "fasit"
    images_directory_path = os.path.join(file_paths["root"], "tiles", images_directory)
    temp_geojson_directory = os.path.join(file_paths["root"])

    print("Images will be saved to: " + str(images_directory_path))

    # Calculates the preferred image size for each call and the array of bboxes to be used to making the calls
    bboxes = util.create_bbox_array(coordinates, config)

    #Open the file and use the geopandas library to get only the features within the bbox
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    gdf = gpd.read_file(os.path.join(BASE_DIR, "resources", "FGBInput.fgb"))
    #Get the bbox from the util file
    temp = util.create_bbox(coordinates)
    bbox = box(temp["minx"], temp["miny"], temp["maxx"], temp["maxy"])
    #Use the geopandas library to filter the features based on the bbox
    features_within_bbox = gdf[gdf.geometry.within(bbox)]
    #Write the features to a temp file
    features_within_bbox.to_file(os.path.join(temp_geojson_directory,'filtered_features.geojson'), driver='GeoJSON')

    # Get the bounding boxes for each image
    i = 0
    amountToMake = len(bboxes)
    for bbox in bboxes:
        file_name = f"tile_{i}.tif"
        # Create a new raster image
        with rasterio.open(
            file_name,
            'w',
            driver='GTiff',
            width=config["tile_size"],
            height=config["tile_size"],
            count=1,
            dtype=rasterio.uint8,
            crs=CRS.from_proj4("+proj=utm +zone=32 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs +type=crs"),
            transform=from_bounds(bbox[0], bbox[1], bbox[2], bbox[3], config["tile_size"], config["tile_size"])
        ) as dst:
            # Load GeoJSON file
            with open(os.path.join(temp_geojson_directory,'filtered_features.geojson')) as src:
                geoms = [shape(feature['geometry']) for feature in json.load(src)['features']]
                if(len(geoms) > 0):
                    # Rasterize the GeoJSON features
                    rasterized = rasterize(
                        geoms,
                        out_shape=(config["tile_size"], config["tile_size"]),
                        transform=dst.transform,
                        fill=1,
                        default_value=0,
                        all_touched=True
                    )
                    
                    # Write the rasterized data to the raster image
                    
                    i+=1
                    dst.write( rasterized , 1)

            #Copy the files to the right directory, they won't be written there for some reason
        shutil.move(file_name, images_directory_path)
        print(f"Saved file to {images_directory_path}")
    if(i == amountToMake):
        return True
    else:
        return False

