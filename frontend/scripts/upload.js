document.getElementById('file-input').addEventListener('change', function() {
    var file = this.files[0];
    var reader = new FileReader();
    reader.onload = function(e) {
        var data = JSON.parse(e.target.result);
        var geojsonLayer = L.geoJSON(data, {
            onEachFeature: function(feature, layer) {
                var coordinates = feature.geometry.coordinates[0]; // Access the first nested array
                var latLongCoordinates = coordinates.map(function(coord) {
                    return [coord[1], coord[0]]; // Swap the coordinates to get lat-long format
                });

                var output = '';
                for (var i = 0; i < latLongCoordinates.length; i++) {
                    output += '<b>P' + (i + 1) + ':</b> ' + latLongCoordinates[i] + '<br>';

                    // Create a circle for each coordinate
                    var circle = L.circle(latLongCoordinates[i], {
                        radius: 10, // Adjust the radius as needed
                        color: 'blue',
                        fillColor: '#f03',
                        fillOpacity: 0.5
                    }).addTo(map);
                    circle.bindPopup('P' + (i + 1) + ' = ' + latLongCoordinates[i]).openPopup();
                }
                document.getElementById('coordinates').innerHTML = output;
                updateCoordinates(latLongCoordinates);   
            }
        });
        geojsonLayer.addTo(map);
        map.fitBounds(geojsonLayer.getBounds());
    };
    reader.readAsText(file);

    async function updateCoordinates(coordinates) {
        const response = await fetch('http://localhost:8000/update_coordinates', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(coordinates),
        });
      
        const data = await response.json();
        return data;
      }
});
