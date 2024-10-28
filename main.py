from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import requests
import time

# Create output directory if it doesn't exist
output_dir = './output/'
os.makedirs(output_dir, exist_ok=True)

# Initialize the WebDriver
driver = webdriver.Chrome()

# Base URL with page parameter
base_url = 'https://core.ac.uk/search/?q=science+AND+fieldsOfStudy%3A%22biology%22&page='


# Function to scrape articles
def scrape_articles():
    articles = []
    article_elements = driver.find_elements(By.CSS_SELECTOR, 'div.card-container-11P0y')

    for article_element in article_elements:
        try:
            # Title and link
            title_element = article_element.find_element(By.CSS_SELECTOR, 'h3.styles-title-1k6Ib a')
            title = title_element.text
            link = title_element.get_attribute('href')
        except Exception as e:
            title, link = "Not available", "Not available"
            print(f"Error retrieving title or link: {e}")

        # Authors
        authors = []
        author_elements = article_element.find_elements(By.CSS_SELECTOR, 'li[itemprop="author"]')
        for author in author_elements:
            authors.append(author.text if author.text else "Unknown")

        # Venue and publication date
        try:
            venue = article_element.find_element(By.XPATH,
                                                 './/dt[contains(text(), "Publication venue")]/following-sibling::dd').text
        except:
            venue = "Not available"

        try:
            publication_date = article_element.find_element(By.XPATH,
                                                            './/dt[contains(text(), "Publication date")]/following-sibling::dd').text
        except:
            publication_date = "Not available"

        # PDF link
        try:
            pdf_link = article_element.find_element(By.CSS_SELECTOR, 'figure.styles-thumbnail-1xurx a').get_attribute(
                'href')
        except:
            pdf_link = "Not available"

        # Append article data to the list
        articles.append({
            'title': title,
            'link': link,
            'authors': authors,
            'venue': venue,
            'publication_date': publication_date,
            'pdf_link': pdf_link,
        })

    return articles


# Function to download PDF files
def download_pdf(pdf_url, title):
    if pdf_url == "Not available":
        print(f"No PDF link available for: {title}")
        return

    try:
        response = requests.get(pdf_url)
        response.raise_for_status()  # Raise an error for bad responses

        # Clean the title for safe file naming
        safe_title = title.replace('/', '-')  # Replace any slashes in title
        pdf_filename = os.path.join(output_dir, f"{safe_title}.pdf")

        with open(pdf_filename, 'wb') as pdf_file:
            pdf_file.write(response.content)
        print(f"Downloaded: {pdf_filename}")

    except Exception as e:
        print(f"Error downloading {pdf_url}: {e}")


all_articles = []
page_number = 1
scrapping_limit = 10

while page_number <= scrapping_limit:
    # Load the URL for the current page
    print(f"Scraping page {page_number}...")
    driver.get(base_url + str(page_number))
    time.sleep(5)  # Wait for the page to load

    # Scrape articles on the current page
    articles = scrape_articles()

    # Stop if no articles are found on the current page (end of pagination)
    if not articles:
        print("No more articles found. Ending pagination.")
        break

    all_articles.extend(articles)
    page_number += 1

# Close the browser only after all pages are scraped
print("Scraping completed. Closing the browser.")
driver.quit()

# Print all articles found and download PDFs
for article in all_articles:
    print(article)
    download_pdf(article['pdf_link'], article['title'])
