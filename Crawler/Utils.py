import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .Constants import Constants

def get_and_unwrap(*args, **kwargs) -> BeautifulSoup:
    try:
        response = requests.get(*args, **kwargs)
        assert response.status_code != 401
        return BeautifulSoup(response.text, 'html.parser')
    except:
        return None

def select_unique(html, *args, **kwargs):
    result = html.select(*args, **kwargs)
    assert len(result) == 1, 'Selection is not unique!'
    return result[0]

def index_back(s, c):
    for i in reversed(range(len(s))):
        if s[i] == c:
            return i
    return -1

class WebDriverException(Exception):
    pass

class WebDriver:
    def __init__(self, url=None, headless=True):
        options = Options()
        if headless:
            options.add_argument("--headless")
        
        self.driver = None
        try:
            print('Creating driver.')
            driver = webdriver.Chrome(options=options)
        except:
            raise WebDriverException('Failed to create driver.')
        try:
            print('Visiting dummy domain.')
            driver.get('https://httpbin.org/headers')
            driver.add_cookie({'name': list(Constants.COOKIE.value.keys())[0], 'value': list(Constants.COOKIE.value.values())[0]})
        except:
            raise WebDriverException('Failed to set cookies.')    
        self.driver = driver
        if url is not None:
            self.get(url)
    @property
    def sanity(self):
        return self.driver is not None
    def get(self, url):
        assert self.sanity, 'Driver is abnormal.'
        try:
            print(f'Visiting {url}') 
            self.driver.get(url)
        except:
            raise WebDriverException(f'Failed to go to {url}.')
    @property
    def html(self):
        assert self.sanity, 'Driver is abnormal.'
        return BeautifulSoup(self.driver.page_source, 'html.parser')
    def close(self):
        assert self.sanity, 'Driver is abnormal.'
        self.driver.close()
