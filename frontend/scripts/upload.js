// Listen for changes in the file input element
document.getElementById('file-input').addEventListener('change', function () {
    // Retrieve the first file selected by the user
    var file = this.files[0];

    // Initialize FileReader to read the content of the file
    var reader = new FileReader();

    // Function to be called when the file is successfully read
    reader.onload = function (e) {
        // Attempt to parse the file content as JSON
        try {
            var data = JSON.parse(e.target.result);

            // Process the JSON data (assuming GeoJSON structure for map visualization)
            var geojsonLayer = L.geoJSON(data, {
                onEachFeature: function (feature, layer) {
                    // Example processing for each feature in the GeoJSON object
                    // This could include converting coordinates, adding to a map layer, etc.
                }
            });
            // Add the processed layer to the map and adjust the map's view accordingly
            geojsonLayer.addTo(map);
            map.fitBounds(geojsonLayer.getBounds());

            console.log(data["features"][0]["geometry"]["coordinates"])
        } catch (error) {
            // Alert the user in case of an error parsing the JSON file content 
            alert('Error parsing the JSON file: ' + error);
        }
    };

    // Function to be called when the file has finished loading
    reader.onloadend = function () {
        // Ensure the "Next" button is enabled after the file is loaded
        var nextBtn = document.getElementById('nextBtn');
        nextBtn.disabled = false;
    };

    // Start reading the file as text; suitable for JSON and GeoJSON files
    reader.readAsText(file);
});

// Event listener for the "Next" button click action
document.getElementById('nextBtn').addEventListener('click', function () {
    // Check if the "Next" button is disabled and display an error message if so
    if (this.disabled) {
        document.getElementById('fileUploadError').style.display = 'block';
    } else {
    // Continue to next step if the button is enabled
    }
});
