function myfunction() {
  if (document.getElementById("displaytable").style.display === "none") {
    document.getElementById("displaytable").style.display = "table";
    document.getElementById("Detail").value = "Hide Analysis";
  } else {
    document.getElementById("displaytable").style.display = "none";
    document.getElementById("Detail").value = "Image Analysis";
  }
}

function showPreview(event) {
  if (event.target.files.length > 0) {
    var src = URL.createObjectURL(event.target.files[0]);
    var preview = document.getElementById("file-ip-1-preview");
    var process = document.getElementById("process");
    var classify = document.getElementById("classify");
    preview.src = src;
    process.style.display = "inline-block";
    classify.style.display = "inline-block";
  }
}
