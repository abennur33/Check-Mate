# Meet your Check-Mate!

## Overview

Check-Mate is a digital fact-checking companion, designed as a Chrome extension, that empowers users to verify the accuracy of claims encountered on the web. The extension leverages fact-checking databases and scholarly sources to provide users with valuable insights into the credibility of highlighted text.

![Check-Mate Logo](extension/images/logo.png)

## Key Features

- **Text Highlighting:**
  - Users can use the extension just by highlighting text on a web page.

- **Fact-Checking Options:**
  - Users can choose to fact-check the highlighted claim against political/current events fact-checking databases or scientific and scholarly sources.

- **Accuracy Probability:**
  - The extension provides information on how likely the claim is to be accurate.

- **Source Attribution:**
  - Users are presented with a source that the accuracy probability is based on.

## Project Goals

We wanted to build an app that could use AI to empower people with a safeguard against the dangers of misinformation in the modern world. This tool can be beneficial to everyone but especially students, whether in elementary school or university.

## Team

- Aadit Bennur ([@abennur33](https://github.com/abennur33))
- Sahil Shaik ([@sahilshaik123](https://github.com/sahilshaik123))
- Jaidev Parhar ([@jaidevparhar](https://github.com/jaidevparhar))
- Henry Lee ([@LofiTea](https://github.com/LofiTea))

## How to Use

1. **Highlight Text:**
   - Select a piece of text on a web page.

2. **Use Check-Mate:**
   - Right-click on the highlighted text and choose the "Check-Mate" option.

3. **Fact-Checking Options:**
   - Select either political/current events fact-checking databases or scientific and scholarly sources.

4. **View Results:**
   - The extension provides information on the accuracy probability and the source it is based on.

## Installation

1. **Download Extension:**
   - Clone or download the Check-Mate repository to your local machine.

2. **Download Chrome Canary:**
   - Download the developer version of Chrome called "Chrome Canary".
   - This extension uses some beta technologies not available to stable Chrome.

3. **Load Extension:**
   - Open Chrome and navigate to `chrome://extensions/`.
   - Enable "Developer mode" in the top right corner.
   - Click "Load unpacked" and select the folder containing the extension files.

4. **Usage:**
   - Highlight text on a web page, right-click, and select the "Check-Mate" option to initiate fact-checking.
  
## Technical Specifications

This extension uses an HTML/CSS/JS framework for the popup menu while using a custom Flask-based API to provide the back-end computing. Based on HTTP inputs, the custom API uses two separate NLP models and web scraping to compare a claim against various databases. The confidence score is then returned back to the extension along with the source info it was based on.

## Contributing

Contributions are welcome! Please follow the [contribution guidelines](CONTRIBUTING.md).

## Boilermake XI Hackathon

This project was built for the Boilermake XI Hackathon.

## Issues

Report any issues or provide suggestions on the [GitHub Issues](https://github.com/your-username/check-mate-extension/issues) page.
