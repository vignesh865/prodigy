const authorizationToken = "token 0a1163a8e4d5e6b87585d537937b7c2b56cc79b6";

// Function to check if a source is connected
function isSourceConnected(source, connectedSources) {
    return connectedSources.includes(source);
}

// Function to update the button state
function updateButtonState(buttonId, connectedSources) {
    const button = document.getElementById(buttonId);
    const source = button.getAttribute('data-source');

    if (isSourceConnected(source, connectedSources)) {
        // If the source is connected, disable the button and add "Connected" label
        button.disabled = true;
        button.innerHTML = `${button.innerHTML} (Connected)`;
    } else {
        // If the source is not connected, enable the button
        button.disabled = false;
    }
}

// Function to fetch the list of connected sources from the API
function fetchConnectedSources() {

    // Make a GET request to /integration/integrate with the Authorization header
    fetch('/integration/integrate', {
        headers: {
            'Authorization': authorizationToken
        }
    })
    .then(response => response.json())
    .then(data => {
        // Extract the "sources" array from the JSON response
        const connectedSources = data.sources;
        // Update the button state based on the list of connected sources
        updateButtonState('googleDriveButton', connectedSources);
        updateButtonState('oneDriveButton', connectedSources);
    })
    .catch(error => console.error("Error:", error));
}

function connectToSource(event){
    const source = event.currentTarget.getAttribute('data-source');
    const integrateEndpoint = "/integration/integrate?source_type="+source;

    fetch(integrateEndpoint, {
        method: 'POST',
        headers: {
            'Authorization': authorizationToken
        }
    }).then(response => response.json())
        .then(data => {
            if (data.code == 307) {
                // If the first API call is successful, redirect to the authorization URL
                window.location.href = data.message;
                return;
            }
                alert(data.message)
        })
        .catch(error => console.error("Error:", error));
}

// Call the fetchConnectedSources function on page load
window.addEventListener('load', fetchConnectedSources);
$('#googleDriveButton,#oneDriveButton').click(connectToSource)