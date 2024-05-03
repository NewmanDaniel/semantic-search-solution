document.getElementById("submitButton").addEventListener("click", function() {
    const userInput = document.getElementById("textInput").value;
    const url = baseURL + "/api/get-top-k-similar-proposals/";
    fetch(url, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({text_to_search: userInput, k: 10})
    })
    .then(response => response.json())
    .then(data => {
        if(data.task_id) {
            pollForResult(data.task_id);
        }
    });
});

function pollForResult(taskId) {
    const resultUrl = baseURL + `/api/task-result/${taskId}/`;
    const interval = setInterval(() => {
        fetch(resultUrl)
        .then(response => response.json())
        .then(data => {
            if(data.status === 'completed') {
                clearInterval(interval);
                displayResult(data.result);
            }
        });
    }, 2000); // Poll every 2 seconds
}

function displayResult(data) {
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "";
    data.forEach(item => {
        resultDiv.innerHTML += `<p>${item[0]}: ${item[1]}</p>`;
    });
    resultDiv.innerHTML += '<button onclick="location.reload()">Try Again</button>';
}

