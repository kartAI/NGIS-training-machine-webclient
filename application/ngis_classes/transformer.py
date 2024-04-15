import pyproj

# Function for converting epsg using pyproj


def convert_bbox_25832_to_5972(bbox):
    # Define the input CRS as EPSG 25832
    in_crs = pyproj.CRS.from_proj4("+proj=utm +zone=32 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs +type=crs")

    # Define the output CRS as EPSG 5972
    out_crs = pyproj.CRS.from_epsg(5972)

    # Define the transformer
    transformer = pyproj.Transformer.from_crs(in_crs, out_crs)

    # Convert the bounding box coordinates
    xmin, ymin, xmax, ymax = bbox
    xmin, ymin = transformer.transform(xmin, ymin)
    xmax, ymax = transformer.transform(xmax, ymax)
    bbox_5972 = [xmin, ymin, xmax, ymax]

    return bbox_5972
