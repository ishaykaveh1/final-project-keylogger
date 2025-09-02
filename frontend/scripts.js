const BACKEND_URL = "http://127.0.0.1:5000";

let currentContent = {}; // Variable to store the full content

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