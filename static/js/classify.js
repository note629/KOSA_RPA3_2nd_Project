window.onload = function () {
  var dropzone = document.getElementById("dropzone");

  // Assuming your file input field's id is 'id_image'
  var fileInput = document.getElementById("id_input_img");

  dropzone.ondragover = function () {
    this.className = "dragover";
    return false;
  };

  dropzone.ondragleave = function () {
    this.className = "";
    return false;
  };

  dropzone.ondrop = function (e) {
    e.preventDefault();
    this.className = "";

    fileInput.files = e.dataTransfer.files;

    // Trigger the onchange event manually since it doesn't get triggered automatically when setting files programmatically.
    var event = new Event("change");
    fileInput.dispatchEvent(event);
  };
};
