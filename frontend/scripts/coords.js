document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("coordinates-input");
  const doneButton = document.getElementById("done-button");

  doneButton.addEventListener("click", async () => {
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

    // Fetch code block
    try {
      const response = await fetch("/update_coord.js", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          coordinates: latLngArray.map((coord) => [coord.lat, coord.lng]),
        }),
      });

      if (response.ok) {
        console.log("Coordinates updated successfully");
      } else {
        console.error("Failed to update coordinates");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  });
});
