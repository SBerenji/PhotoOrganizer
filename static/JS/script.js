// Event listener for form submission
document.getElementById("photoOrganizerForm").addEventListener('submit', async function (event) {
    event.preventDefault(); // Prevent form from reloading the page

    const formData = new FormData(); // Create FormData object
    const photoFiles = document.getElementById("photoFiles").files;

    // Append files to FormData
    for (let i = 0; i < photoFiles.length; i++) {
        formData.append('files', photoFiles[i]);
    }

    try {
        // Send POST request with FormData
        const response = await fetch('/organize-photos', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        
        if (response.ok) {
            alert(result.message);
            if (result.download_link) {
                const link = document.createElement("a");
                link.href = result.download_link;
                link.target = "_blank";
                link.textContent = "Download Organized Photos";
                document.body.appendChild(link);
            }
        }  else {
            alert(`Error: ${result.error || 'An unknown error occurred'}`);
        }
    } catch (error) {
        console.error('Fetch error:', error);
        alert('An unexpected error occurred while processing your request.');
    }
});
