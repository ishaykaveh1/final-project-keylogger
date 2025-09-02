const BACKEND_URL = "http://127.0.0.1:5000";

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

    fetch(`${BACKEND_URL}/data/${name}`)
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
        })
        .catch(error => {
            contentArea.textContent = "Error loading content.";
            console.error('Error:', error);
        });
}