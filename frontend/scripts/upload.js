document.getElementById('file-input').addEventListener('change', function () {
    var file = this.files[0];
    var reader = new FileReader();

    // Reads the contents of the file and converts it to a JSON object
    reader.onload = function (e) {
        var data = JSON.parse(e.target.result);

        // Creates a new Leaflet GeoJSON layer and adds it to the map
        var geojsonLayer = L.geoJSON(data, {
            onEachFeature: function (feature, layer) {
                var coordinates4326 = feature.geometry.coordinates[0]; // Access the first nested array
                var coordinates3857 = [];
                var latLongCoordinates = coordinates4326.map(function (coord) {

                    // Convert from EPSG 4326 (lat-long) to EPSG 3857 (Web Mercator)
                    var point = proj4('EPSG:4326', 'EPSG:3857', [coord[0], coord[1]]);

                    // Adds the converted point to the 3857 array
                    coordinates3857.push(point);

                    // Return the original point in lat-long format
                    return [coord[0], coord[1]];
                });

                // Creates a string with the lat-long coordinates and displays it
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
    // Sends a POST request with converted coordinates toserver and returns server's response
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
document.getElementById('file-input').addEventListener('change', function () {
    console.log('File input changed');
    var file = this.files[0];
    var reader = new FileReader();
    var nextBtn = document.getElementById('nextBtn'); // Get a reference to the "Next" button

    // Disable the button
    nextBtn.disabled = true;

    reader.onload = function (e) {
        // ...existing code...

        // Enable the button when the file input's change event fires
        nextBtn.disabled = false;
    };

    reader.readAsText(file);
    // ...existing code...
});

document.getElementById('nextBtn').addEventListener('click', function () {
    if (this.disabled) {
        document.getElementById('fileUploadError').style.display = 'block';
    } else {
        // Continue to next step
    }
});