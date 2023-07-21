// background.js
chrome.browserAction.onClicked.addListener(function(tab) {
  // Get the URL and title of the current active tab
  const url = tab.url;
  const title = tab.title;

  // Create the payload data
  const data = {
    url: url,
    title: title
  };

  // Send a POST request to the server
  fetch('http://localhost:38582/report', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
    .then(response => {
      // Handle the response if needed
    })
    .catch(error => {
      // Handle any errors
      console.error('Error:', error);
    });
});
