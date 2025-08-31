const BACKEND_URL = "http://127.0.0.1:5000";
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
    });

// Fetch content of a selected computer
function loadContent(name) {
    fetch(`${BACKEND_URL}/computer/${name}`)
        .then(response => response.json())
        .then(data => {
            let contentArea = document.getElementById("content-area");
            let text = "";

            for (let file in data.content) {
                text += `=== ${file} ===\n${data.content[file]}\n\n`;
            }

            contentArea.textContent = text;
        });
}