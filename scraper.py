from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import requests
from fake_useragent import UserAgent
import time
import os
import random

# Configure ChromeDriver options
options = Options()
options.headless = False  # Set to True if you want to run it in headless mode
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--disable-infobars')
options.add_argument('--disable-extensions')

# Path to your ChromeDriver
service = Service("/usr/bin/chromedriver")

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

def download_pdf(url, file_name):
    """
    Download a PDF file from the given URL and save it locally.

    :param url: URL of the PDF file.
    :param file_name: Local file name to save the PDF.
    :return: None
    """
    try:
        # Use a fake user agent to mimic a browser
        headers = {
            "User-Agent": UserAgent().random,
            "Referer": "https://scholar.google.com/"
        }
        response = requests.get(url, headers=headers, stream=True)
        
        if response.status_code == 200:
            with open(file_name, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Saved {file_name}")
        else:
            print(f"Failed to download {url}. HTTP status: {response.status_code}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def scrape_google_scholar_pdfs(query, download_folder, max_retries=15):
    """
    Function to scrape PDF links from Google Scholar search results.

    :param query: The search keyword for Google Scholar.
    :param download_folder: The folder where PDFs will be saved.
    :param max_retries: Number of retries for handling stale elements.
    """
    try:
        # Open Google Scholar
        driver.get("https://scholar.google.com/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
        
        # Enter the search query
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.submit()
        
        # Wait for search results to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "gs_res_ccl_mid")))
        time.sleep(2)

        # Create download folder if it doesn't exist
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        # Loop through search results to find PDF links
        pdf_count = 1
        while True:
            try:
                # Refetch all PDF links on the current page
                pdf_links = driver.find_elements(By.PARTIAL_LINK_TEXT, "[PDF]")

                if not pdf_links:
                    print("No more PDF links found on this page.")
                
                for pdf_link in pdf_links:
                    retries = 0
                    while retries < max_retries:
                        try:
                            # Wait for the PDF link to be visible before clicking
                            WebDriverWait(driver, 10).until(EC.visibility_of(pdf_link))
                            
                            # Move to the element to avoid stale errors
                            actions = ActionChains(driver)
                            actions.move_to_element(pdf_link).perform()
                            
                            pdf_link_href = pdf_link.get_attribute("href")
                            
                            if pdf_link_href and pdf_link_href.endswith(".pdf"):
                                print(f"Downloading PDF {pdf_count}: {pdf_link_href}")
                                file_name = os.path.join(download_folder, f"paper_{pdf_count}.pdf")
                                download_pdf(pdf_link_href, file_name)
                                pdf_count += 1
                                
                            break  # Exit retry loop on success
                        
                        except StaleElementReferenceException:
                            print(f"Stale element encountered. Retrying ({retries + 1}/{max_retries})...")
                            retries += 1
                            time.sleep(2)
                    
                    if retries == max_retries:
                        print(f"Failed to download PDF {pdf_count} due to stale element.")

                # Check for "Next" button and navigate
                next_button = driver.find_elements(By.LINK_TEXT, "Next")
                if next_button:
                    print("Moving to the next page...")
                    driver.execute_script("arguments[0].click();", next_button[0])
                    time.sleep(random.uniform(3, 7))  # Random delay to avoid detection
                else:
                    print("No more pages available.")
                    break  # Exit the loop

            except Exception as e:
                print(f"An error occurred while processing the page: {e}")
                break

    except TimeoutException:
        print("Timeout while loading Google Scholar.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

# Example usage
if __name__ == "__main__":
    query = "Artificial Intelligence research papers"
    download_folder = "./scholar_pdfs"
    scrape_google_scholar_pdfs(query, download_folder)
