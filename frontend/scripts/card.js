//Define the card data
const cardData = [
    {
      icon: 'fa-map-marker-alt',
      text: 'Tegn utsnitt på kart',
      link: 'map.html'
    },
    {
      icon: 'fa-keyboard',
      text: 'Skriv inn koordinater',
      link: 'coords.html'
    },
    {
      icon: 'fa-upload',
      text: 'Last opp geoJSON-fil',
      link: 'upload.html'
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