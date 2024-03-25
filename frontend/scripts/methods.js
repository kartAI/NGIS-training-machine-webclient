
// Displays an alert with information about the layer selection
function showLayerInfo() {
  alert("Information about layer selection...");
}


// Displays an alert with information about Ortofoto
function showOrtofotoInfo() {
  alert("Information about Ortofoto...");
}

// Data structure representing the cards to be displayed on the webpage
const cardData = [
  {
    icon: 'fa-map-marker-alt', // Font Awesome icon class for the card
    text: 'Draw shape on map', // Text displayed on the card
    link: 'map.html' // URL the card links to
  },
  {
    icon: 'fa-keyboard', // Font Awesome icon class for the card
    text: 'Write coordinates', // Text displayed on the card
    link: 'coordinates.html' // URL the card links to
  },
  {
    icon: 'fa-upload', // Font Awesome icon class for the card
    text: 'Upload geoJSON-file', // Text displayed on the card
    link: 'uploadFile.html' // URL the card links to
  }
];


// Generates HTML content for cards based on cardData and appends it to the card container
const cardContainer = document.getElementById('card-container');
cardData.forEach(card => {
  const cardHtml = `
    <a href="${card.link}" class="card p-5 mb-4 rounded-3 shadow-sm onClick="updateImageSources()">
      <div class="card-body">
        <span class="fas ${card.icon}"></span>
      </div>
      <h3 class="my-0 fw-normal">${card.text}</h3>
    </a>
  `;
  cardContainer.innerHTML += cardHtml; // Append the card HTML to the container
});


// On window load, set up necessary cookies for the session
window.onload = () => {
  setup_cookies(); // Call the function to set up cookies
}

// Sets up cookies by making a POST request to the server
// @returns {Promise<Object>} A promise that resolves with the server response data

async function setup_cookies() {
  const response = await fetch('/cookies', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  });
  const data = await response.json(); // Parse the JSON response
  console.log(data); // Log the data for debugging
  return data; // Return the data for further processing
}

// Get references to DOM elements related to data source selection.
let ngis_layer = document.getElementById("ngis-layer");
let wms_layer = document.getElementById("wms-layer");
let fgb_layer = document.getElementById("fgb-layer");
let wms_orto = document.getElementById("wms-ortofoto");
let cog_orto = document.getElementById("cog-ortofoto");

// Updates the image sources based on user selections and sends the selections to the server
// @returns {Promise<Object>|void} A promise that resolves with the server response data, or void if selections are incomplete

async function updateImageSources() {
  console.log("Updating image sources...");
  let labelSource = ""; // Variable to hold the label source selection
  let ortoSource = ""; // Variable to hold the Ortofoto source selection
  let filled = true; // Flag to check if all selections are made

  // Determine the label source based on user selection
  if (ngis_layer.checked) {
    labelSource = "NGIS";
  } else if (wms_layer.checked) {
    labelSource = "WMS";
  } else if (fgb_layer.checked) {
    labelSource = "FGB";
  } else {
    filled = false; // No label source selected
    console.log("No label source selected");
  }

  // Determine the Ortofoto source based on user selection
  if (wms_orto.checked) {
    ortoSource = "WMS";
  } else if (cog_orto.checked) {
    ortoSource = "COG";
  } else {
    filled = false; // No Orto source selected
    console.log("No Orto source selected");
  }

  // If all necessary selections are made, send the data to the server
  if (filled) {
    console.log("Sending selections to the server...");
    const response = await fetch('/updateDataSources', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({"label_source": labelSource, "orto_source": ortoSource}),
    });
    
    const data = await response.json(); // Parse the JSON response
    return data; // Return the data for further processing
  } else {
    document.getElementById("Error").innerHTML = "Please select data sources";
  }
}
