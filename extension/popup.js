document.addEventListener('DOMContentLoaded', function () {
    var selectedOption;

    document.getElementById('button').addEventListener('click', function () {
        selectedOption = document.querySelector('input[name="options"]:checked').value;
        localStorage.setItem('selectedOption', selectedOption);
        hideLoadingScreen();
    });

    document.getElementById('check-button').addEventListener('click', function () {
        window.location.href = chrome.runtime.getURL('loading-screen.html?option=' + selectedOption);
    });

    function hideLoadingScreen() {
        var loadingScreen = document.querySelector('.ring');
        loadingScreen.style.display = 'none';
    }
});