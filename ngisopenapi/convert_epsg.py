def convert_epsg(fname):

    import json
    import pyproj
    import os
    from shapely.geometry import shape, mapping

    with open(os.getenv('f_path') + fname) as f:
        data = json.load(f)

    src_crs = pyproj.CRS(data['crs']['properties']['name'])
    target_crs = pyproj.CRS('EPSG:4326')

    transformer = pyproj.Transformer.from_crs(src_crs, target_crs)

    for feature in data['features']:
        geom = shape(feature['geometry'])
        geom_4326 = transformer.transform(geom)
        feature['geometry'] = mapping(geom_4326)

    with open((os.getenv('f_path') + fname), 'w') as f:
        json.dump(data, f)
