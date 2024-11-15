# GoogleScholarPDFScraper
This Python script automates the process of searching for research papers on Google Scholar and downloading available PDF links to a specified folder. It uses Selenium for browser automation and requests for downloading PDFs. The script is designed to mimic human browsing behavior to avoid detection.

Features
Searches Google Scholar for a user-defined query.
Extracts and downloads PDF files linked in the search results.
Handles stale elements with a retry mechanism.
Supports headless browser mode for silent operation.
Saves downloaded PDFs in a user-specified folder.

Prerequisites
Python 3.7+
Required Python packages:
selenium
requests
fake_useragent
Google Chrome installed on your system.
ChromeDriver matching your Chrome version. Install it and ensure it is in your system's PATH or specify its path in the script.

Step 1 - Download Chrome
Update your packages.
```
sudo apt update
Download and install chrome
```
```
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
If you get 'wget' command not found, that means you do not have wget installed on your machine. Simply install it by running:
```
```
sudo apt install wget
```
Then you can install chrome from the downloaded file.
```
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f
```
Check Chrome is installed correctly.
```
google-chrome --version
```
This version is important, you will need it to get the chromedriver.

#Step 2 - Install Chromedriver
 Download Chromedriver But you need the correct version, so remember which version of chrome you have from 

step 1 above and download the correct chromedriver.

In my case, I had version 92.xx.xxx.xx.xx. So I need to click on the version that supports 92. Install the correct chromedriver

Download the version that is best suited for your operating system, for me (Running Ubuntu 20.04 on Digital Ocean VPS) - the correct version is chromedriver_linux64.zip. You need to right-click on the link and copy link. Install the correct chromedriver

Download the chromedriver in your VPS, make sure you replace this link with your link to match your version of chrome.
```
wget https://chromedriver.storage.googleapis.com/92.0.4515.107/chromedriver_linux64.zip
```
You will get a zip file, you need to unzip it:
```
unzip chromedriver_linux64.zip
```
Make sure you unzip the file in your current directory, you can ls to copy and paste the correct file to unzip.

You then need to move the file to the correct location, so you can find when you need it.
```
sudo mv chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver
```
#Step 3 - Test Installation
Run the command
```
chromedriver --url-base=/wd/hub
```
You should get feedback that chrome is working properly, but the best way to test this is with python. The following code will scrap google and return the title of the website. Create a python file and add the following code:
```
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()

options.headless = True

driver = webdriver.Chrome("/usr/bin/chromedriver", options=options)

driver.get("https://google.com/")
print(driver.title)
driver.quit()
```
Step 4: Install Selenium and Other Python Packages
Install the required packages using pip:

```
pip3 install selenium requests fake-useragent
```
Verify the installation:

```
python3 -c "import selenium; print('Selenium installed successfully!')"
```
Step 5: Configure the Script
Update the ChromeDriver path in the script if it’s not in your system PATH:

```
service = Service("/path/to/chromedriver")
```
Ensure the download_folder exists or will be created by the script:

```
download_folder = "./scholar_pdfs"
```
Update the query variable with your desired search term:

```
query = "Artificial Intelligence research papers"
```
Step 6: Run the Script
Run the script in the terminal:
```
python3 scholar_pdf_scraper.py
```
Disclaimer
This script is intended for educational and personal use only. Ensure compliance with Google Scholar's terms of service when using this tool.

