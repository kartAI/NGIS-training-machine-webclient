// coordinates.js
document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("coordinates-input");
    const doneButton = document.getElementById("done-button");
  
    doneButton.addEventListener("click", () => {
      // Get the input value and split it by commas
      const inputCoordinates = input.value.split(",");
  
      const latLngArray = [];
  
      // Loop through the inputCoordinates and create latLng objects
      for (let i = 0; i < inputCoordinates.length; i += 2) {
        const latLng = L.latLng(parseFloat(inputCoordinates[i]), parseFloat(inputCoordinates[i + 1]));
        latLngArray.push(latLng);
      }
  
      console.log("latLngArray:", latLngArray);
  
      // Create a polygon from the latLngArray and add it to the map
      const polygon = L.polygon(latLngArray, { color: "red" }).addTo(map);
      map.fitBounds(polygon.getBounds());

      var output = '';
                for (var i = 0; i < latLngArray.length; i++) {
                    output += '<b>P' + (i + 1) + ':</b> ' + latLngArray[i] + '<br>';

                    // Create a circle for each coordinate
                    var circle = L.circle(latLngArray[i], {
                        radius: 10, // Adjust the radius as needed
                        color: 'red',
                        fillColor: '#f03',
                        fillOpacity: 0.5
                    }).addTo(map);
                    circle.bindPopup('P' + (i + 1) + ' = ' + latLngArray[i]).openPopup();
                }
                document.getElementById('coordinates').innerHTML = output;
    });
  });
  