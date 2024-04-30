//Helper functions that are used in other scripts


// Asynchronously updates the server with the new coordinates.
async function updateCoordinateFile(coordinates, contentType) {
  // Make a POST request to the server endpoint designated for updating the coordinate file.
  const response = await fetch("/updateCoordinateFile", {
    method: "POST",
    headers: {
      "Content-Type": contentType,
    },
    body: JSON.stringify({ input: coordinates }), // Send the coordinates as JSON.
  });

  // Await the JSON response from the server, which could include confirmation or result data.
  const data = await response.json();
  return data; // Return the server's response data.
}

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
// Enables the "Next" button in the UI, typically after a successful operation.
function enableNextButton() {
  // Access the "Next" button using its document ID.
  const nextButton = document.getElementById("nextButton");
  // Enable the button by setting its `disabled` property to false.
  nextButton.disabled = false;
}

//Disables the "Next button in the UI"
function disableNextButton() {
  // Access the "Next" button using its document ID.
  const nextButton = document.getElementById("nextButton");
  // Disable the button by setting its `disabled` property to true.
  nextButton.disabled = true;
}

// Function to display given coordinates on a map by drawing a polygon.
function drawCoordinatesOnMap(coordinates, color = "#cd32cd", map) {
  // Define projections for converting between coordinate systems using proj4.
  proj4.defs("EPSG:25832", "+proj=utm +zone=32 +ellps=GRS80 +units=m +no_defs");
  proj4.defs("EPSG:4326", "+proj=longlat +datum=WGS84 +no_defs");

  // Convert the coordinates from EPSG:25832 to EPSG:4326 (a common format for web maps).
  var coordinates4326 = coordinates.map((coord) =>
    proj4("EPSG:25832", "EPSG:4326", coord)
  );

  let correctedPairs = [];
  // Correct the order of coordinates for compatibility with the mapping library.
  for (let i = 0; i < coordinates4326.length; i++) {
    correctedPairs.push([coordinates4326[i][1], coordinates4326[i][0]]);
  }
  // Use Leaflet to draw a polygon on the map using the converted and corrected coordinates.
  const polygon = L.polygon(correctedPairs, { color: "red" }).addTo(map);
  polygon.setStyle({ fillColor: "#ffffff" });
  polygon.setStyle({ color: color });
  polygon.setStyle({ opacity: 0.65 });
  // Adjust the map view to fit the bounds of the polygon.
  map.fitBounds(polygon.getBounds());
}

function checkPreLoadedCoordinates(map) {
  if (localStorage.getItem("Coordinates")) {
    let tempCoordinateArrayStrings = localStorage.getItem("Coordinates").split(",");
    let tempCoordinateArray = [];
    for (let i = 0; i < tempCoordinateArrayStrings.length; i++) {
      tempCoordinateArray.push(parseFloat(tempCoordinateArrayStrings[i]));
    }
    let finalCoordinateArray = [];
    for (let i = 0; i < tempCoordinateArray.length; i += 2) {
      finalCoordinateArray.push([
        tempCoordinateArray[i],
        tempCoordinateArray[i + 1],
      ]);
    }
    let color ="#FF0000"
    console.log(finalCoordinateArray);
    drawCoordinatesOnMap(finalCoordinateArray, color, map);
    enableNextButton()
  }
}

export {
  updateCoordinateFile,
  convertToEPSG25832,
  enableNextButton,
  disableNextButton,
  drawCoordinatesOnMap,
  checkPreLoadedCoordinates,
};
