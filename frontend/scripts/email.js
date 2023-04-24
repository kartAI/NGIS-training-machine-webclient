async function getFiles() {
  const response = await fetch("/get_files");
  const data = await response.json();

  if (data.folder_summary.length === 0) {
    const noFilesMsg = "Ingen filer funnet!";
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
  document.getElementById("fileListHeader").textContent = `Følgende antall filer vil bli sendt: ${file_count}`;
}

function sendEmail() {
  const email = document.getElementById("emailInput").value;

  if (email === "") {
    alert("Please enter an email address");
    return;
  }

  document.getElementById("submitButton").disabled = true;
  document.getElementById("filesPreview").innerHTML = "<p>Laster...</p>";

  fetch("/send_zip_file", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email }),
  })
    .then((response) => {
      if (response.ok) {
        document.getElementById("filesPreview").innerHTML = "<p>E-posten ble sendt!</p>";
        // Kjør delete_all_folders funksjonen ved å sende en forespørsel til /delete_folders
        fetch("/delete_folders", {
          method: "POST",
        })
          .then((response) => {
            if (!response.ok) {
              console.error("En feil oppstod under sletting av mapper:", response.statusText);
            }
          })
          .catch((error) => {
            console.error("En feil oppstod under sletting av mapper:", error);
          });
      } else {
        document.getElementById("filesPreview").innerHTML = "<p>En feil har oppstått... prøv igjen senere.</p>";
        console.error(response.statusText);
      }
    })
    .catch((error) => {
      document.getElementById("filesPreview").innerHTML = "<p>En feil har oppstått... prøv igjen senere.</p>";
      console.error(error);
    });
}
