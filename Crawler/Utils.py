import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .Constants import Constants

def get_and_unwrap(*args, **kwargs) -> BeautifulSoup:
    response = requests.get(*args, **kwargs)
    assert response.status_code == 200
    return BeautifulSoup(response.text, 'html.parser')

def select_unique(html, *args, **kwargs):
    result = html.select(*args, **kwargs)
    if result == []:
        return None
    assert len(result) == 1, 'Selection is not unique!'
    return result[0]

class WebDriver:
    def __init__(self, url=None, headless=True):
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        self.driver = driver
        driver.get('https://httpbin.org/headers')
        driver.add_cookie({'name': list(Constants.COOKIE.value.keys())[0], 'value': list(Constants.COOKIE.value.values())[0]})
        if url is not None:
            driver.get(url)
    def get(self, url):
        self.driver.get(url)
    @property
    def html(self):
        return BeautifulSoup(self.driver.page_source, 'html.parser')
    def close(self):
        self.driver.close()
