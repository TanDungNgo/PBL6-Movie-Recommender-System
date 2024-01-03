function updateFileName() {
  const fileInput = document.getElementById("file-input");
  const fileNameElement = document.getElementById("file-name");
  
  if (fileInput.files.length > 0) {
      fileNameElement.textContent = fileInput.files[0].name;
  } else {
      fileNameElement.textContent = "File not selected!";
  }
}

