function uploadImage() {
    document.getElementById('fileInput').click();
}

document.getElementById('upload-container').addEventListener('click', uploadImage);

document.getElementById('upload-container').addEventListener('dragover', function(e) {
    e.preventDefault();
    e.stopPropagation();
    this.classList.add('dragover');
});

document.getElementById('upload-container').addEventListener('dragleave', function(e) {
    e.preventDefault();
    e.stopPropagation();
    this.classList.remove('dragover');
});

document.getElementById('upload-container').addEventListener('drop', function(e) {
    e.preventDefault();
    e.stopPropagation();
    this.classList.remove('dragover');

    var file = e.dataTransfer.files[0];
    var reader = new FileReader();

    reader.onload = function(e) {
        var imagePreview = document.getElementById('imagePreview');
        imagePreview.innerHTML = '<img src="' + e.target.result + '" class="img-thumbnail">';
    };

    reader.readAsDataURL(file);
});

// window.onload = function() {
//   var dropZone = document.getElementById('drop_zone');
//   var imgDisplay = document.getElementById('img_display');

//   // Prevent default behavior for drag and drop
//   ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
//       dropZone.addEventListener(eventName, preventDefaults, false);
//       document.body.addEventListener(eventName, preventDefaults, false);
//   });

//   // Function to prevent default behavior
//   function preventDefaults(e) {
//       e.preventDefault();
//       e.stopPropagation();
//   }

//   // Highlight drop zone when dragging over it
//   ['dragenter', 'dragover'].forEach(eventName => {
//       dropZone.addEventListener(eventName, highlight, false);
//   });

//   ['dragleave', 'drop'].forEach(eventName => {
//       dropZone.addEventListener(eventName, unhighlight, false);
//   });

//   // Function to highlight drop zone
//   function highlight() {
//       dropZone.classList.add('highlight');
//   }

//   // Function to remove highlight from drop zone
//   function unhighlight() {
//       dropZone.classList.remove('highlight');
//   }

//   // Handle dropped files
//   dropZone.addEventListener('drop', handleDrop, false);

//   // Function to handle dropped files
//   function handleDrop(e) {
//       var dt = e.dataTransfer;
//       var files = dt.files;

//       handleFiles(files);
//   }

//   // Function to handle files
//   function handleFiles(files) {
//       for (var i = 0; i < files.length; i++) {
//           var file = files[i];
//           var imageType = /^image\//;

//           if (!imageType.test(file.type)) {
//               alert("Please drop only images.");
//               continue;
//           }

//           var img = document.createElement("img");
//           img.file = file;
//           img.classList.add('img_preview');

//           imgDisplay.style.display = 'block';
//           imgDisplay.src = URL.createObjectURL(file);
//       }
//   }
// }

// // Function to trigger file input click
// function uploadImage() {
//   document.getElementById('fileInput').click();
// }

// // Event listener for file input change
// document.getElementById('fileInput').addEventListener('change', function () {
//   const file = this.files[0];
//   if (file) {
//       const reader = new FileReader();
//       reader.onload = function (e) {
//           const imageData = e.target.result;
//           document.getElementById('imagePreview').innerHTML = '<img src="' + imageData +
//               '" style="max-width: 100%; max-height: 300px;">';
//       };
//       reader.readAsDataURL(file);
//   }
// });

// // Event listener for form submission
// document.getElementById('upload-form').addEventListener('submit', function (event) {
//   event.preventDefault();

//   var form_data = new FormData();
//   form_data.append('image', document.querySelector('input[name="file"]').files[0]);

//   // Perform fetch request
//   fetch('/image_analysis', {
//       method: 'POST',
//       body: form_data
//   })
//   .then(response => response.json())
//   .then(data => {
//       // Display analysis result
//       var result_div = document.getElementById('result');
//       result_div.style.display = 'block';
//       var result_content = document.querySelector('.result-content');
//       result_content.innerHTML = '';

//       for (var key in data) {
//           var value = data[key];
//           if (typeof value === 'object') {
//               result_content.innerHTML += `<p><strong>${key}:</strong></p>`;
//               for (var prop in value) {
//                   result_content.innerHTML += `<p>${prop}: ${value[prop]}</p>`;
//               }
//           } else {
//               result_content.innerHTML += `<p><strong>${key}:</strong> ${value}</p>`;
//           }
//       }
//   })
//   .catch(error => console.error('Error:', error));
// });

// // Event listener for upload button click
// document.getElementById('upload-btn').addEventListener('click', function () {
//   document.getElementById('fileInput').click();
// });

// // Event listener for submit button click
// document.getElementById('submit-btn').addEventListener('click', function () {
//   document.getElementById('upload-form').submit();
// });

// // Event listener for file input change
// document.getElementById('file').addEventListener('change', function () {
//   var file = this.files[0];
//   if (file) {
//       var reader = new FileReader();
//       reader.onload = function (event) {
//           var imagePreview = document.getElementById('image-preview');
//           imagePreview.innerHTML = `<img src="${event.target.result}" alt="Uploaded Image">`;
//           imagePreview.style.display = 'block';
//       };
//       reader.readAsDataURL(file);
//   } else {
//       document.getElementById('image-preview').style.display = 'none';
//   }
// });

// // Event listener for image preview click
// document.getElementById('image-preview').addEventListener('click', function () {
//   document.getElementById('upload-btn').click();
// });
