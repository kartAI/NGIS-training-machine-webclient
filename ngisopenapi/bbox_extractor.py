import json
import pyproj
from shapely.geometry import shape, box

def get_bbox():
    # Define the source and target CRSs
    src_crs = pyproj.CRS("epsg:3857")
    target_crs = pyproj.CRS("epsg:5972")

    # Read the GeoJSON file
    with open('C:\\temp\\test.geojson', 'r') as f:
        geojson_data = json.load(f)

    # Extract the coordinates of the first polygon feature
    polygon_coords = geojson_data['features'][0]['geometry']['coordinates'][0]

    # Convert the coordinates to a Shapely polygon object
    polygon = shape({
        'type': 'Polygon',
        'coordinates': [polygon_coords]
    })

    # Transform the coordinates to the target CRS
    transformer = pyproj.Transformer.from_crs(src_crs, target_crs, always_xy=True)
    polygon_coords_5972 = [transformer.transform(lon, lat) for lon, lat in polygon_coords]

    # Convert the transformed coordinates to a Shapely polygon object
    polygon_5972 = shape({
        'type': 'Polygon',
        'coordinates': [polygon_coords_5972]
    })

    # Get the bounding box of the polygon
    bbox = polygon_5972.bounds

    # Convert the bounding box to a Shapely polygon object
    bbox_polygon = box(*bbox)

    bbox_geojson = f"{bbox_polygon.bounds[0]},{bbox_polygon.bounds[1]},{bbox_polygon.bounds[2]},{bbox_polygon.bounds[3]}"

    # Print the bounding box
    print('Minimum X:', bbox_polygon.bounds[0])
    print('Maximum X:', bbox_polygon.bounds[2])
    print('Minimum Y:', bbox_polygon.bounds[1])
    print('Maximum Y:', bbox_polygon.bounds[3])

    return bbox_geojson
