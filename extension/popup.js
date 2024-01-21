document.addEventListener('DOMContentLoaded', function () {
    // Common code for all sections
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
        if (message.action === 'displayData') {
            displayResults(message.data);
        }
    });

    // Popup Section
    var checkPoliticalButton = document.getElementById('button-political');
    var checkScientificButton = document.getElementById('button-scientific');

    if (checkPoliticalButton) {
        checkPoliticalButton.addEventListener('click', function () {
            hidePopup();
            showLoadingScreen();
            simulateAPIResponse();
        });
    }

    if (checkScientificButton) {
        checkScientificButton.addEventListener('click', function () {
            hidePopup();
            showLoadingScreen();
            simulateAPIResponse();
        });
    }

    // Loading Screen Section
    function showLoadingScreen() {
        var loadingScreen = document.querySelector('.loading-screen');
        loadingScreen.style.display = 'block';
    }

    function hideLoadingScreen() {
        var loadingScreen = document.querySelector('.loading-screen');
        loadingScreen.style.display = 'none';
    }

    // Simulate API response after 1 second
    function simulateAPIResponse() {
        setTimeout(function () {
            hideLoadingScreen();
            showResultsScreen();
        }, 1000); // 1000 milliseconds = 1 second
    }

    // Results Section
    function showResultsScreen() {
        var resultsScreen = document.getElementById('results');
        resultsScreen.style.display = 'block';
    }

    function hidePopup() {
        var popup = document.getElementById('popup');
        popup.style.display = 'none';
    }

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
});