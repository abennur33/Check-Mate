var selection = "";
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'getAPIData') {
      // Retrieve the service info from local storage
        fetchDataFromApi(request.data, selection)
            .then(data => {
                console.log(data)
                sendResponse({data});
            })
            .catch(error => {
                console.error('API request failed', error);
                // Handle errors and notify the popup
            });

      return true; // Enable asynchronous response
    }
});

function fetchDataFromApi(option, text) {
    // Local host server URL
    const apiUrl = 'http://127.0.0.1:5000/search';

    // Data for the POST request
    const postData = {
        source: option,
        query: text
    };

    // Make the API call
    return fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // Add any additional headers if needed
        },
        body: JSON.stringify(postData),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        });
}

chrome.runtime.onInstalled.addListener(function () {
    chrome.contextMenus.create({
        title: "Open Popup",
        contexts: ["all"],
        id: "openPopup",
      });
  });

//   function handleContext(info, tab) {
//     const selectedText = info.selectionText;
//     console.log(selectedText)
//   }

  chrome.contextMenus.onClicked.addListener(function(info) {
    chrome.action.openPopup();
    selection = info.selectionText;
    console.log(selection);
  }
  );

//   const openPopup = async() => {
//     chrome.action.openPopup({});
//   }
  


