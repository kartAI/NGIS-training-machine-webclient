const formContainer = document.getElementById('form-container');
  const inputsArray = [];

  for (let i = 1; i <= 5; i++) {
    // Create a new label element
    const label = document.createElement('label');
    label.setAttribute('for', `coordinates-${i}`);
    label.textContent = `Coordinates Point ${i}`;

    // Create a new input element
    const input = document.createElement('input');
    input.setAttribute('type', 'text');
    input.setAttribute('id', `coordinates-${i}`);
    input.setAttribute('class', 'form-control');
    input.setAttribute('aria-describedby', 'coordinateHelp');
    input.setAttribute('placeholder', 'Enter coordinates, separated by comma');

    // Add an event listener to each input to save its value to the array
    input.addEventListener('change', (event) => {
      inputsArray[i - 1] = event.target.value;
    });

    // Create a new div element to group the label, input, and small elements
    const inputGroup = document.createElement('div');
    inputGroup.setAttribute('class', 'form-group');
    inputGroup.appendChild(label);
    inputGroup.appendChild(input);

    // Add the input group to the form container
    formContainer.appendChild(inputGroup);
  }

  // Create a "Done" button to save the input values and call saveCoordinates()
  const doneButton = document.createElement('button');
  doneButton.setAttribute('type', 'button');
  doneButton.setAttribute('class', 'btn btn-primary');
  doneButton.textContent = 'Done';
  doneButton.addEventListener('click', () => {
    // Get the input values from the inputsArray
    const coordinatesArray = inputsArray.map(input => input.split(","));

    console.log("coordinatesArray:", coordinatesArray);

    const latLngArray = [];

    // Loop through the coordinatesArray and create latLng objects
    for (let i = 0; i < coordinatesArray.length; i++) {
      const latLng = L.latLng(parseFloat(coordinatesArray[i][0]), parseFloat(coordinatesArray[i][1]));
      latLngArray.push(latLng);
    }

    console.log("latLngArray:", latLngArray);

    // Create a polygon from the latLngArray and add it to the map
    const polygon = L.polygon(latLngArray, { color: "red" }).addTo(map);
    map.fitBounds(polygon.getBounds());
  });

  // Add the "Done" button to the form container
  formContainer.appendChild(doneButton);