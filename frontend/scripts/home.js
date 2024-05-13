//Event listeners for the privacy popup and the cookie popup
document.getElementById('privacyPolicyLink').addEventListener('click', function(event) {
  event.preventDefault();
  document.getElementById('privacyPolicyPopup').style.display = 'block';
  document.getElementById('modalOverlay').style.display = 'block';  // Show the modal background
});

document.getElementById('closePrivacyPopup').addEventListener('click', function() {
  document.getElementById('privacyPolicyPopup').style.display = 'none';
  document.getElementById('modalOverlay').style.display = 'none';  // Hide the modal background
});

document.getElementById('cookiePolicyLink').addEventListener('click', function(event) {
  event.preventDefault();
  document.getElementById('cookiePolicyPopup').style.display = 'block';
  document.getElementById('modalOverlay').style.display = 'block';  // Show the modal background
});

document.getElementById('closeCookiePopup').addEventListener('click', function() {
  document.getElementById('cookiePolicyPopup').style.display = 'none';
  document.getElementById('modalOverlay').style.display = 'none';  // Hide the modal background
});

// Close pop-up when clicking outside of it
document.getElementById('modalOverlay').addEventListener('click', function() {
  document.getElementById('privacyPolicyPopup').style.display = 'none';
  document.getElementById('cookiePolicyPopup').style.display = 'none';
  document.getElementById('modalOverlay').style.display = 'none';
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

