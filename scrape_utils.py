from bs4 import BeautifulSoup as bs
import requests as req
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from logs import log


def get_soup(url):
    try:
        header = {'User-Agent': 'Mozilla/5.0'}
        ra = req.get(url, allow_redirects=True, timeout=10, headers=header)
        redirected_url = ra.url
        return bs(ra.text, 'html.parser'), redirected_url
    except Exception as e:
        return None, None


def get_selenium():
    service = Service(executable_path='/snap/bin/chromium.chromedriver')
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(45)
    return driver


def get_soup_with_selenium(url, driver):
    try:
        driver.get(url)
        page_source = driver.page_source
        soup = bs(page_source, 'html.parser')
        return soup, driver.current_url
    except WebDriverException:
        log('WebDriverException occurred')
        return None, None
    except Exception as e:
        log('Exception occurred')
        return None, None
