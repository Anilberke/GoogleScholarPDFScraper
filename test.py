from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Set up Chrome options
options = Options()
options.headless = True  # Run Chrome in headless mode (without a GUI)

# Specify the path to your ChromeDriver
service = Service("/usr/bin/chromedriver")

# Initialize the Chrome driver using the Service object
driver = webdriver.Chrome(service=service, options=options)

# Navigate to Google's homepage
driver.get("https://google.com/")

# Print the title of the page
print(driver.title)

# Close the browser
driver.quit()


