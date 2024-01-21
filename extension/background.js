chrome.runtime.onMessage.addListener((data, sender, sendResponse) => {
    if (data.data[0] == 1) {
        console.log(data);

        fetchDataFromApi("gschol")
            .then(data => {
                console.log(data)
                chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
                    chrome.tabs.sendMessage(tabs[0].id, {data: [2, data]});
                });
            })
            .catch(error => {
                console.error('API request failed', error);
                // Handle errors and notify the popup
            });
    }
});

// chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
//     if (request.action == "startApiRequest") {
//       // Show loading screen or spinner in the popup
//       chrome.browserAction.setPopup({ popup: 'loading-screen.html' });

//       // Perform the API request and send data back to the content script
//       fetchDataFromApi(message.option)
//           .then(data => {
//               // Send data back to the popup
//               chrome.browserAction.setPopup({ popup: 'results.html' });
//               chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
//                   const activeTab = tabs[0];
//                   chrome.tabs.sendMessage(activeTab.id, { action: 'displayData', data });
//               });
//           })
//           .catch(error => {
//               console.error('API request failed', error);
//               // Handle errors and notify the popup
//           });
//   }
// });

function fetchDataFromApi(option) {
    // Local host server URL
    const apiUrl = 'http://127.0.0.1:5000/test';

    // Data for the POST request
    const postData = {
        source: option,
        query: 'test'
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


