let scrollHeight = Math.max(
  document.body.scrollHeight, document.documentElement.scrollHeight,
  document.body.offsetHeight, document.documentElement.offsetHeight,
  document.body.clientHeight, document.documentElement.clientHeight
);

function nav() {
  const url = window.location.href;
  if (url.endsWith("/upload.html") || url.endsWith("/map.html")|| url.endsWith("/coords.html")) {
    document.location.href = "./order.html";
  } else if (url.endsWith("/order.html")) {
    document.location.href = "./confirm.html";
  }
}

async function updateValue() {
  let inputTraining = document.getElementById("training");
  let inputValidation = document.getElementById("validation");
  let training_fraction = [inputTraining.value, inputValidation.value];

  console.log(training_fraction);

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

function confirmTraining() {
  fetch('/startTraining', {
      method: 'POST'
  })
      .then(() => {
          // Navigate to confirm.html regardless of the response
          window.location.href = '/sendToEmail.html';
      })
      .catch(error => console.error(error));
}

