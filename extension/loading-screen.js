document.addEventListener('DOMContentLoaded', function () {
    // Show loading screen
    showLoadingScreen();

    chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
        if (request.data[0] == 2) {
            console.log("message sent to loading screen")
            // API response received, hide loading screen and proceed to results
            hideLoadingScreen();
            window.location.href = chrome.runtime.getURL('results.html');
        }
    });
});

function showLoadingScreen() {
    var loadingScreen = document.querySelector('.ring');
    loadingScreen.style.display = 'block';
}

function hideLoadingScreen() {
    var loadingScreen = document.querySelector('.ring');
    loadingScreen.style.display = 'none';
}
