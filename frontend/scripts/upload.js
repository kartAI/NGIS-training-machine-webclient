

function uploadFile(){
    coordSysElement = document.getElementById("coordSys")
    fileElement = document.getElementById("file-input")
    
    if(coordSysElement.value === "None"){
        alert("Please choose a coordinate system!")
        return
    }

    if(!fileElement.files[0]){
        alert("Please add a file!")
        return
    }
    
    // Retrieve the first file selected by the user
    var file = fileElement.files[0];

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

            let coordinateArray = data["features"][0]["geometry"]["coordinates"][0]
            console.log(coordinateArray)
            console.log(coordSysElement.value)
            if(coordSysElement.value != "EPSG:25832"){
                coordinateArray = convertToEPSG25832(coordinateArray, coordSysElement.value)
            }
            console.log(coordinateArray)
            console.log(data["features"][0]["geometry"]["coordinates"])
            result = updateCoordinateFile(kartAIcoords)
    updateCoordinateFile(kartAIcoords).then(function(result){
        console.log(result)
        if(result.error_message == "Your chosen coordinates do not overlap with the disclosed areas, please choose a different area or data source"){
            let element = document.getElementById("error-message")
            element.innerHTML = result.error_message
            element.removeAttribute("hidden");
            console.log("Test1")
            document.getElementById("nextButton").disabled = true;
        }else{
            document.getElementById("error-message").setAttribute("hidden", true)
            document.getElementById("nextButton").disabled = false;
        }
    })
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
}

if(localStorage.getItem("Coordinates")){
    tempCoordinateArrayStrings = localStorage.getItem("Coordinates").split(",")
    tempCoordinateArray = []
    for(i = 0; i < tempCoordinateArrayStrings.length; i++){
       tempCoordinateArray.push(parseFloat(tempCoordinateArrayStrings[i]))
    }
    finalCoordinateArray = []
    for(i = 0; i < tempCoordinateArray.length; i += 2){
        finalCoordinateArray.push([tempCoordinateArray[i], tempCoordinateArray[i+1]])
    }
    console.log(finalCoordinateArray)
    drawCoordinatesOnMap(finalCoordinateArray, color="#FF0000");
    var nextBtn = document.getElementById('nextBtn');
        nextBtn.disabled = false;
  }


// Event listener for the "Next" button click action
document.getElementById('nextBtn').addEventListener('click', function () {
    // Check if the "Next" button is disabled and display an error message if so
    if (this.disabled) {
        document.getElementById('fileUploadError').style.display = 'block';
    } else {
    // Continue to next step if the button is enabled
    }
});

// Converts coordinates from any supported EPSG system to EPSG:25832.
function convertToEPSG25832(coordsArray, originalEPSG) {
    // Add definitions for the target projection system.
      proj4.defs("EPSG:25832", "+proj=utm +zone=32 +ellps=GRS80 +units=m +no_defs");
      proj4.defs("EPSG:4326", "+proj=longlat +datum=WGS84 +no_defs");
      // Additional projection definitions can be added here for other EPSG codes as needed.
    
      // Convert each coordinate in the array from the original EPSG system to EPSG:25832.
      return coordsArray.map((coord) => {
        const [longitude, latitude] = coord;
        const [x, y] = proj4(originalEPSG, "EPSG:25832", [longitude, latitude]);
        return [x, y]; // Return the converted coordinate pair.
      });
    }

    // Asynchronously updates the server with the new coordinates.
    async function updateCoordinateFile(coordinates) {
      // Make a POST request to the server endpoint designated for updating the coordinate file.
      const response = await fetch("/updateCoordinateFile", {
        method: "POST",
        headers: {
          "Content-Type": "application/json", 
        },
        body: JSON.stringify({ input: coordinates }), // Send the coordinates as JSON.
      });
    
      // Await the JSON response from the server, which could include confirmation or result data.
      const data = await response.json();
      return data; // Return the server's response data.
    }

    // Map reseizes with the window
    window.addEventListener('resize', function() {
        map.invalidateSize();  // This Leaflet method helps to ensure the map sizes itself correctly after the container size changes
    });
    