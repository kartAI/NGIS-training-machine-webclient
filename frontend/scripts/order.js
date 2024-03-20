
//Javascript code for downloading file. missings paths and file
document.getElementById("downloadButton").addEventListener("click", function() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/path-to-your-file", true); // Specify the file path here
    xhr.responseType = "blob";
    xhr.onload = function() {
        if (xhr.status === 200) {
            var blob = xhr.response;
            var link = document.createElement("a");
            link.href = window.URL.createObjectURL(blob);
            link.download = "filename.extension"; // Specify the filename and extension
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    };
    xhr.send();
});

fetch('header.html')
    .then(function(response) {
        return response.text();
    })
    .then(function(data) {
        document.getElementById('header').innerHTML = data;
    })
    .catch(function(error) {
        console.error('Error loading the header:', error);
    });
