
// Creating map of URL suffixes to their corresponding target pages
const pageMap = {
  'upload.html': 'constraints.html',
  'map.html': 'constraints.html',
  'coords.html': 'constraints.html',
  'constraints.html': 'confirm.html'
};

// Function to handle page navigation
function nav() {
  const url = window.location.href;
  const urlSuffix = url.split('/').pop();
  const targetPage = pageMap[urlSuffix];
  if (targetPage) {
    document.location.href = `./${targetPage}`;
  }
}

let inputTraining = document.getElementById("training");
let inputValidation = document.getElementById("validation");
let inputBuilding = document.getElementById("building");
let continueBtn = document.getElementById("continueBtn");
const errorMessage = document.getElementById('error-message');

// Function to check if all required fields have values
function allFieldsFilled() {
  return (
    inputTraining.value !== '' &&
    inputValidation.value !== '' &&
    inputBuilding.value !== ''
  );
}

// Function to validate fields and start training
function validateStart() {
  if (allFieldsFilled()) {
    // Hide the error message if it's visible
    errorMessage.classList.add('d-none');

    // Call your existing functions
    updateValue();
    startTraining();
  } else {
    // Show the error message
    errorMessage.classList.remove('d-none');
  }
}

//update the training data fractions on the server
async function updateValue() {
  let inputTraining = document.getElementById("training");
  let inputValidation = document.getElementById("validation");
  let inputBuilding = document.getElementById("building");
  let training_fraction = [inputTraining.value, inputValidation.value, inputBuilding.value];

  const response = await fetch('http://localhost:8000/update_training', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(training_fraction),
  });

  const data = await response.json();
  return data;
}

function startTraining() {
  // Show the modal
  $('#confirmationModal').modal('show');
}

// Initiates a training process and redirects to next page
function confirmTraining() {
  fetch('/startTraining', {
    method: 'POST'
  })
    .then(() => {
      // If request succeeds, redirect to next page
      window.location.href = '/sendToEmail.html';
    })
    // If request fails, log error
    .catch(error => console.error(error));
}
// Loading screen function
function loadingModal() {
  $('.modal').modal('show');

}