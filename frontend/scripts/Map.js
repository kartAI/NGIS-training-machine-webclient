//map initialization
var map = L.map('map', {crs: L.CRS.EPSG3857}).setView([59.887537, 10.523083], 14);

//Add OpenStreetMap Tiles
var osm = L.tileLayer('https://api.maptiler.com/maps/openstreetmap/{z}/{x}/{y}.jpg?key=gBHYqk3cSCXUdQqICyH3', {
    attribution: '<a href=" https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a><a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>'
}).addTo(map);

//leaflet draw
var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);


//adds drawcontrols
var drawControl = new L.Control.Draw({
    draw: {
        polyline: false,
        polygon: true,
        rectangle: true,
        circle: false,
        marker: false
    },
    edit: {
        featureGroup: drawnItems,
        remove: false
    }
});

map.addControl(drawControl);

//binds listener to the event:created
map.on("draw:created", function (c) {
    //retrieves the type of a shape drawn and sets the inner HTML of an element to display that type.
    document.getElementById("shapeType").innerHTML = c.layerType;
    
    //retrieves drawn shape
    var layer = c.layer;
    //adds shape to layergroup: drawnItems
    drawnItems.addLayer(layer);
    noScroll();
    //retrieves the coordinates of the shape
    var coords;
    if (layer instanceof L.Polygon) {
        //retrieves all the coordinates of the polygon
        coords = layer.getLatLngs();
    } else if (layer instanceof L.Rectangle) {
        //retrieves the bounding box of the rectangle
        coords = layer.getBounds();
    }
    

// convert the coordinates to an array
var coordsArray = coords[0].map(function(coord) {
    return [coord.lng, coord.lat];
});

// create a new array with unique coordinates
var uniqueCoordsArray = [];
var coordsMap = new Map();
for (var i = 0; i < coordsArray.length; i++) {
    var key = coordsArray[i].join(',');
    if (!coordsMap.has(key)) {
        uniqueCoordsArray.push(coordsArray[i]); 
        coordsMap.set(key, true);
    }
}

// Add the first coordinate again at the end of the array
uniqueCoordsArray.push(uniqueCoordsArray[0]);

// Print the uniqueCoordsArray to console
console.log(uniqueCoordsArray);

// convert the unique coordinates back to Leaflet LatLng objects
var uniqueCoords = uniqueCoordsArray.map(function(coord) {
    return L.latLng(coord[0], coord[1]);
});

// update the HTML element with the unique coordinates
var coordinatesElement = document.getElementById("coordinates");
var coordinatesString = "";
for (var i = 0; i < uniqueCoords.length; i++) {
    var point = L.CRS.EPSG4326.project(uniqueCoords[i]);
    coordinatesString += "<b>P" + (i+1) + ": </b>" + uniqueCoords[i].lat + ", " + uniqueCoords[i].lng + "<br>";
}

kartAIcoords4326 = uniqueCoordsArray;

// Define the source (EPSG:4326) and destination (EPSG:3857) projections
const epsg4326 = 'EPSG:4326';
const epsg3857 = 'EPSG:3857';

// Function to convert coordinates from EPSG:4326 to EPSG:3857
function convertToEPSG3857(coordsArray) {
  return coordsArray.map(coord => {
    const [longitude, latitude] = coord;
    const [x, y] = proj4(epsg4326, epsg3857, [longitude, latitude]);
    return [x, y];
  });
}

// Convert the coordinates and store them in a new array
const kartAIcoords = convertToEPSG3857(kartAIcoords4326);

console.log(kartAIcoords);

coordinatesElement.innerHTML = coordinatesString;
updateCoordinates(kartAIcoords);


});

function saveCoordinates() {
    var coordinatesInput = document.getElementById("coordi").value;
    console.log("coordinatesInput:", coordinatesInput);
    var coordinatesArray = coordinatesInput.split(",");
    console.log("coordinatesArray:", coordinatesArray);
    var latLngArray = [];
    for (var i = 0; i < coordinatesArray.length; i += 2) {
        var latLng = L.latLng(parseFloat(coordinatesArray[i]), parseFloat(coordinatesArray[i + 1]));
        latLngArray.push(latLng);
    }
    console.log("latLngArray:", latLngArray);
    var polygon = L.polygon(latLngArray, { color: "red" }).addTo(map);
    map.fitBounds(polygon.getBounds());
}

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
  

function noScroll() {
    map.scrollWheelZoom.disable();
};