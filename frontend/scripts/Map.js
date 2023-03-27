//map initialization
var map = L.map('map', {crs: L.CRS.EPSG3857}).setView([58.146513160381325, 7.99581527709961], 14);

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
        polyline: true,
        polygon: true,
        rectangle: true,
        circle: true,
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
    return [coord.lat, coord.lng];
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

// convert the unique coordinates back to Leaflet LatLng objects
var uniqueCoords = uniqueCoordsArray.map(function(coord) {
    return L.latLng(coord[0], coord[1]);
});

// update the HTML element with the unique coordinates
var coordinatesElement = document.getElementById("coordinates");
var coordinatesString = "";
for (var i = 0; i < uniqueCoords.length; i++) {
    coordinatesString += "<b>P" + (i+1) + ": </b>" + uniqueCoords[i].lat + ", " + uniqueCoords[i].lng + "<br>";
}

coordinatesElement.innerHTML = coordinatesString;


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

function noScroll() {
    map.scrollWheelZoom.disable();
};