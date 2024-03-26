// This script is designed to interact with a web page for handling geographical coordinates.
// It includes functionality for parsing, converting, and displaying coordinates on a map.

// Set up an event listener for when the window finishes loading.
window.onload = () => {
  // Access elements from the document using their ID to interact with the UI.
  const inputCoordinates = document.getElementById("coordinates-input"); // Input field for user to enter coordinates.
  const doneButton = document.getElementById("done-button"); // Button for user to indicate completion of coordinate input.
  const coordSys = document.getElementById("coordSys"); // Dropdown for selecting the coordinate system.

  // Add an event listener to the "Done" button for when it is clicked.
  doneButton.addEventListener("click", async () => {
    const coordSysValue = coordSys.value; // Retrieve the value of the selected coordinate system.

    // Check if the user has selected a coordinate system before proceeding.
    if (coordSysValue === "Choose coordinatesystem") {
      alert("Please choose a coordinatesystem before proceeding.");
      return; // Exit the function early if no coordinate system is selected.
    }

    // Parse the input coordinates based on the selected coordinate system.
    let coordinateArray = parseCoordinates(inputCoordinates.value, coordSysValue);

    // If the selected system is not EPSG:25832, convert the coordinates to EPSG:25832.
    if (coordSysValue != "EPSG:25832") {
      coordinateArray = convertToEPSG25832(coordinateArray, coordSysValue);
    }

    // Display the coordinates on a map.
    drawCoordinatesOnMap(coordinateArray);
    console.log("Coordinates that will be pushed:" + coordinateArray);

    // Enable the next button in the UI, typically allowing the user to proceed with the next action.
    enableNextButton();

    // Send the updated coordinates to the server for processing or storage.
    updateCoordinateFile(coordinateArray);
  });
};

// Function to display given coordinates on a map by drawing a polygon.
function drawCoordinatesOnMap(coordinates) {
  // Define projections for converting between coordinate systems using proj4.
    proj4.defs("EPSG:25832", "+proj=utm +zone=32 +ellps=GRS80 +units=m +no_defs");
    proj4.defs("EPSG:4326", "+proj=longlat +datum=WGS84 +no_defs");

  // Convert the coordinates from EPSG:25832 to EPSG:4326 (a common format for web maps).
  var coordinates4326 = coordinates.map((coord) =>
    proj4("EPSG:25832", "EPSG:4326", coord)
  );

  let correctedPairs = [];
  // Correct the order of coordinates for compatibility with the mapping library.
  for(let i = 0; i < coordinates4326.length; i++){
    correctedPairs.push([coordinates4326[i][1], coordinates4326[i][0]]);
  }

  // Use Leaflet to draw a polygon on the map using the converted and corrected coordinates.
  const polygon = L.polygon(correctedPairs, { color: "red" }).addTo(map);
  // Adjust the map view to fit the bounds of the polygon.
  map.fitBounds(polygon.getBounds());
}

// Function to parse input coordinates from a string to an array of coordinate pairs.
function parseCoordinates(coordinates) {
  // Check if the input format is an array of coordinates in string format.
  if (coordinates[0] == "[") {
    // Process the string to separate individual coordinate pairs.
    let pairs = coordinates.slice(1, -1).split("], [");

    let resultString = "";
    pairs.forEach((pair, index) => {
      let coords = pair.split(", ");
      resultString += coords.join(",");
      if (index !== pairs.length - 1) {
        resultString += ",";
      }
    });
    coordinates = resultString;
  }

  // Convert the string of coordinates into an array of numeric coordinate pairs.
  let inputCoordinates = coordinates.split(",");
  let coordsArray = [];
  for (let i = 0; i < inputCoordinates.length; i += 2) {
    let coord = [
      parseFloat(inputCoordinates[i]),
      parseFloat(inputCoordinates[i + 1]),
    ];
    coordsArray.push(coord);
  }

  return coordsArray;
}


// Converts coordinates from any supported EPSG system to EPSG:25832.
function convertToEPSG25832(coordsArray, originalEPSG) {
  // Add definitions for the target projection system.
  proj4.defs(
    "EPSG:25832",
    "+proj=utm +zone=32 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs +type=crs"
    );
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
  
  // Enables the "Next" button in the UI, typically after a successful operation.
  function enableNextButton() {
    // Access the "Next" button using its document ID.
    const nextButton = document.getElementById("next-button");
    // Enable the button by setting its `disabled` property to false.
    nextButton.disabled = false;
  }
  