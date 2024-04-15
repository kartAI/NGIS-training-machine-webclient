'''from dotenv import load_dotenv
import os
import re
import itertools
import sys  
import requests
from shapely.geometry import box, shape 
from application import util
from application.ngis_classes.api import NgisOpenApi
from application.ngis_classes import transformer
from shapely.geometry import Polygon, MultiPoint
import pyproj
import geopandas as gpd
import rasterio
from rasterio.features import rasterize
from rasterio.transform import from_bounds
import json
from rasterio.crs import CRS
from shapely.geometry import box, shape 
from shapely import polygonize
import os
from scipy.spatial.distance import cdist
from application import util  
import time
import shutil
import uuid
import geopandas as gpd
import rasterio
from rasterio.features import rasterize
from rasterio.transform import from_bounds
from rasterio.crs import CRS
import math
from shapely.geometry import box, linestring
from shapely.geometry import LineString, Polygon


def rasterize_geojson(geojson_df, out_shape, transform, crs):
    # Create an empty array to store the rasterized data
    rasterized = rasterize(
        [(geom, 1) for geom in geojson_df.geometry],
        out_shape=out_shape,
        transform=transform,
        dtype='uint8',
        all_touched=True,
        fill=0
    )
    return rasterized


def get_api():
    try:
        url = os.getenv('NGISAPI_URL')
        user = os.getenv('NGISAPI_USER')
        password = os.getenv('NGISAPI_PASS')
        return NgisOpenApi(url, user, password, "KartAITest")
    except Exception as e:
        print(f"Error getting API: {e}")
        sys.exit(1) 

coordinateFile =  [[579437.0120495302, 6583346.571546951], [579432.7154448506, 6583551.118976941], [579764.2546158503, 6583558.097703439], [579768.5691575849, 6583353.550518579], [579437.0120495302, 6583346.571546951]]
config = {"label_source": "WMS", "orto_source": "WMS", "data_parameters": ["100", "0", "80"], "layers": ["Bygning", "Veg", "Bru"], "colors": ["#563d7c", "#563d7c", "#563d7c"], "tile_size": 500, "image_resolution": 0.2}

def getNGIS():
    print("Starting NGIS SCRIPT")

    # Finds the path to the coordinates file
    #coordinates_file_path = file_paths["coordinates"]
    #config_file_path = file_paths["config"]

    # Reads the coordinates from the coordinates-JSON file
    #coordinates = util.read_file(coordinates_file_path)['Coordinates']
    #config = util.read_file(config_file_path)["Config"]

    #We need to transform the coordinates to make them work with NGIS (From 25872 to 5)

    temp = util.create_bbox(coordinateFile)
    tempcoords = transformer.convert_bbox_25832_to_5972([temp["minx"], temp["maxx"], temp["miny"], temp["maxy"]])
    tempBox = [[tempcoords[0], tempcoords[2]],[tempcoords[1], tempcoords[3]]]
    #Get the enviornment variables
    current_script_directory = os.path.dirname(os.path.abspath(__file__))
    env_file_path = os.path.join(current_script_directory, "..", "application", ".env")



    #Loads environment variables from the right file
    load_dotenv(env_file_path)
    dataset_id = "093adf63-06f5-42d6-ba11-b79f11bdc271"
    api = get_api()
    #bbox = str([temp["minx"], temp["miny"], temp["maxx"], temp["maxy"]])
    print(tempBox)
    bboxes = util.create_bbox_array(tempBox, config)
    bbox = f"{tempcoords[0]},{tempcoords[1]},{tempcoords[2]},{tempcoords[3]}"
    print(len(bboxes))
    print(bbox)

    file_name = "test.geojson"

     #Calls the api.get_features method to get the features from the NGIS Open-API.
    try:
        res = api.get_features(dataset_id, bbox)
        # Convert coordinates to Shapely LineString objects
        linestring_coords = []
        for feature in res['features']:
            if feature["geometry"]["type"] == 'LineString':
                linestring_coords.append(feature["geometry"]["coordinates"])
        linestrings_shapely = [LineString(coords) for coords in linestring_coords]

        # Initialize lists to store polygons and remaining linestrings
        polygons = []
        linestrings_remaining = []

        # Iterate through each linestring
        for linestring in linestrings_shapely:
            # Check if the linestring has only two points
            if len(linestring.coords) == 2:
                linestrings_remaining.append(linestring)
            else:
                # Calculate the distance between the first and last point
                distance_threshold = 1e-6  # You may need to adjust this threshold based on your data
                start_point = linestring.coords[0]
                end_point = linestring.coords[-1]
                distance = math.sqrt((start_point[0] - end_point[0]) ** 2 + (start_point[1] - end_point[1]) ** 2)
                
                # Check if the distance is very small (indicating closure)
                if distance < distance_threshold:
                    # Convert to polygon if closed
                    polygons.append(Polygon(linestring))
                else:
                    # Otherwise, keep as a linestring
                    linestrings_remaining.append(linestring)

        # Create GeoJSON features for polygons
        print(polygons)
        data = {}

    except Exception as e:
        print("Error in gathering features:", e)
        sys.exit(1)

    for i in range(len(bboxes)):
        print("Starting new box!")
        gdf = gpd.read_file(file_name)
        output_name = f"tile_{i}.tif"
        # Get bounding box of GeoJSON
        #bbox = gdf.total_bounds
        bbox = bboxes[i]
        print(bbox);

        # Define raster dimensions (width, height)
        width = config["tile_size"]
        height = config["tile_size"]

        # Create a raster transform
        transform = from_bounds(bbox[0], bbox[1], bbox[2], bbox[3], width, height)

        # Create a raster CRS
        crs = CRS.from_epsg(5972)  # You can change the EPSG code as per your data

        # Rasterize the GeoJSON data
        raster_data = rasterize_geojson(gdf, (height, width), transform, crs)

        # Define metadata for the GeoTIFF file
        meta = {
            'driver': 'GTiff',
            'count': 1,
            'dtype': raster_data.dtype,
            'width': width,
            'height': height,
            'crs': crs,
            'transform': transform
        }

        # Write raster data to GeoTIFF file
        with rasterio.open(output_name, "w", **meta) as dst:
            dst.write(raster_data, 1)
    

    def load_image(self, image_path, minx, miny, maxx, maxy, tile_size):
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        target_ds = gdal.GetDriverByName('GTiff').Create(
            image_path,
            tile_size, tile_size, 1, gdal.GDT_Byte, ['COMPRESS=LZW', 'PREDICTOR=2'])
        geo_transform = (
            minx, (maxx - minx) / tile_size, 0,
            maxy, 0, (miny - maxy) / tile_size,
        )
        target_ds.SetGeoTransform(geo_transform)
        srs_wkt = self.tile_grid.srs.ExportToWkt()
        target_ds.SetProjection(srs_wkt)

        if self.layer is None:
            self.open()

        # Create ring
        if self.layer.GetSpatialRef():
            ring = ogr.Geometry(ogr.wkbLinearRing)
            ring.AddPoint(minx, miny)
            ring.AddPoint(maxx, miny)
            ring.AddPoint(maxx, maxy)
            ring.AddPoint(minx, maxy)
            ring.AddPoint(minx, miny)

            # Create polygon
            poly = ogr.Geometry(ogr.wkbPolygon)
            poly.AddGeometry(ring)
            poly.AssignSpatialReference(self.tile_grid.srs)
            poly.TransformTo(self.layer.GetSpatialRef())

            self.layer.SetSpatialFilter(poly)

        feature_count = self.layer.GetFeatureCount()
        print('feature count: ', feature_count)
        # Fill raster - Label saved when GDAL completes rasterization
        if isinstance(self.attribute_filter, (list, tuple)):
            for ix, attr_f in enumerate(self.attribute_filter):
                bv = 1 + ix
                if isinstance(attr_f, (list, tuple)):
                    bv = attr_f[0]
                    attr_f = attr_f[1]
                self.layer.SetAttributeFilter(attr_f)
                if gdal.RasterizeLayer(target_ds, [1], self.layer, burn_values=[bv], options=['ALL_TOUCHED=TRUE']) != 0:
                    err = "lar"
                    raise Exception("error rasterizing layer: %s" % err)
        elif isinstance(self.attribute_filter, str):
            self.layer.SetAttributeFilter(self.attribute_filter)
            if gdal.RasterizeLayer(target_ds, [1], self.layer, burn_values=[1], options=['ALL_TOUCHED=TRUE']) != 0:
                err = "lar"
                raise Exception("error rasterizing layer: %s" % err)
        else:
            if gdal.RasterizeLayer(target_ds, [1], self.layer, burn_values=[1], options=['ALL_TOUCHED=TRUE']) != 0:
                err = "lar"
                raise Exception("error rasterizing layer: %s" % err)

        arr = target_ds.ReadAsArray()
        target_ds = None  # Save to file
        return arr, srs_wkt, geo_transform'''