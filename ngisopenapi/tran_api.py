import requests
import pyproj

#API for transforming the epsg of one or multiple coordinates

BASE_URL = 'https://ws.geonorge.no'

def get_available_projections(kategori=None, system=None):
    """Fetches a list of available projections from the API."""
    params = {}
    if kategori:
        params["kategori"] = kategori
    if system:
        params["system"] = system
    response = requests.get(f"{BASE_URL}/transformering/v1/projeksjoner", params=params)
    return response.json()


def transform_coord(x, y, fra, til, z=None, t=None):
    """Transforms a single coordinate from one coordinate system to another."""
    params = {"x": x, "y": y, "fra": fra, "til": til}
    if z:
        params["z"] = z
    if t:
        params["t"] = t
    response = requests.get(f"{BASE_URL}/transformering/v1/transformer", params=params)
    return response.json()

def transform_coords(coords, fra, til):
    """Transforms a list of coordinates from one coordinate system to another."""
    data = [{"x": x, "y": y} for x, y in coords]
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f"{BASE_URL}/transformering/v1/transformer?fra={fra}&til={til}", json=data, headers=headers)
    return response.json()


#Function for converting epsg using pyproj
def convert_bbox_3857_to_5972(bbox):
    # Define the input CRS as EPSG 3857
    in_crs = pyproj.CRS.from_epsg(3857)

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