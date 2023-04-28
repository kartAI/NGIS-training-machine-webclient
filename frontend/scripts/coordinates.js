function logSelectedEpsg() {
  const coordSys = document.getElementById("coordSys");
  if (coordSys.value !== "Choose coordinatesystem") {
    console.log("Selected EPSG:", coordSys.value);
  }
}

window.onload = () => {
  const input = document.getElementById("coordinates-input");
  const doneButton = document.getElementById("done-button");
  const coordSys = document.getElementById("coordSys"); // Get the coordSys element
  // Define the projections
  const epsg3857 = 'EPSG:3857';

  const coordsArray = [];

  // Add event listener to coordSys select element
  coordSys.addEventListener("change", () => {
    console.log("coordSys change event triggered"); // Add this line to check if the event is being triggered

    if (coordSys.value !== "Choose coordinatesystem") {
      console.log("Selected EPSG:", coordSys.value); // Log the selected EPSG
    }
  });
  doneButton.addEventListener("click", async () => {
    const coordSysValue = coordSys.value; // Get the selected EPSG value
    if (coordSysValue === "Choose coordinatesystem") {
      alert("Please choose a coordinatesystem before proceeding.");
      return;
    }

    //Example of code for adding more EPSG
    if (coordSysValue === 'EPSG:5972') {
      proj4.defs(coordSysValue, '+proj=utm +zone=33 +ellps=WGS84 +units=m +no_defs');
    }
    
    // Get the input value and split it by commas
    const inputCoordinates = input.value.split(",");

    // Loop through the inputCoordinates and create objects
    for (let i = 0; i < inputCoordinates.length; i += 2) {
      const latLng = L.latLng(parseFloat(inputCoordinates[i + 1]), parseFloat(inputCoordinates[i]));
      coordsArray.push(latLng);
    }

    console.log("coordsArray:", coordsArray);

    // Check if the selected coordinate system is not EPSG:4326, then convert the coordinates to EPSG:3857
    let convertedCoordsArray;
    if (coordSysValue != 'EPSG:4326') {
      convertedCoordsArray = coordsArray.map(coord => {
        const [y, x] = proj4(coordSysValue, epsg3857, [coord.lat, coord.lng]);
        return [y, x];
      });
    } else {
      convertedCoordsArray = coordsArray;
    }

    console.log(convertedCoordsArray);

    // Create a polygon from the convertedCoordsArray and add it to the map
    const polygon = L.polygon(convertedCoordsArray, { color: "red" }).addTo(map);
    map.fitBounds(polygon.getBounds());

    // Send the coordinates to the server
    updateCoordinates(convertedCoordsArray);

    // Enable the next button
    enableNextButton();

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
}

function enableNextButton() {
  const nextButton = document.getElementById("next-button");
  nextButton.disabled = false;
}
