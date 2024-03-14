  //Header
var xhr = new XMLHttpRequest();
xhr.open('GET', 'header.html');
xhr.responseType = 'text';

xhr.onload = function () {
  if (xhr.status === 200) {
    var headerDiv = document.getElementById('header');
    headerDiv.innerHTML = xhr.response;
  }
};
xhr.send();


// Map of pages and their corresponding next pages
const pageMap = {
  'uploadFile.html': 'setConstraints.html',
  'map.html': 'setConstraints.html',
  'coordinates.html': 'setConstraints.html',
  'setConstraints.html': 'success.html'
};

// Navigate to target page based on current page URL
function nav() {
  const url = window.location.href;
  const urlSuffix = url.split('/').pop();
  const targetPage = pageMap[urlSuffix];
  if (targetPage) {
    document.location.href = `./${targetPage}`;
  }
}

// Navigate to home page
function home() {
  var url = "frontend\pages\home.html";
  window.location(url);
}

const inputTraining = document.getElementById("training");
const inputValidation = document.getElementById("validation");
const inputBuilding = document.getElementById("building");
const inputBuildingLayer = document.getElementById("buildingCheck");
const inputRoadLayer = document.getElementById("roadCheck");
const inputBridgeLayer = document.getElementById("bridgeCheck");
const inputBuildingColor = document.getElementById("buildingColor");
const inputRoadColor = document.getElementById("roadColor");
const inputBridgeColor = document.getElementById("bridgeColor");
const inputTileSize = document.getElementById("tileSize");
const inputResolution = document.getElementById("imageResolution");
const continueBtn = document.getElementById("continueBtn");
const errorMessage = document.getElementById('error-message');
const labelWMS = document.getElementById("labelWMS");
const labelOrto = document.getElementById("labelOrto")

function validateStart() {
  const inputFields = ['training', 'validation', 'building'];
  const errorMessages = ['Please fill out this field.', 'Please fill out this field.', 'Please fill out this field.'];
  const rangeErrorMessage = 'Please enter a value between 0 and 100.';

  let allFieldsFilledFlag = true;
  let validRangeFlag = true;

  for (let i = 0; i < inputFields.length; i++) {
    const inputField = document.getElementById(inputFields[i]);
    const errorMessage = document.getElementById(`error-message-${inputFields[i]}`);

    if (inputField.value === '') {
      errorMessage.textContent = errorMessages[i];
      errorMessage.classList.remove('d-none');
      allFieldsFilledFlag = false;
    } else {
      errorMessage.textContent = '';
      errorMessage.classList.add('d-none');
    }

    const inputValue = parseFloat(inputField.value);
    if (isNaN(inputValue) || inputValue < 0 || inputValue > 100) {
      errorMessage.textContent = rangeErrorMessage;
      errorMessage.classList.remove('d-none');
      validRangeFlag = false;
    }
  }



  if (allFieldsFilledFlag && validRangeFlag) {
    updateConfig();
    startTraining();
  }
}

// Updates the WMS config file on the server
async function updateConfig() {
  //Define the arrays
  const layers = [];
  const colors = [];


  //Checks each checkbox to see if the box is checked, if it is then add the data to the array.
  if(inputBuildingLayer.checked){
    layers.push("Bygning")
    colors.push(inputBuildingColor.value)
  }

  if(inputRoadLayer.checked){
    layers.push("Veg")
    colors.push(inputRoadColor.value)
  }

  if(inputBridgeLayer.checked){
    layers.push("Bru")
    colors.push(inputBridgeColor.value)
  }

  const trainingFraction = [inputTraining.value, inputValidation.value, inputBuilding.value];

  const response = await fetch('/updateConfigFile', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({"data_parameters": trainingFraction, "layers": layers, "colors": colors, "tile_size": inputTileSize.value, "image_resolution": inputResolution.value, "labelWMS": labelWMS, "labelOrto": labelOrto}),
  });

  const data = await response.json();
  return data;
}



// Update the training data fractions on the server
async function updateValue() {
  const trainingFraction = [inputTraining.value, inputValidation.value, inputBuilding.value];

  const response = await fetch('/update_training', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(trainingFraction),
  });

  const data = await response.json();
  return data;
}

// Display a confirmation modal
function startTraining() {
  $('#confirmationModal').modal('show');
}

// Initiate a training process and redirect to next page
function confirmTraining() {
  fetch('/startTraining', {
    method: 'POST'
  })
    .then(() => {
      window.location.href = '/order.html';
    })
    .catch(error => console.error(error));
}

// Initiate a download process and redirect to next page
function generatePhotos() {
  fetch('/generatePhotos', {
    method: 'POST'
  })
    .then(() => {
      window.location.href = '/order.html';
    })
    .catch(error => console.error(error));
}

// Display the loading modal
function loadingModal() {
  $('.modal').modal('show');
}
