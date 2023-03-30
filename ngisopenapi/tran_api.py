import requests

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

coordinates = [(10.51749515507254, 59.884356859704404), (10.51749515507254, 59.888276515139424),(10.527923583722442, 59.888276515139424), (10.527923583722442, 59.884356859704404)]
transformed = transform_coords(coordinates, 4326, 3857)
print(f"Transformed coordinates (4326 -> 5972):", transformed)