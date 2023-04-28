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
function home() {
  var url = "frontend\pages\home.html";
  window.location(url);
}

const inputTraining = document.getElementById("training");
const inputValidation = document.getElementById("validation");
const inputBuilding = document.getElementById("building");
const continueBtn = document.getElementById("continueBtn");
const errorMessage = document.getElementById('error-message');

// Check if all required fields have values
function validateStart() {
  const inputFields = ['training', 'validation', 'building'];
  const errorMessages = ['Please fill out this field.', 'Please fill out this field.', 'Please fill out this field.'];

  let allFieldsFilledFlag = true;

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
  }

  if (allFieldsFilledFlag) {
    updateValue();
    startTraining();
  }
}

// Update the training data fractions on the server
async function updateValue() {
  const trainingFraction = [inputTraining.value, inputValidation.value, inputBuilding.value];

  const response = await fetch('http://localhost:8000/update_training', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(trainingFraction),
  });

  const data = await response.json();
  return data;
}

// Show the confirmation modal
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

// Show the loading modal
function loadingModal() {
  $('.modal').modal('show');
}
