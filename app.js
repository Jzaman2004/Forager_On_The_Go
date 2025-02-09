// Select the necessary elements
const imageInput = document.getElementById("imageInput");
const imagePreview = document.getElementById("imagePreview");
const processImageBtn = document.getElementById("processImageBtn");
const resultText = document.getElementById("resultText");

// Event listener for image upload
imageInput.addEventListener("change", function(event) {
    const file = event.target.files[0];

    if (file) {
        const reader = new FileReader();

        reader.onload = function(e) {
            // Create an img element to display the uploaded image
            const imgElement = document.createElement("img");
            imgElement.src = e.target.result;
            imgElement.alt = "Uploaded Image";
            imagePreview.innerHTML = "";  // Clear any previous preview
            imagePreview.appendChild(imgElement);
        }

        // Read the uploaded file as a Data URL (to display the image)
        reader.readAsDataURL(file);
    }
});

// Event listener for the "Process Image" button
processImageBtn.addEventListener("click", function() {
    // If an image is uploaded, display a processing message
    if (imageInput.files.length > 0) {
        resultText.textContent = "Processing image...";
        // Here you can add further image processing functionality
        // For now, let's just update the result text with a success message
        setTimeout(() => {
            resultText.textContent = "Image processed successfully!";
        }, 2000);
    } else {
        resultText.textContent = "Please upload an image first.";
    }
});
