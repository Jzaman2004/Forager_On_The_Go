// Handle form submission
document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();

    var formData = new FormData();
    formData.append('file', document.getElementById('file-input').files[0]);

    // Make the API request to Flask backend
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Populate the HTML with the response data
        document.getElementById('description').value = data.description;
        document.getElementById('confidence').value = data.confidence.toFixed(2);
        document.getElementById('survival-advice').value = data.survival_advice;

        // Removed the code that updates the image path
        // const imagePath = data.image_path; 
        // document.getElementById('output-img').src = imagePath;

        // Show the output section
        document.getElementById('output').style.display = 'block';
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
