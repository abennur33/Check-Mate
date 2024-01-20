document.addEventListener('DOMContentLoaded', function () {
    var selectedOption;

    document.getElementById('check-button').addEventListener('click', function () {
        // Get the selected option
        selectedOption = document.querySelector('input[name="options"]:checked').value;
        console.log(selectedOption);

        // Send a message to the background script to initiate the API request
        // In popup.js
        chrome.runtime.sendMessage(activeTab.id, { action: 'startApiRequest', option: selectedOption });
    });
});