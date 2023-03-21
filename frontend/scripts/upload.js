document.getElementById('file-input').addEventListener('change', function() {
    var file = this.files[0];
    var reader = new FileReader();
    reader.onload = function(e) {
        var data = JSON.parse(e.target.result);
        var geojsonLayer = L.geoJSON(data, {
            onEachFeature: function(feature, layer) {
                var coordinates = feature.geometry.coordinates;
                document.getElementById('coordinates').innerHTML = coordinates;
            }
        });
        geojsonLayer.addTo(map);
        map.fitBounds(geojsonLayer.getBounds());
    };
    reader.readAsText(file);
    });