import { convertToEPSG25832, disableNextButton,enableNextButton, drawCoordinatesOnMap, updateCoordinateFile, checkPreLoadedCoordinates } from "./helper.js";
// This script is designed to interact with a web page for handling geographical coordinates.
// It includes functionality for parsing, converting, and displaying coordinates on a map.

var map = L.map("map", { crs: L.CRS.EPSG3857 }).setView(
  [58.151833, 8.004227],
  14
); // Set the map view to a specific location and zoom level (Note, this is ESPG 3857)

// OpenStreetMap Tiles
var osm = L.tileLayer(
  "https://api.maptiler.com/maps/openstreetmap/{z}/{x}/{y}.jpg?key=gBHYqk3cSCXUdQqICyH3",
  {
    attribution:
      '<a href=" https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a><a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
  }
).addTo(map); // Add the OpenStreetMap layer to the map


// Set up an event listener for when the window finishes loading.
window.onload = () => {
  // Access elements from the document using their ID to interact with the UI.
  const inputCoordinates = document.getElementById("coordinates-input"); // Input field for user to enter coordinates.
  const doneButton = document.getElementById("done-button"); // Button for user to indicate completion of coordinate input.
  const coordSys = document.getElementById("coordSys"); // Dropdown for selecting the coordinate system.
 
  checkPreLoadedCoordinates(map)
 
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
    drawCoordinatesOnMap(coordinateArray, "#FF0000", map);

    // Send the updated coordinates to the server for processing or storage.
    updateCoordinateFile(coordinateArray, "application/json").then(function(result){
        console.log(result)
        if(result.error_message == "Your chosen coordinates do not overlap with the disclosed areas, please choose a different area or data source"){
            let element = document.getElementById("error-message")
            element.innerHTML = result.error_message
            element.removeAttribute("hidden");
            disableNextButton()
          }else{
            document.getElementById("error-message").setAttribute("hidden", true)
            enableNextButton()
        }
    })
  });
};

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

// The function disables the scroll wheel zoom on the map.
function noScroll() {
  map.scrollWheelZoom.disable();
}