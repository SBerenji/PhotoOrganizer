// Event listener for form submission
document.getElementById("photoOrganizerForm").addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form from reloading the page



    // Get file path from the input field
    let filePath = document.getElementById('filePath').value;

    // Send POST request to FastAPI backend with the file path
    fetch('/organize-photos', {
        method : 'POST',
        headers:{
            'Content-Type' : 'application/json',
        },
        body: JSON.stringify({
            file_path: filePath
        })
    })
    .then(response => response.json())
    .then(data => {
        //Handle the response from the backend (display a success message)
        alert(data.message);

        // update the UI  ???
    })
    .catch(error => {
        console.error('Error:', error)
    })



})