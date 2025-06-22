async function getRecommendations() {
    let preferencesInput = document.getElementById("preferences").value;
    let responseDiv = document.getElementById("response");

    let formData = new FormData();
    formData.append("preferences", preferencesInput);

    let response = await fetch("/recommend", {
        method: "POST",
        body: formData
    });

    if (!response.ok) {
        responseDiv.innerHTML = "<p style='color: red;'>Error: Unable to process the request.</p>";
        return;
    }

    let data = await response.json();
    responseDiv.innerHTML = `<p>${data.recommendations}</p>`;
}