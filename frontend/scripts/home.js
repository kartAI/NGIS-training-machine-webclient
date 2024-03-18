
document.getElementById('cookiePolicyLink').addEventListener('click', function(event) {
    event.preventDefault();
    document.getElementById('cookiePolicyPopup').style.display = 'block';
});

document.getElementById('closePopup').addEventListener('click', function() {
    document.getElementById('cookiePolicyPopup').style.display = 'none';
});