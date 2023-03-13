//map initialization
var map = L.map('map', { crs: L.CRS.EPSG3857 }).setView([58.146513160381325, 7.99581527709961], 14);

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
map.on("draw:created", function (e) {
    //retrieves the type of a shape drawn and sets the inner HTML of an element to display that type.
    document.getElementById("shapeType").innerHTML = e.layerType;

    //retrieves drawn shape
    var layer = e.layer;

    //adds shape to layergroup: drawnItems
    drawnItems.addLayer(layer);

    //retrieves the coordinates of the shape
    var coords = layer.toGeoJSON().geometry.coordinates;

    // If the layer is a rectangle, convert the bounding box to a polygon
    if (layer instanceof L.Rectangle) {
        coords = [[            [coords[0][1], coords[0][0]],
            [coords[1][1], coords[0][0]],
            [coords[1][1], coords[1][0]],
            [coords[0][1], coords[1][0]],
            [coords[0][1], coords[0][0]]
        ]];
    }

    // log the coordinates to the console
    console.log(coords);
});

        // convert the coordinates to an array
        var coordsArray = coords[0].map(function (coord) {
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
        var uniqueCoords = uniqueCoordsArray.map(function (coord) {
            return L.latLng(coord[0], coord[1]);
        });

        // update the HTML element with the unique coordinates
        var coordinatesElement = document.getElementById("coordinates");
        var coordinatesString = "";
        for (var i = 0; i < uniqueCoords.length; i++) {
            coordinatesString += "<b>P" + (i + 1) + ": </b>" + uniqueCoords[i].lat + ", " + uniqueCoords[i].lng + "<br>";
        }

        coordinatesElement.innerHTML = coordinatesString;
        
    ;


