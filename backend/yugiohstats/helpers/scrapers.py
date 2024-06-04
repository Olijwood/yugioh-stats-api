from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def scrape_yugioh_sets(url):
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    with webdriver.Chrome(options=chrome_options) as driver:
        driver.get(url)
        wait = WebDriverWait(driver, 15)
        try:
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'magicSets')))
            html = driver.page_source
        except TimeoutException:
            print("Timed out waiting for element to be visible")
            return None

    soup = BeautifulSoup(html, 'html.parser')
    print('scraped html soup')
    return soup