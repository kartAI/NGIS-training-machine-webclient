
document.getElementById('cookiePolicyLink').addEventListener('click', function(event) { // Add event listener to the cookie policy link
    event.preventDefault(); // Prevent the default action of the link
    document.getElementById('cookiePolicyPopup').style.display = 'block'; // Display the cookie policy popup
});

document.getElementById('closePopup').addEventListener('click', function() { // Add event listener to the close button
    document.getElementById('cookiePolicyPopup').style.display = 'none'; // Hide the cookie policy popup
});

// Elements for input fields and the continue buttons
window.onload = () => {
    setup_cookies()
    firstTime = localStorage.getItem("firstTime")
    if(firstTime == null){
        document.getElementById('cookiePolicyPopup').style.display = 'block';
        localStorage.setItem("firstTime", "No")
    }
  }
  // Sets up cookies by making a POST request to the server (/cookies route)
  async function setup_cookies(){
    const response = await fetch('/cookies', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', 
      },
    });
    const data = response.json() // Parse the JSON response
    console.log(data)
    return data
  }

