async function sendQuery() {
    let userQuery = document.getElementById("query").value;
    let responseDiv = document.getElementById("ai_response");
    let taskDiv = document.getElementById("tasks");


    let formData = new FormData();
    formData.append("user_query", userQuery);

    let response = await fetch("/chat", {
        method: "POST",
        body: formData
    });

    if (!response.ok) {
        responseDiv.innerHTML = "<p style='color: red;'>Error: Unable to process the request.</p>";
        return;
    }

    let data = await response.json();
    responseDiv.innerHTML = `<p>${data.ai_response}</p>`;

    // If data.tasks is an array, display each task (dictionary) as a formatted block
    if (Array.isArray(data.tasks)) {
        taskDiv.innerHTML = data.tasks.map(task => {
            // For each dictionary, create a div with key-value pairs
            return `<div style="margin-bottom:10px; padding:8px; border:1px solid #ccc;">
                ${Object.entries(task).map(([key, value]) => 
                    `<strong>${key}:</strong> ${value}<br>`
                ).join('')}
            </div>`;
        }).join('');
    } else {
        // fallback if tasks is a string
        taskDiv.innerHTML = `<p>${data.tasks}</p>`;
    }

    
}
