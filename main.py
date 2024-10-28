from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import requests

# Create output directory if it doesn't exist
output_dir = './output/'
os.makedirs(output_dir, exist_ok=True)

# Initialize the WebDriver
driver = webdriver.Chrome()  # or webdriver.Firefox() based on your browser
base_url = 'https://core.ac.uk/search/?q=science+AND+fieldsOfStudy%3A%22biology%22'
driver.get(base_url)

# Allow time for the page to load
time.sleep(5)  # Adjust as necessary

# Function to scrape articles
def scrape_articles():
    articles = []
    article_elements = driver.find_elements(By.CSS_SELECTOR, 'div.card-container-11P0y')

    for article_element in article_elements:
        title_element = article_element.find_element(By.CSS_SELECTOR, 'h3.styles-title-1k6Ib a')
        title = title_element.text
        link = title_element.get_attribute('href')

        # Get authors
        authors = []
        author_elements = article_element.find_elements(By.CSS_SELECTOR, 'li[itemprop="author"]')
        for author in author_elements:
            authors.append(author.text)

        # Use explicit waits for venue and publication date
        try:
            venue = WebDriverWait(article_element, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, './/dt[contains(text(), "Publication venue")]/following-sibling::dd'))
            ).text

            publication_date = WebDriverWait(article_element, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, './/dt[contains(text(), "Publication date")]/following-sibling::dd'))
            ).text

            # Get PDF link
            pdf_link = article_element.find_element(By.CSS_SELECTOR, 'figure.styles-thumbnail-1xurx a').get_attribute('href')

            # Append article data to the list
            articles.append({
                'title': title,
                'link': link,
                'authors': authors,
                'venue': venue,
                'publication_date': publication_date,
                'pdf_link': pdf_link,
            })

        except Exception as e:
            print(f"Error retrieving details for an article: {e}")

    return articles

# Function to download PDF files
def download_pdf(pdf_url, title):
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

# Scrape initial articles
articles = scrape_articles()
print("Articles found:", articles)

# Pagination logic
while True:
    try:
        # Wait for the next button to be clickable
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'ul.styles_pagination__2rBoj button:last-child'))
        )
        next_button.click()
        time.sleep(5)  # Wait for the next page to load

        # Scrape articles on the new page
        articles += scrape_articles()

    except Exception as e:
        print("No more pages or an error occurred:", e)
        break

# Close the browser
driver.quit()

# Print all articles found and download PDFs
for article in articles:
    print(article)
    download_pdf(article['pdf_link'], article['title'])