// Initialize a new XMLHttpRequest to load an HTML snippet into a div with the id 'header'
var xhr = new XMLHttpRequest();
xhr.open('GET', 'header.html'); // Specifies the type of request and the URL of the file to be loaded
xhr.responseType = 'text'; // Sets the response format to plain text

xhr.onload = function () {
  // This function is called when the request completes successfully
  if (xhr.status === 200) { // Check if the HTTP request status is "OK"
    var headerDiv = document.getElementById('header'); // Get the div element where the header will be loaded
    headerDiv.innerHTML = xhr.response; // Set the inner HTML of the div to the loaded header content
  }
};
xhr.send(); // Sends the request to the server

// Defines a map of pages to their corresponding next pages for navigation
const pageMap = {
  'uploadFile.html': 'setConstraints.html',
  'map.html': 'setConstraints.html',
  'coordinates.html': 'setConstraints.html',
  'setConstraints.html': 'success.html'
};

// Navigates to the target page based on the current page URL
function nav() {
  const url = window.location.href; // Get the current page URL
  const urlSuffix = url.split('/').pop(); // Extract the last part of the URL
  const targetPage = pageMap[urlSuffix]; // Get the target page from the map based on the current page
  if (targetPage) {
    document.location.href = `./${targetPage}`; // Navigate to the target page if it exists
  }
}

// Navigates to the home page.
function home() {
  var url = "frontend/pages/home.html"; // Define the URL of the home page
  window.location(url); // Redirect to the home page
}
// Elements for input fields and the continue button
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
const emailInput = document.getElementById("email");
const datasetNameInput = document.getElementById("datasetName");
const continueBtn = document.getElementById("continueBtn");
const errorMessage = document.getElementById('error-message');

// Validates the start conditions before proceeding
function validateStart() {
  // Define required input fields and error messages
  const inputFields = ['training', 'validation', 'building', "tileSize", "imageResolution"];
  const emptyMessage = "Please fill out this field."
  const rangeErrorMessage = 'Please enter a value between 1 and 100 in this field.';
  // Update configuration and start the training process if validation passes
  let allFieldsFilledFlag = true;
  let validRangeFlag = true;


  let email = "";
  let datasetName = "Dataset"
  if(emailInput.value != ""){
      email = emailInput.value;
    }
    
    
    if(datasetNameInput.value != ""){
      datasetName = datasetNameInput.value
    }
    localStorage.setItem("datasetName", datasetNameInput.value)

  // Check if all input fields are filled and display error messages if not
  for (let i = 0; i < inputFields.length; i++) {
    const inputField = document.getElementById(inputFields[i]); // Get the input field element
    const errorMessage = document.getElementById(`error-message-${inputFields[i]}`); // Get the error message element

    // Check if the input field is empty and display an error message if so
    if (inputField.value === '') {
      errorMessage.textContent = emptyMessage;
      errorMessage.classList.remove('d-none');
      allFieldsFilledFlag = false;
    } else { // Clear the error message if the input field is filled
      errorMessage.textContent = '';
      errorMessage.classList.add('d-none');
    }
  }
  // Line 78-113 | Check if the input fields are within the valid range and display error messages if not
  console.log(inputTraining.value)
  if(parseFloat(inputTraining.value) < 0 || parseFloat(inputTraining.value) > 100){
    errorElement = document.getElementById("error-message-training");
      errorElement.textContent = rangeErrorMessage;
      errorElement.classList.remove('d-none');
      validRangeFlag = false;
  } 

  if(parseFloat(inputValidation.value) < 0 || parseFloat(inputValidation.value) > 100){
    errorElement = document.getElementById("error-message-validation");
      errorElement.textContent = rangeErrorMessage;
      errorElement.classList.remove('d-none');
      validRangeFlag = false;
  }

  if(parseFloat(inputBuilding.value) < 0 || parseFloat(inputBuilding.value) > 100){
    errorElement = document.getElementById("error-message-building");
      errorElement.textContent = rangeErrorMessage;
      errorElement.classList.remove('d-none');
      validRangeFlag = false;
  }

  if(parseFloat(inputTileSize.value) < 100 || parseFloat(inputTileSize.value) > 1104){
    errorElement = document.getElementById("error-message-tileSize");
      errorElement.textContent = "Please enter a tile size between 100 and 1104";
      errorElement.classList.remove('d-none');
      validRangeFlag = false;
  }

  if(parseFloat(inputResolution.value) < 0 || parseFloat(inputResolution.value) > 0.5){
    errorElement = document.getElementById("error-message-imageResolution");
      errorElement.textContent = "Please enter a resolution between 0.1 and 0.5";
      errorElement.classList.remove('d-none');
      validRangeFlag = false;
    }
    
    if (allFieldsFilledFlag && validRangeFlag) {
      if(updateConfig())
      updateConfig();
      startTraining();
  }
}

// Updates the WMS config file on the server
async function updateConfig() {
  // Define the arrays
  const layers = [];
  const colors = [];


  console.log(datasetName);
  console.log(email); 


  // Line 128 - 142 | Checks each checkbox to see if the box is checked, if it is then add the data to the array
  if(inputBuildingLayer.checked){
    layers.push("Bygning")
    colors.push(inputBuildingColor.value)
  }

  if(inputRoadLayer.checked){
    layers.push("Veg")
    colors.push(inputRoadColor.value)
  }

  if(inputBridgeLayer .checked){
    layers.push("Bru")
    colors.push(inputBridgeColor.value)
  }
  // Fetches the data from the server and returns the data
  const trainingFraction = [inputTraining.value, inputValidation.value, inputBuilding.value];

  // Fetches the data from the server and returns the data
  const response = await fetch('/updateConfigFile', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({"data_parameters": trainingFraction, "layers": layers, "colors": colors, "tile_size": inputTileSize.value, "image_resolution": inputResolution.value, "email" : emailInput.value, "dataset_name": datasetNameInput.value}),
  });
  // Await the JSON response from the server, which would include result data
  const data = await response.json();
  if(data.error_message){
    document.getElementById("error-message").innerHTML = data.error_message
  }
  return data;
}


// Display a confirmation modal
function startTraining() {
  $('#confirmationModal').modal('show');
}

// Initiate a download process and redirect to next page
async function generatePhotos() {
  const response = await fetch('/generatePhotos', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  const data = await response.json();
  if(data.message){
    let element = document.getElementById("message");
    element.innerHTML = data.message
    element.classList.add("alert-danger")
    element.removeAttribute("hidden")
    document.getElementById("loadingModal").setAttribute("hidden")
  }else{
    document.location.href = "./order.html"
    }
}


// Display the loading modal
function loadingModal() {
  $('#loadingModal').modal('show');
}




// Add event listeners to the input fields
inputTraining.addEventListener("input", updateValidation);
inputValidation.addEventListener("input", updateTraining);

// Function to update validation input based on training input
function updateValidation() {
  const trainingValue = parseFloat(inputTraining.value);
  if (!isNaN(trainingValue)) {
    const validationValue = 100 - trainingValue;
    inputValidation.value = validationValue > 0 ? validationValue : 0;
  }
}

// Function to update training input based on validation input
function updateTraining() {
  const validationValue = parseFloat(inputValidation.value);
  if (!isNaN(validationValue)) {
    const trainingValue = 100 - validationValue;
    inputTraining.value = trainingValue > 0 ? trainingValue : 0;
  }
}

// Initialize values when the page loads
updateValidation();
updateTraining();


if(localStorage.getItem("ConfigSet") != null){
  data_parameters = localStorage.getItem("data_parameters").split(",")
  inputTraining.value = parseFloat(data_parameters[0])
  inputValidation.value = parseFloat(data_parameters[1])
  inputBuilding.value = parseFloat(data_parameters[2])
 
 
  colors = localStorage.getItem("colors").split(",")
  console.log(colors[0])
  inputBuildingColor.value = String(colors[0])
  inputBridgeColor.value = colors[1]
  inputRoadColor.value = colors[2]

  layers = localStorage.getItem("layers").split(",")

  if(!layers.includes("Veg")){
    inputRoadLayer.checked = false
  }
  if(!layers.includes("Bru")){
    inputBridgeLayer.checked = false
  }
  if(!layers.includes("Bygning")){
    inputBridgeLayer.checked = false
  }

  inputTileSize.value = parseFloat(localStorage.getItem("tile_size"))
  inputResolution.value = parseFloat(localStorage.getItem("image_resolution"))
}