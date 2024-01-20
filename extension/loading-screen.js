document.addEventListener('DOMContentLoaded', function () {
    setTimeout(function () {
        window.location.href = chrome.runtime.getURL('results.html');
    }, 3000);

    setTimeout(function () {
        hideLoadingScreen();
    }, 3000);
});

function hideLoadingScreen() {
    var loadingScreen = document.querySelector('.ring');
    loadingScreen.style.display = 'none';
}
