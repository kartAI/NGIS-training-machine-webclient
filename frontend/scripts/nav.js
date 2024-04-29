// Initialize a new XMLHttpRequest to load an HTML snippet into a div with the id 'header'
var xhr = new XMLHttpRequest();
xhr.open("GET", "header.html"); // Specifies the type of request and the URL of the file to be loaded
xhr.responseType = "text"; // Sets the response format to plain text

xhr.onload = function () {
  // This function is called when the request completes successfully
  if (xhr.status === 200) {
    // Check if the HTTP request status is "OK"
    var headerDiv = document.getElementById("header"); // Get the div element where the header will be loaded
    headerDiv.innerHTML = xhr.response; // Set the inner HTML of the div to the loaded header content
  }
};
xhr.send(); // Sends the request to the server

// Defines a map of pages to their corresponding next pages for navigation
const pageMap = {
  "uploadFile.html": "setConstraints.html",
  "map.html": "setConstraints.html",
  "coordinates.html": "setConstraints.html",
  "setConstraints.html": "success.html",
};

// Navigates to the target page based on the current page URL
function nav() {
  const url = window.location.href; // Get the current page URL
  const urlSuffix = url.split("/").pop(); // Extract the last part of the URL
  const targetPage = pageMap[urlSuffix]; // Get the target page from the map based on the current page
  if (targetPage) {
    document.location.href = `./${targetPage}`; // Navigate to the target page if it exists
  }
}

// Navigates to the home page.
function home() {
  var url = "frontend/pages/home.html"; // Define the URL of the home page
  window.location(url); // Redirect to the home page
}

//Info Popups
if (window.location.href.includes("methods.html")) {
  document.addEventListener("DOMContentLoaded", function () {
    console.log("HELLO");
    document.getElementById("info-modal-text").innerHTML = "none";
  });
}
