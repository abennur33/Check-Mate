document.addEventListener('DOMContentLoaded', async () => {
    // Common code for all sections
    var selectedOption;

    // Popup Section
    var checkPoliticalButton = document.getElementById('button-political');
    var checkScientificButton = document.getElementById('button-scientific');


    if (checkPoliticalButton) {
        checkPoliticalButton.addEventListener('click', function () {
            hidePopup();
            showLoadingScreen();
            selectedOption = "snopes"
            callAPIResponse();
        });
    }

    if (checkScientificButton) {
        checkScientificButton.addEventListener('click', function () {
            hidePopup();
            showLoadingScreen();
            selectedOption = "gschol"
            callAPIResponse();
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
    function callAPIResponse() {
        chrome.runtime.sendMessage({ action: 'getAPIData', data: selectedOption}, response => {
            console.log(response);
            hideLoadingScreen();
            showResultsScreen();
            displayResults(response.data);
        });
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

        if (data.percent <= 40) {
            percentageBar.style.backgroundColor = '#FF5C5C';
            percentElement.textContent = (100 - data.percent) 
                + '% confident your claim is false.'
        } else if (data.percent > 41 && data.percent <= 70) {
            percentageBar.style.backgroundColor = '#FBFCA8';
            percentElement.textContent = data.percent 
                + '% confident your claim is true.'
        } else {
            percentageBar.style.backgroundColor = '#ACFCA8';
            percentElement.textContent = data.percent 
                + '% confident your claim is true.'
        }

        percentageBar.style.width = data.percent + '%';

        urlElement.innerHTML = `My Source: <a href="${data.url}" target="_blank">${data.url}</a>`;
    }
});