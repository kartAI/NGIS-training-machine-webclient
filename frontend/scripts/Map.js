// Map initialization
var map = L.map('map', { crs: L.CRS.EPSG3857 }).setView([59.887537, 10.523083], 14);

// Add OpenStreetMap Tiles
var osm = L.tileLayer('https://api.maptiler.com/maps/openstreetmap/{z}/{x}/{y}.jpg?key=gBHYqk3cSCXUdQqICyH3', {
    attribution: '<a href=" https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a><a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>'
}).addTo(map);

// Leaflet draw
var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);


// Specifies controls to be displayed
var drawControl = new L.Control.Draw({
    draw: {
        polyline: false,
        polygon: true,
        rectangle: true,
        circle: false,
        marker: false,
        edit: false
    }
});

map.addControl(drawControl);

// Binds listener to the event:created
map.on("draw:created", function (c) {

    // Enable the next button
    document.getElementById("nextButton").disabled = false;

    // Retrieves drawn shape
    var layer = c.layer;

    // Adds shape to layergroup: drawnItems
    drawnItems.addLayer(layer);
    noScroll();

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

    // Create a new array with unique coordinates
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


    // Convert the unique coordinates back to Leaflet LatLng objects
    var uniqueCoords = uniqueCoordsArray.map(function (coord) {
        return L.latLng(coord[0], coord[1]);
    });

    // Update the HTML element with the unique coordinates
    var coordinatesElement = document.getElementById("coordinates");
    var coordinatesString = "";
    for (var i = 0; i < uniqueCoords.length; i++) {
        var point = L.CRS.EPSG4326.project(uniqueCoords[i]);
        coordinatesString += "<b>P" + (i + 1) + ": </b>" + uniqueCoords[i].lat + ", " + uniqueCoords[i].lng + "<br>";
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

// Function saves coordinates entered by the user, converts them to latLng objects, and draws a red polygon on the map.
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

// Updates the coordinates on the server.
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

// The function disables the scroll wheel zoom on the map.
function noScroll() {
    map.scrollWheelZoom.disable();
}
