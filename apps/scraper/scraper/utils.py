from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def format_date(days, months, years):
    return date(int(years), int(months), int(days))


def chrome():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    return webdriver.Chrome(chrome_options=chrome_options)
