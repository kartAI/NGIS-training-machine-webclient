async function getFiles() {
  const response = await fetch("/get_files");
  const data = await response.json();

  // Displays a message on the webpage if no files are found, or displays a summary of the folder contents
  if (data.folder_summary.length === 0) {
    const noFilesMsg = "No files found!";
    document.getElementById("fileList").innerHTML = noFilesMsg;
  } else {
    const folderSummary = data.folder_summary;
    document.getElementById("fileList").innerHTML = folderSummary;
  }
}

// Calls the getFiles function when the page loads
window.onload = function () {
  getFiles();
};

// Updates the file list summary based on the files selected by the user
function updateFileListSummary() {
  let selected_files = document.getElementById("fileInput").files;
  let file_count = selected_files.length;
  document.getElementById("fileListHeader").textContent = `The following number of files will be sent: ${file_count}`;
}

// Sends a POST request to the server to send an email with the selected files attached
function sendEmail() {
  const email = document.getElementById("emailInput").value;

  // Displays an error message if no email address is entered
  if (email === "") {
    alert("Please enter an email address");
    return;
  }

  // Disables the submit button and displays a loading message
  document.getElementById("submitButton").disabled = true;
  document.getElementById("filesPreview").innerHTML = "<p>Loading...</p>";

  // Sends a POST request to the server to send the email with the selected files attached
  fetch("/send_zip_file", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email }),
  })
    .then((response) => {
      if (response.ok) {
        // Displays a success message and redirects to a success page after a delay
        document.getElementById("filesPreview").innerHTML = "<p>Email sent successfully!</p>";

        // Sends a POST request to the server to delete all temporary folders created during the process
        fetch("/delete_folders", {
          method: "POST",
        })
          .then((response) => {
            if (!response.ok) {
              console.error("An error occurred while deleting folders:", response.statusText);
            }
          })
          .catch((error) => {
            console.error("An error occurred while deleting folders:", error);
          });

        setTimeout(() => {
          window.location.href = "success.html";
        }, 2000);
      } else {

        // Displays an error message if the email fails to send
        document.getElementById("filesPreview").innerHTML = "<p>An error has occurred... please try again later.</p>";
        console.error(response.statusText);
      }
    })
    .catch((error) => {

      // Displays an error message if an error occurs while sending the email
      document.getElementById("filesPreview").innerHTML = "<p>An error has occurred... please try again later.</p>";
      console.error(error);
    });
}
