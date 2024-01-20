document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('check-button').addEventListener('click', function () {
        window.location.href = chrome.runtime.getURL('results.html');
    });
});