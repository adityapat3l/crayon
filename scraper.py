from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_scraper():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path="./chromedriver", options=chrome_options)

    return driver

