document.addEventListener('DOMContentLoaded', function () {
    // Show loading screen
    showLoadingScreen();

    // Get the active tab ID
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        const activeTabId = tabs[0].id;

        // Listen for messages from the background script
        chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
            if (message.action === 'apiResponse' && sender.tab.id === activeTabId) {
                // API response received, hide loading screen and proceed to results
                hideLoadingScreen();
                window.location.href = chrome.runtime.getURL('results.html');
            }
        });
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
