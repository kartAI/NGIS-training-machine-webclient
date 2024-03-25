function showLayerInfo() {
  alert("Information about layer selection...");
}

function showOrtofotoInfo() {
  alert("Information about Ortofoto...");
}


//Define the card data
const cardData = [
  {
    icon: 'fa-map-marker-alt',
    text: 'Draw shape on map',
    link: 'map.html'
  },
  {
    icon: 'fa-keyboard',
    text: 'Write coordinates',
    link: 'coordinates.html'
  },
  {
    icon: 'fa-upload',
    text: 'Upload geoJSON-file',
    link: 'uploadFile.html'
  }
];

//Loop through the card data and generate the HTML code for each card -->
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
  cardContainer.innerHTML += cardHtml;
});

window.onload = () => {
  setup_folders();
  updateImageSources();
};

async function setup_folders() {
  const response = await fetch("/setupUserSessionFolders", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  });

  const data = await response.json();
  if(data.message){
    let element = document.getElementById("folder-message").innerHTML = data.message;
    element.removeAttribute("hidden")
  }
}


let ngis_layer = document.getElementById("ngis-layer")
let wms_layer = document.getElementById("wms-layer")
let fgb_layer = document.getElementById("fgb-layer")
let wms_orto = document.getElementById("wms-ortofoto")
let cog_orto = document.getElementById("cog-ortofoto")
async function updateImageSources(){
  console.log("AA")
  let labelSource = ""
  let ortoSource = ""
  let filled = true
  if(ngis_layer.checked){
    labelSource = "NGIS"
  }else if(wms_layer.checked){
    labelSource = "WMS"
  }else if(fgb_layer.checked){
    labelSource = "FGB"
  }else{
    filled = false
    console.log("No label source selected")
  }

  if(wms_orto.checked){
    ortoSource = "WMS"
  }else if(cog_orto.checked){
    ortoSource = "COG"
  }else{
    filled = false
    console.log("No Orto source selected")
  }

  if(filled){
    console.log("Calling..")
    const response = await fetch('/updateDataSources', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({"label_source": labelSource, "orto_source": ortoSource}),
    });
    
    const data = await response.json();

    if(data.message){
      let element = document.getElementById("folder-message").innerHTML = data.message;
      element.removeAttribute("hidden")
    }
    
    return data;
  }else{
    document.getElementById("Error").innerHTML = "Please select data sources"
  }
}
