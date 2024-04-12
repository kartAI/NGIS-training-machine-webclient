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