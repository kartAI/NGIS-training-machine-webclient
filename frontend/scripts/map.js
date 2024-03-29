// Map initialization
var map = L.map('map', { crs: L.CRS.EPSG3857 }).setView([58.151833, 8.004227], 14);

// Add OpenStreetMap Tiles
var osm = L.tileLayer('https://api.maptiler.com/maps/openstreetmap/{z}/{x}/{y}.jpg?key=gBHYqk3cSCXUdQqICyH3', {
    attribution: '<a href=" https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a><a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>'
}).addTo(map);

// Søkefunksjon til leaflet maps
L.Control.geocoder().addTo(map);

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
        edit: false,
        remove: true
    }
});

map.addControl(drawControl);

var cornerCircles = [];

// Binds listener to the event:created
map.on("draw:created", function (c) {

    // Enable the next button
    document.getElementById("nextButton").disabled = false;

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
            bounds.getSouthWest()
        ];
//defining the size of the circles
        corners.forEach(function (corner, index) {
            var circle = L.circle(corner, { radius: 5 }).addTo(map);

            // Add tooltip to the circle to display coordinate point
            var labelText = (index === 0 || index === 4) ? "P1,P5" : "P" + (index + 1);
            circle.bindTooltip(labelText);
            

            
            circle.openTooltip();
        setTimeout(function () {
            circle.closeTooltip();
        }, 3000);
        cornerCircles.push(circle); //stores the circle reference inside the array

            
        });
    }

    if (drawControl.options.draw.remove) {
        // Bind click event to the drawn shape for removal
        layer.on('click', function () {
            drawnItems.removeLayer(layer);
            // Remove corner circles when rectangle is removed
            cornerCircles.forEach(function (circle) {
                map.removeLayer(circle);
            });
            // Clear the array
            
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

    //We need to add the new projection to the project
    proj4.defs("EPSG:25832","+proj=utm +zone=32 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs +type=crs");

    // Define the source (EPSG:4326) and destination (EPSG:3857) projections
    const epsg4326 = 'EPSG:4326';
    const epsg3857 = 'EPSG:3857';
    const epsg25832 = 'EPSG:25832';

    // Function to convert coordinates from EPSG:4326 to EPSG:3857
    function convertToEPSG3857(coordsArray) {
        return coordsArray.map(coord => {
            const [longitude, latitude] = coord;
            const [x, y] = proj4(epsg4326, epsg25832, [longitude, latitude]);
            return [x, y];
        });
    }

    // Convert the coordinates and store them in a new array
    const kartAIcoords = convertToEPSG3857(kartAIcoords4326);

    console.log(kartAIcoords);

    coordinatesElement.innerHTML = coordinatesString;
    updateCoordinateFile(kartAIcoords);


});


// Updates the coordinates on the server for wms.
async function updateCoordinateFile(coordinates) {
    //Make a POST Request to the server
    const response = await fetch('/updateCoordinateFile', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({"input": coordinates}),
    });

    const data = await response.json();
    return data;
}

// Updates the coordinates on the server.
async function updateCoordinates(coordinates) {
    const response = await fetch('http://localhost:8000/update_coordinates', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({"input": coordinates}),
    });

    const data = await response.json();
    return data;
}

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



// The function disables the scroll wheel zoom on the map.
function noScroll() {
    map.scrollWheelZoom.disable();
}


window.onload = () => {
    setup_folders()
  }
  
  async function setup_folders(){
    const response = await fetch('/setupUserSessionFolders', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
  
    const data = await response.json();
    return data;
  }