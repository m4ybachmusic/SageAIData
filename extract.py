import csv
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# Define the CSV filename
csv_filename = "content_data2.csv"

# Initialize the CSV with headers if it doesn't already exist
def initialize_csv(filename):
    try:
        with open(filename, mode='x', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["URL", "Content Type", "Topic", "Subtopic", "Content"])
            print(f"{filename} created with headers.")
    except FileExistsError:
        print(f"{filename} already exists. Skipping initialization.")

# Function to save extracted content to CSV
def save_content_to_csv(data, filename):
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([data['url'], data['content_type'], data['topic'], data['subtopic'], data['content']])
    print(f"Data saved to {filename} for URL: {data['url']}")

# Function to extract content from static websites
def extract_static_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            content = ' '.join(p.get_text(strip=True) for p in paragraphs)
            return content
        else:
            print(f"Failed to retrieve content from {url}. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Request error for {url}: {e}")
        return None

# Function to extract content from dynamic websites using Playwright
def extract_dynamic_content(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=10000)
            page.wait_for_selector('body', timeout=10000)
            content = page.content()
            browser.close()
            soup = BeautifulSoup(content, 'html.parser')
            paragraphs = soup.find_all('p')
            return ' '.join(p.get_text(strip=True) for p in paragraphs)
    except Exception as e:
        print(f"Failed to retrieve dynamic content from {url}: {e}")
        return None

# Main function to handle extraction and saving
def extract_and_save(url, content_type, topic, subtopic, filename):
    if content_type == 'static':
        content = extract_static_content(url)
    elif content_type == 'dynamic':
        content = extract_dynamic_content(url)
    else:
        print("Invalid content type. Choose 'static' or 'dynamic'.")
        return

    if content:
        data = {
            'url': url,
            'content_type': content_type,
            'topic': topic,
            'subtopic': subtopic,
            'content': content
        }
        save_content_to_csv(data, filename)
    else:
        print(f"Content extraction failed for {url}.")
    
# extract_and_save("https://www.verywellmind.com/generalized-anxiety-disorder-4166193", "dynamic", "Mental Health", "Generalized Anxiety Disorder", csv_filename)
