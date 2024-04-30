import {
  convertToEPSG25832,
  disableNextButton,
  enableNextButton,
  drawCoordinatesOnMap,
  updateCoordinateFile,
  checkPreLoadedCoordinates,
} from "./helper.js";

// Map initialization
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

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map); // Add the scalebar layer to the map

// Search function for Leaflet
L.Control.geocoder().addTo(map);

//Scalebar function for leaflet
var scalebar = new L.control.scale({
  imperial: false,
  metric: true,
}).addTo(map);

var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems); // Add the FeatureGroup to the map

// Specifies controls to be displayed
var drawControl = new L.Control.Draw({
  draw: {
    polyline: false,
    polygon: true,
    rectangle: true,
    circle: false,
    marker: false,
    edit: false,
    remove: true,
  },
});

map.addControl(drawControl); // Add the draw control to the map

// Array to store the corner circles of the rectangle, useful to see rectangle if zoomed out
var cornerCircles = [];

// Binds listener to the event:created
map.on("draw:created", function (c) {
  //If there are objects that are drawn on the map already we remove them
  map.eachLayer(function (layer) {
    //Check to see the layer is of the correct type
    if (layer instanceof L.Polygon || layer instanceof L.Circle) {
      map.removeLayer(layer);
    }
  });

  // Retrieves drawn shape
  var layer = c.layer;

  // Adds shape to layergroup: drawnItems
  drawnItems.addLayer(layer);
  noScroll();

  // Add small circles at the corners of the rectangle to show the coordinate points
  if (layer instanceof L.Rectangle) {
    var bounds = layer.getBounds();
    var corners = [
      bounds.getNorthWest(),
      bounds.getNorthEast(),
      bounds.getSouthEast(),
      bounds.getSouthWest(),
    ];
    // Define the size of the circles
    corners.forEach(function (corner, index) {
      var circle = L.circle(corner, { radius: 5 }).addTo(map); // Radius can be changed to make the circle bigger or smaller

      // Add tooltip to the circle to display coordinate point
      var labelText = index === 0 || index === 4 ? "P1,P5" : "P" + (index + 1);
      circle.bindTooltip(labelText); // Add a position prediction to the corner circles

      // Close the tooltip after 3 seconds
      circle.openTooltip();
      setTimeout(function () {
        circle.closeTooltip();
      }, 3000);
      cornerCircles.push(circle); // Stores the circle reference inside the array
    });
  }
  // Remove the drawn shape when clicked
  if (drawControl.options.draw.remove) {
    // Bind click event to the drawn shape for removal
    layer.on("click", function () {
      drawnItems.removeLayer(layer);
      // Remove corner circles when rectangle is removed
      cornerCircles.forEach(function (circle) {
        map.removeLayer(circle);
      });
    });
  }

  // Retrieves the coordinates of the shape
  var coords;
  if (layer instanceof L.Polygon) {
    // Retrieves all the coordinates of the polygon
    coords = layer.getLatLngs();
  } else if (layer instanceof L.Rectangle) {
    // Retrieves the bounding box of the rectangle
    coords = layer.getBounds();
  }

  // Convert the coordinates to an array
  var coordsArray = coords[0].map(function (coord) {
    return [coord.lng, coord.lat];
  });

  // Create a new array
  var uniqueCoordsArray = []; // Array to store unique coordinates
  var coordsMap = new Map(); // Map to store unique coordinates
  for (var i = 0; i < coordsArray.length; i++) {
    // Loop through the coordinates
    var key = coordsArray[i].join(","); // Create a key for the map
    if (!coordsMap.has(key)) {
      // Check if the map contains the key
      uniqueCoordsArray.push(coordsArray[i]); // Add the coordinate to the array
      coordsMap.set(key, true); // Set the key in the map
    }
  }

  // Add the first coordinate again at the end of the array
  uniqueCoordsArray.push(uniqueCoordsArray[0]);

  // Convert the coordinates and store them in a new array
  const kartAIcoords = convertToEPSG25832(uniqueCoordsArray, "EPSG:4326");
  updateCoordinateFile(kartAIcoords, "application/json").then(function (
    result
  ) {
    console.log(result);
    if (
      result.error_message ==
      "Your chosen coordinates do not overlap with the disclosed areas, please choose a different area or data source"
    ) {
      let element = document.getElementById("error-message");
      element.innerHTML = result.error_message;
      element.removeAttribute("hidden");
      disableNextButton();
    } else {
      document.getElementById("error-message").setAttribute("hidden", true);
      enableNextButton();
    }
  });
});

//Check for preloaded coordinates in localstorage
window.onload = () => {
  if(localStorage.getItem("orto_source") == "WMS" && localStorage.getItem("label_source") == "WMS"){
    document.getElementById("disclosedAreasButton").style.visibility  = "hidden";
}
  checkPreLoadedCoordinates(map);
};

function showDisclosedAreas() {
  const geoJSONData = {
    type: "FeatureCollection",
    name: "leafletArea",
    crs: { type: "name", properties: { name: "urn:ogc:def:crs:EPSG::25832" } },
    features: [
      {
        type: "Feature",
        properties: { id: 0 },
        geometry: {
          type: "MultiPolygon",
          coordinates: [
            [
              [
                [445455.840260153403506, 6447241.938237250782549],
                [446411.136294620053377, 6446821.367656039074063],
                [446200.851004014199134, 6445709.859691408462822],
                [445696.166306560102385, 6445000.897854508832097],
                [444800.951783695199993, 6444171.772994405589998],
                [444392.397504803782795, 6444315.968622249551117],
                [443749.52533066587057, 6445295.297261357307434],
                [444512.560528007161338, 6446989.595888524316251],
                [445455.840260153403506, 6447241.938237250782549],
              ],
            ],
          ],
        },
      },
    ],
  };

  let coordinatesToDraw =
    geoJSONData["features"][0]["geometry"]["coordinates"][0][0];
  let color = "#ff0000";
  drawCoordinatesOnMap(coordinatesToDraw, color, map);
}
window.showDisclosedAreas = showDisclosedAreas;

// The function disables the scroll wheel zoom on the map.
function noScroll() {
  map.scrollWheelZoom.disable();
}
