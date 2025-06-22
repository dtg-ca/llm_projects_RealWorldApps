async function sendQuery() {
    let userQuery = document.getElementById("query").value;
    let responseDiv = document.getElementById("response");

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
    responseDiv.innerHTML = `<p>${data.response}</p>`;
}
