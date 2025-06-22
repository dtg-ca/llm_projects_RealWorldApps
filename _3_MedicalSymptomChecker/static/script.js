async function analyzeSymptoms() {
    let symptomsInput = document.getElementById("symptoms").value;
    let responseDiv = document.getElementById("response");

    let formData = new FormData();
    formData.append("symptoms", symptomsInput);

    let response = await fetch("/analyze_symptoms", {
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