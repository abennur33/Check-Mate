chrome.runtime.onInstalled.addListener(function () {
    chrome.contextMenus.create({
      id: "highlightText",
      title: "Highlight Text",
      contexts: ["selection"],
    });
  });