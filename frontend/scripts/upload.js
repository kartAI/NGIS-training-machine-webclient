document.getElementById('file-input').addEventListener('change', function() {
    var file = this.files[0];
    var reader = new FileReader();
    reader.onload = function(e) {
        var data = JSON.parse(e.target.result);
        var geojsonLayer = L.geoJSON(data, {
            onEachFeature: function(feature, layer) {
                var coordinates4326 = feature.geometry.coordinates[0]; // Access the first nested array
                var coordinates3857 = [];
                var latLongCoordinates = coordinates4326.map(function(coord) {
                    // Convert from EPSG 4326 (lat-long) to EPSG 3857 (Web Mercator)
                    var point = proj4('EPSG:4326', 'EPSG:3857', [coord[0], coord[1]]);
                    coordinates3857.push(point); // Add the converted point to the 3857 array
                    return [coord[0], coord[1]]; // Return the original point in lat-long format
                });

                var output = '';
                for (var i = 0; i < latLongCoordinates.length; i++) {
                    output += '<b>P' + (i + 1) + ':</b> ' + latLongCoordinates[i] + '<br>';
                }
                document.getElementById('coordinates').innerHTML = output;
                updateCoordinates(coordinates3857);
            }
        });
        geojsonLayer.addTo(map);
        map.fitBounds(geojsonLayer.getBounds());
    };
    reader.readAsText(file);

    async function updateCoordinates(coords) {
        const response = await fetch('http://localhost:8000/update_coordinates', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(coords),
        });
      
        const data = await response.json();
        return data;
      }
});
