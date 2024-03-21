window.onload = () => {
  const inputCoordinates = document.getElementById("coordinates-input");
  const doneButton = document.getElementById("done-button");
  const coordSys = document.getElementById("coordSys"); // Get the coordSys element

  doneButton.addEventListener("click", async () => {
    const coordSysValue = coordSys.value; // Get the selected EPSG value
    if (coordSysValue === "Choose coordinatesystem") {
      alert("Please choose a coordinatesystem before proceeding.");
      return;
    }

    let coordinateArray = parseCoordinates(
      inputCoordinates.value,
      coordSysValue
    );
    if (coordSysValue != "EPSG:25832") {
      coordinateArray = convertToEPSG25832(coordinateArray, coordSysValue);
    }
    drawCoordinatesOnMap(coordinateArray)
    console.log("Coordinates that will be pushed:" + coordinateArray);
    // Enable the next button
    enableNextButton();
    // Send the coordinates to the server
    updateCoordinateFile(coordinateArray);
  });
};

function drawCoordinatesOnMap(coordinates) {
  proj4.defs("EPSG:25832", "+proj=utm +zone=32 +ellps=GRS80 +units=m +no_defs");
  proj4.defs("EPSG:4326", "+proj=longlat +datum=WGS84 +no_defs");


  let coordsArray = []
  for (let i = 0; i < coordinates.length; i += 2) {
    const latLng = L.latLng(parseFloat(coordinates[i][0]), parseFloat(coordinates[i][1]));
    coordsArray.push(latLng);
  }


  let convertedCoordsArray;
  convertedCoordsArray = coordsArray.map(coord => {
    const [y, x] = proj4("EPSG:25832", "EPSG:3857", [coord.lat, coord.lng]);
    return [y, x];
  });
  const polygon = L.polygon(convertedCoordsArray, { color: "red" }).addTo(map);
  map.fitBounds(polygon.getBounds());
}

function parseCoordinates(coordinates) {
  //If the coordiantes are input as points [x,y], [x,y] for example, we need to make it convert it
  if (coordinates[0] == "[") {
    // Remove the square brackets and split the string into pairs of coordinates
    let pairs = coordinates.slice(1, -1).split("], [");

    // Initialize an array to store the result
    let resultString = "";

    // Iterate over each pair of coordinates
    pairs.forEach((pair, index) => {
      // Split the pair into individual coordinates
      let coordinates = pair.split(", ");

      // Convert coordinates to string and add to the result string
      resultString += coordinates.join(",");

      // Add a comma if it's not the last pair
      if (index !== pairs.length - 1) {
        resultString += ",";
      }
    });

    coordinates = resultString;
  }

  // Get the input value and split it by commas
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

// Function to convert coordinates from EPSG:4326 to EPSG:3857
function convertToEPSG4326(coordsArray, originalEPSG) {
  //Add custom projections to proj4 for other EPSGs
  proj4.defs(
    "EPSG:25832",
    "+proj=utm +zone=32 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs +type=crs"
  );
  proj4.defs("EPSG:5972", "+proj=utm +zone=33 +ellps=WGS84 +units=m +no_defs");

  return coordsArray.map((coord) => {
    const [longitude, latitude] = coord;
    const [x, y] = proj4(originalEPSG, "EPSG:3857", [longitude, latitude]);
    return [x, y];
  });
}

// Function to convert coordinates from EPSG:4326 to EPSG:3857
function convertToEPSG25832(coordsArray, originalEPSG) {
  //Add custom projections to proj4 for other EPSGs
  proj4.defs(
    "EPSG:25832",
    "+proj=utm +zone=32 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs +type=crs"
  );
  proj4.defs("EPSG:5972", "+proj=utm +zone=33 +ellps=WGS84 +units=m +no_defs");

  return coordsArray.map((coord) => {
    const [longitude, latitude] = coord;
    const [x, y] = proj4(originalEPSG, "EPSG:25832", [longitude, latitude]);
    return [x, y];
  });
}

async function updateCoordinateFile(coordinates) {
  //Make a POST Request to the server
  const response = await fetch("/updateCoordinateFile", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ input: coordinates }),
  });

  const data = await response.json();
  return data;
}

function enableNextButton() {
  const nextButton = document.getElementById("next-button");
  nextButton.disabled = false;
}
