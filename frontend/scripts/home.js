
document.getElementById('cookiePolicyLink').addEventListener('click', function(event) {
    event.preventDefault();
    document.getElementById('cookiePolicyPopup').style.display = 'block';
});

document.getElementById('closePopup').addEventListener('click', function() {
    document.getElementById('cookiePolicyPopup').style.display = 'none';
});

window.onload = () => {
    setup_cookies()
  }
  
  async function setup_cookies(){
    const response = await fetch('/cookies', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    const data = response.json()
    console.log(data)
    return data
  }

