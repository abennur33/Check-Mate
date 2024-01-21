document.addEventListener('DOMContentLoaded', function () {
    var selectedOption;

    document.getElementById('check-button').addEventListener('click', function () {
        // Get the selected option
        selectedOption = document.querySelector('input[name="options"]:checked').value;
        console.log(selectedOption);

        window.location.href = chrome.runtime.getURL('loading-screen.html');

        // Send a message to the background script to initiate the API request
        // In popup.js
        chrome.tabs.query({
            active: true,
            currentWindow: true
        }, function(tabs) {
            chrome.scripting.executeScript({
                target: {
                    tabId: tabs[0].id
                },
                function: sendData,
            });
        });
        
        const sendData = async () => {        
            chrome.runtime.sendMessage({
                count: 12,
                data: [1]
            }, function(response) {
                console.log(response.received);
            });
        }
    });
});