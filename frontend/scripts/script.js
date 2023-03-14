
let scrollHeight = Math.max(
    document.body.scrollHeight, document.documentElement.scrollHeight,
    document.body.offsetHeight, document.documentElement.offsetHeight,
    document.body.clientHeight, document.documentElement.clientHeight
  );


  function nav() {
    const url = window.location.href;
    if (url.endsWith("/upload.html") || url.endsWith("/map.html")) {
      document.location.href = "./order.html";
    } else if (url.endsWith("/order.html")) {
      document.location.href = "./confirm.html";
    }
  }

  const formContainer = document.getElementById('form-container');

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
  
  
    // Create a new div element to group the label, input, and small elements
    const inputGroup = document.createElement('div');
    inputGroup.setAttribute('class', 'form-group');
    inputGroup.appendChild(label);
    inputGroup.appendChild(input);
  
    // Add the input group to the form container
    formContainer.appendChild(inputGroup);
  }