import pyproj

# Define the source and target projections
src_proj = pyproj.Proj('epsg:4326')
tgt_proj = pyproj.Proj('epsg:5972')

# Define a list of coordinates to transform
coordinates = [(59.88428843596066, 10.52247333500418), 
               (59.887024441455345, 10.528309821820587), 
               (59.89122495633452, 10.520885467267364),
               (59.89092339860052, 10.515091895795196),
               (59.88795075447632, 10.514705657697052)]

# Transform each coordinate and print the result
for x, y in coordinates:
    lon, lat = pyproj.transform(src_proj, tgt_proj, x, y)
    print(f'X: {lon}, Y: {lat}')
