document.addEventListener('DOMContentLoaded', function () {
    // Handle the display of results
    chrome.runtime.onMessage.addListener((data, sender, sendResponse) => {
        if (data.data[0] == 3) {
            print("GOT DATA")
            // Display the percent and url
            displayResults(data.data[1]);
        }
    });
});

function displayResults(data) {
    var percentElement = document.getElementById('percentage');
    var urlElement = document.getElementById('url-result');
    var percentageBar = document.getElementById('percentage-bar');

    percentElement.textContent = `Percentage: ${data.percent}%`;
    urlElement.textContent = `URL: ${data.url}`;

    if (data.percent < 30) {
        percentageBar.style.backgroundColor = 'red';
    } else if (data.percent >= 30 && data.percent < 70) {
        percentageBar.style.backgroundColor = 'yellow';
    } else {
        percentageBar.style.backgroundColor = 'green';
    }

    percentageBar.style.width = data.percent + '%';
}
