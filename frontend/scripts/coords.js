document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("coordinates-input");
  const doneButton = document.getElementById("done-button");

  doneButton.addEventListener("click", async () => {
    // Get the input value and split it by commas
    const inputCoordinates = input.value.split(",");

    const coordsArray = [];

    // Loop through the inputCoordinates and create objects
    for (let i = 0; i < inputCoordinates.length; i += 2) {
      const latLng = L.latLng(parseFloat(inputCoordinates[i + 1]), parseFloat(inputCoordinates[i]));
      coordsArray.push(latLng);
    }

    console.log("coordsArray:", coordsArray);

    // Define the projection definitions
    const epsg4326 = 'EPSG:4326';
    const epsg3857 = 'EPSG:3857';

    // Convert the coordsArray to EPSG:3857
    const coordsArray3857 = coordsArray.map(coord => {
      const [x, y] = proj4(epsg4326, epsg3857, [coord.lng, coord.lat]);
        return [x, y];
      });

    console.log(coordsArray3857);
    updateCoordinates(coordsArray3857);

    // Create a polygon from the coordsArray and add it to the map
    const polygon = L.polygon(coordsArray, { color: "red" }).addTo(map);
    map.fitBounds(polygon.getBounds());

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
  });
});
