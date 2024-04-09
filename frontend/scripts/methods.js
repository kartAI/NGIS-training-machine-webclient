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
    icon: "fa-map-marker-alt", // Font Awesome icon class for the card
    text: "Draw shape on map", // Text displayed on the card
    link: "map.html", // URL the card links to
  },
  {
    icon: "fa-keyboard", // Font Awesome icon class for the card
    text: "Write coordinates", // Text displayed on the card
    link: "coordinates.html", // URL the card links to
  },
  {
    icon: "fa-upload", // Font Awesome icon class for the card
    text: "Upload geoJSON-file", // Text displayed on the card
    link: "uploadFile.html", // URL the card links to
  },
];

// Generates HTML content for cards based on cardData and appends it to the card container
const cardContainer = document.getElementById("card-container");
cardData.forEach((card) => {
  const cardHtml = `
    <a href="${card.link}" class="card p-5 mb-4 rounded-3 shadow-sm>
      <div class="card-body">
        <span class="fas ${card.icon}"></span>
        <br> 
      </div>
      <h3 class="my-0 fw-normal">${card.text}</h3>
    </a>
  `;
  cardContainer.innerHTML += cardHtml; // Append the card HTML to the container
});



// Sets up cookies by making a POST request to the server
// @returns {Promise<Object>} A promise that resolves with the server response data

async function setup_user_folders() {
  const response = await fetch("/setupUserSessionFolders", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  });
  const data = await response.json(); // Parse the JSON response
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

  document.getElementById("loadingIcon").hidden = false;
  document.getElementById("message").hidden = true;

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
    const response = await fetch("/updateDataSources", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        label_source: labelSource,
        orto_source: ortoSource,
      }),
    });

    const data = await response.json(); // Parse the JSON response
    console.log(data);
    if (data.error == 1) {
      let element = document.getElementById("message");
      element.innerHTML = data.message;
      element.classList.add("alert-danger");
      element.removeAttribute("hidden");
    } else {
      let element = document.getElementById("message");
      element.innerHTML = data.message;
      element.classList.add("alert-success");
    }
    setTimeout(() => {
      document.getElementById("loadingIcon").hidden = true;
      document.getElementById("message").hidden = false;
    }, 1000); // 1000 milliseconds (1 second)

    return data; // Return the data for further processing
  } else {
    document.getElementById("Error").innerHTML = "Please select data sources";
  }
}



async function loadMetaData() {
  fileElement = document.getElementById("file-input");

  if (!fileElement.files[0]) {
    alert("Please add a file!");
    return;
  }
  console.log("Loading metadata from file and sending it to the server...");
  var file = fileElement.files[0];
  var reader = new FileReader();

    
    // Function to be called when the file is successfully read
    reader.onload = function (e) {
        // Attempt to parse the file content as JSON
        try {
            var data = JSON.parse(e.target.result);
            coordinates_input = data["Chosen Coordinates: "]
            config_input = data["Config Options Used: "]
            uploadMetaData(coordinates_input, config_input)
          }catch (error) {
            // Alert the user in case of an error parsing the JSON file content 
            alert('Error parsing the JSON file: ' + error);
        }
    }
    reader.readAsText(file);
}

async function uploadMetaData(coordinates, config){
  const response = await fetch("/loadMetaData", {
     method: "POST",
     headers: {
       "Content-Type": "application/json",
     },
     body: JSON.stringify({
       coordinates_input: {"Coordinates" : coordinates}, 
       label_source: config["label_source"],
       orto_source: config["orto_source"],
       data_parameters: config["data_parameters"],
       layers: config["layers"],
       colors: config["colors"],
       tile_size: config["tile_size"], 
       image_resolution: config["image_resolution"]
     })
   });

   const data = await response.json()
   if(data.written == true){
    document.getElementById("loadingIcon").hidden = false;
    document.getElementById("message").hidden = true;
    setTimeout(() => {
      document.getElementById("loadingIcon").hidden = true;
      document.getElementById("message").hidden = false;
    }, 1000); // 1000 milliseconds (1 second)

    console.log(config["data_parameters"])

    localStorage.setItem("Coordinates", coordinates)
    localStorage.setItem("ConfigSet", "True")
    localStorage.setItem("label_source", config["label_source"])
    localStorage.setItem("orto_source", config["orto_source"])
    localStorage.setItem("data_parameters", config["data_parameters"])
    localStorage.setItem("layers", config["layers"])
    localStorage.setItem("colors", config["colors"])
    localStorage.setItem("tile_size", config["tile_size"])
    localStorage.setItem("image_resolution", config["image_resolution"])

    let element = document.getElementById("message");
      element.innerHTML = data.message;
      element.classList.add("alert-success");
      element.removeAttribute("hidden");
      switch(config["label_source"]){
        case "WMS":
        wms_layer.checked = true
        break
        case "NGIS":
        ngis_layer.checked = true
        break
        case "FGB":
        fgb_layer.checked = true
        break
      }

      switch(config["orto_source"]){
        case "WMS":
        wms_orto.checked = true
        break
        case "COG":
        cog_orto.checked = true
        break
      }

   }else{
    let element = document.getElementById("message");
      element.innerHTML = data.message;
      element.classList.add("alert-danger");
      element.removeAttribute("hidden");
   }
 }

 // On window load, set up necessary cookies for the session
window.onload = () => {
  setup_user_folders(); // Call the function to set up cookies
  updateImageSources();
};

 document.getElementById('file-input').addEventListener('change', function(e) {
  loadMetaData()
});

document.getElementById('ngis-layer').addEventListener('change', function(e) {
  updateImageSources()
});

document.getElementById('wms-layer').addEventListener('change', function(e) {
  updateImageSources()
});


document.getElementById('fgb-layer').addEventListener('change', function(e) {
  updateImageSources()
});


document.getElementById('wms-ortofoto').addEventListener('change', function(e) {
  updateImageSources()
});


document.getElementById('cog-ortofoto').addEventListener('change', function(e) {
  updateImageSources()
});

document.getElementById('satelitt-ortofoto').addEventListener('change', function(e) {
  updateImageSources()
});


document.getElementById('ortoDatabase').addEventListener('change', function(e) {
  updateImageSources()
});
