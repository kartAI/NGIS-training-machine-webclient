// Create a new XMLHttpRequest object
var xhr = new XMLHttpRequest();

// Set the URL of the file to load
xhr.open('GET', 'header.html');

// Set the response type to 'text'
xhr.responseType = 'text';

// When the file is loaded, insert the contents into the empty div
xhr.onload = function () {
    if (xhr.status === 200) {
        // Get a reference to the empty div
        var headerDiv = document.getElementById('header');

        // Insert the contents of the loaded file into the div
        headerDiv.innerHTML = xhr.response;
    }
};

// Send the request to load the file
xhr.send();

console.log('JavaScript code executed.');