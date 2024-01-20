chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action == "startApiRequest") {
      // Show loading screen or spinner in the popup
      chrome.browserAction.setPopup({ popup: 'loading-screen.html' });

      // Perform the API request and send data back to the content script
      fetchDataFromApi(message.option)
          .then(data => {
              // Send data back to the popup
              chrome.browserAction.setPopup({ popup: 'results.html' });
              chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
                  const activeTab = tabs[0];
                  chrome.tabs.sendMessage(activeTab.id, { action: 'displayData', data });
              });
          })
          .catch(error => {
              console.error('API request failed', error);
              // Handle errors and notify the popup
          });
  }
});

function fetchDataFromApi(option) {
  // Local host server URL
  const apiUrl = 'http://127.0.0.1:5000/test';

  // Parameters for the API call
  const params = {
      option: option,
      otherParameter: 'test'
  };

  // Construct the query string
  const queryString = new URLSearchParams(params).toString();

  // Construct the full URL with query string
  const fullUrl = `${apiUrl}?${queryString}`;

  // Make the API call
  return fetch(fullUrl)
      .then(response => {
          if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json();
      });
}

