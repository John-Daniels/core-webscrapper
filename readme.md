# CORE Web Scraper

## Overview

The CORE Web Scraper is a Python-based application designed to extract research articles from the CORE database, specifically focusing on articles related to biology. This tool retrieves metadata, including titles, authors, publication venues, and PDF links, and allows users to download the associated PDFs.

## Features

- Scrapes article metadata (title, authors, publication venue, etc.) from multiple pages.
- Downloads PDF files of the scraped articles.
- Easy to configure and extend for different queries.

## Installation

To run this project, you need to install the required Python packages listed in `requirements.txt`. Follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/core-webscraper.git
   cd core-webscraper
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Project

1. **Start the script:**
   ```bash
   python scraper.py
   ```

   This will initiate the scraping process, and the program will run until it has scraped the specified number of pages or until no more articles are found.

2. **Output:**
   The scraped articles will be printed to the console, and any downloadable PDFs will be saved in the `./output/` directory.

## How the Project Works

- **WebDriver Initialization:** The script uses Selenium WebDriver with Chrome to navigate through the CORE website. Ensure you have the Chrome browser and the appropriate WebDriver installed for compatibility.

- **Scraping Articles:** The `scrape_articles` function retrieves article information by locating the relevant HTML elements using CSS selectors and XPath. It collects:
  - Title and link to the article.
  - List of authors.
  - Publication venue and date.
  - PDF download link.

- **PDF Downloading:** The `download_pdf` function downloads the PDF files by making HTTP requests to the URLs obtained during scraping. It checks if the PDF link is available and saves it with a sanitized filename in the output directory.

- **Pagination Handling:** The script iterates through the specified number of pages, scraping each for articles until it reaches the limit or finds no more articles.

- **Error Handling:** Basic error handling is included to manage exceptions during scraping and downloading processes.

## Contributing

Contributions are welcome! If you have suggestions or improvements, please submit a pull request or open an issue.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.