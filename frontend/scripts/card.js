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
    <a href="${card.link}" class="card p-5 mb-4 rounded-3 shadow-sm">
      <div class="card-body">
        <span class="fas ${card.icon}"></span>
      </div>
      <h3 class="my-0 fw-normal">${card.text}</h3>
    </a>
  `;
  cardContainer.innerHTML += cardHtml;
});
