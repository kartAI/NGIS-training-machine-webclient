// Map initialization
var map = L.map('map', { crs: L.CRS.EPSG3857 }).setView([58.151833, 8.004227], 14); // Set the map view to a specific location and zoom level (Note, this is ESPG 3857)

// OpenStreetMap Tiles
var osm = L.tileLayer('https://api.maptiler.com/maps/openstreetmap/{z}/{x}/{y}.jpg?key=gBHYqk3cSCXUdQqICyH3', {
    attribution: '<a href=" https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a><a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>'
}).addTo(map); // Add the OpenStreetMap layer to the map

// Search function for Leaflet
L.Control.geocoder().addTo(map);

// FeatureGroup to store drawn lines on the map
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
        remove: true
    }
});

map.addControl(drawControl); // Add the draw control to the map

// Array to store the corner circles of the rectangle, useful to see rectangle if zoomed out
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
        // Define the size of the circles
        corners.forEach(function (corner, index) {
            var circle = L.circle(corner, { radius: 5 }).addTo(map); // Radius can be changed to make the circle bigger or smaller

            // Add tooltip to the circle to display coordinate point
            var labelText = (index === 0 || index === 4) ? "P1,P5" : "P" + (index + 1);
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

    // Create a new array 
    var uniqueCoordsArray = []; // Array to store unique coordinates
    var coordsMap = new Map(); // Map to store unique coordinates
    for (var i = 0; i < coordsArray.length; i++) { // Loop through the coordinates
        var key = coordsArray[i].join(','); // Create a key for the map
        if (!coordsMap.has(key)) { // Check if the map contains the key
            uniqueCoordsArray.push(coordsArray[i]); // Add the coordinate to the array
            coordsMap.set(key, true); // Set the key in the map
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

    kartAIcoords4326 = uniqueCoordsArray; // KartAI coordinates in EPSG:4326, used for conversion

    // EPSG:4326 to EPSG:25832 conversion defined in proj4
    proj4.defs("EPSG:25832","+proj=utm +zone=32 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs +type=crs");

    // Define the source (EPSG:4326) and destination (EPSG:3857) projections
    const epsg4326 = 'EPSG:4326'; 
    const epsg3857 = 'EPSG:3857'; // Default EPSG for Leaflet
    const epsg25832 = 'EPSG:25832'; // Default EPSG for this project

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
    
    console.log(kartAIcoords); // Log the converted coordinates for debugging

    // Update the HTML element with the converted coordinates
    coordinatesElement.innerHTML = coordinatesString;
    updateCoordinateFile(kartAIcoords);
});


// Updates the coordinates on the server for wms.
async function updateCoordinateFile(coordinates) {
    //Make a POST Request to the server
    const response = await fetch('/updateCoordinateFile', { // Send the coordinates to the server
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', 
        },
        body: JSON.stringify({"input": coordinates}), // Send the coordinates as JSON
    });

    const data = await response.json(); 
    return data; // Return the server's response data
}

const geoJSONData = {
    "type": "FeatureCollection",
    "name": "leafletHighlight",
    "crs": {
      "type": "name",
      "properties": {
        "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
      }
    },
    "features": [
      {
        "type": "Feature",
        "properties": {
          "id": 0
        },
        "geometry": {
          "type": "MultiPolygon",
          "coordinates": [
            [
              [
                [58.161162677136666, 8.08024462074493],
                [58.163088906459535, 8.065464745712365],
                [58.16125440470738, 8.060827922172738],
                [58.1559643950546, 8.054220448628769],
                [58.15394603382506, 8.052655520684144],
                [58.148410243600964, 8.052133878035935],
                [58.14376073804149, 8.052771441272633],
                [58.142567674904754, 8.053872686863293],
                [58.141588721445665, 8.053872686863293],
                [58.140242616490056, 8.058161748637454],
                [58.14018142869202, 8.062218969234628],
                [58.14207820153972, 8.065348825123877],
                [58.14446432063769, 8.07392694867219],
                [58.1445255010759, 8.076129439853512],
                [58.149480767422986, 8.077752328092382],
                [58.15278389512783, 8.084243881047861],
                [58.1559643950546, 8.086214531052203],
                [58.15694295323303, 8.086794133994657],
                [58.161162677136666, 8.08024462074493]
              ]
            ]
          ]
        }
      }
    ]
  }

// Define a style for the GeoJSON layer
    var geoJsonLayerStyle = {
        color: "#cd32cd", // Orange line color
        weight: 20,        // Line thickness
        opacity: 0.65     // Line opacity
    };

    // Add the GeoJSON layer with the defined style
    L.geoJSON(geoJSONData, { 
        style: geoJsonLayerStyle,
        onEachFeature: function(feature, layer) {
            if (feature.properties && feature.properties.popupContent) {
                layer.bindPopup(feature.properties.popupContent);
            }
        }
    }).addTo(map); // Add the GeoJSON layer to the map

// Save, convert, draw on map
function saveCoordinates() { // Function to save the coordinates entered by the user
    var coordinatesInput = document.getElementById("coordi").value; // Get the coordinates entered by the user
    console.log("coordinatesInput:", coordinatesInput); // Log 
    var coordinatesArray = coordinatesInput.split(","); // Split the coordinates into an array
    console.log("coordinatesArray:", coordinatesArray); // Log 
    var latLngArray = []; // Store the latLng objects
    for (var i = 0; i < coordinatesArray.length; i += 2) { // Loop through the coordinates
        var latLng = L.latLng(parseFloat(coordinatesArray[i]), parseFloat(coordinatesArray[i + 1])); // Create a latLng object
        latLngArray.push(latLng); // Add the latLng object to the array
    }
    console.log("latLngArray:", latLngArray); // Log 
    var polygon = L.polygon(latLngArray, { color: "red" }).addTo(map); // Draw a red polygon on the map
    map.fitBounds(polygon.getBounds()); // Fit the map to the polygon
}


// The function disables the scroll wheel zoom on the map.
function noScroll() { 
    map.scrollWheelZoom.disable();
}
