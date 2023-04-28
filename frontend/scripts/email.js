async function getFiles() {
  const response = await fetch("/get_files");
  const data = await response.json();

  if (data.folder_summary.length === 0) {
    const noFilesMsg = "No files found!";
    document.getElementById("fileList").innerHTML = noFilesMsg;
  } else {
    const folderSummary = data.folder_summary;
    document.getElementById("fileList").innerHTML = folderSummary;
  }
}

window.onload = function () {
  getFiles();
};

function updateFileListSummary() {
  let selected_files = document.getElementById("fileInput").files;
  let file_count = selected_files.length;
  document.getElementById("fileListHeader").textContent = `The following number of files will be sent: ${file_count}`;
}

function sendEmail() {
  const email = document.getElementById("emailInput").value;

  if (email === "") {
    alert("Please enter an email address");
    return;
  }

  document.getElementById("submitButton").disabled = true;
  document.getElementById("filesPreview").innerHTML = "<p>Loading...</p>";

  fetch("/send_zip_file", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email }),
  })
    .then((response) => {
      if (response.ok) {
        document.getElementById("filesPreview").innerHTML = "<p>Email sent successfully!</p>";
        // runs the delete_all_folders function by sending request to /delete_folders
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
          window.location.href = "confirm.html";
        }, 2000);
          
      } else {
        document.getElementById("filesPreview").innerHTML = "<p>An error has occurred... please try again later.</p>";
        console.error(response.statusText);
      }
    })
    .catch((error) => {
      document.getElementById("filesPreview").innerHTML = "<p>An error has occurred... please try again later.</p>";
      console.error(error);
    });
}