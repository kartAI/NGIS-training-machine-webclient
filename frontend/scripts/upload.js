import {
  convertToEPSG25832,
  disableNextButton,
  enableNextButton,
  drawCoordinatesOnMap,
  updateCoordinateFile,
} from "./helper.js";

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

function uploadFile() {
  coordSysElement = document.getElementById("coordSys");
  fileElement = document.getElementById("file-input");

  if (coordSysElement.value === "None") {
    alert("Please choose a coordinate system!");
    return;
  }

  if (!fileElement.files[0]) {
    alert("Please add a file!");
    return;
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
        },
      });
      // Add the processed layer to the map and adjust the map's view accordingly
      geojsonLayer.addTo(map);
      map.fitBounds(geojsonLayer.getBounds());

      let coordinateArray = data["features"][0]["geometry"]["coordinates"][0];
      if (coordSysElement.value != "EPSG:25832") {
        coordinateArray = convertToEPSG25832(
          coordinateArray,
          coordSysElement.value
        );
      }
      updateCoordinateFile(coordinateArray, "application/json").then(function (
        result
      ) {
        if (
          result.error_message ==
          "Your chosen coordinates do not overlap with the disclosed areas, please choose a different area or data source"
        ) {
          let element = document.getElementById("error-message");
          element.innerHTML = result.error_message;
          element.removeAttribute("hidden");
          enableNextButton();
        } else {
          document.getElementById("error-message").setAttribute("hidden", true);
          disableNextButton();
        }
      });
    } catch (error) {
      // Alert the user in case of an error parsing the JSON file content
      alert("Error parsing the JSON file: " + error);
    }
  };

  // Function to be called when the file has finished loading
  reader.onloadend = function () {
    // Ensure the "Next" button is enabled after the file is loaded
    var nextBtn = document.getElementById("nextBtn");
    nextBtn.disabled = false;
  };

  // Start reading the file as text; suitable for JSON and GeoJSON files
  reader.readAsText(file);
}

// Map reseizes with the window
window.addEventListener("resize", function () {
  map.invalidateSize(); // This Leaflet method helps to ensure the map sizes itself correctly after the container size changes
});

// The function disables the scroll wheel zoom on the map.
function noScroll() {
  map.scrollWheelZoom.disable();
}
