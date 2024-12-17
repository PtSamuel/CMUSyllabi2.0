from dataclasses import dataclass
from urllib.parse import urljoin

from .Constants import Constants
from .Utils import get_and_unwrap, select_unique, WebDriver

@dataclass
class Immediate:
    syllabus_url: str
    file_name: str
    
@dataclass
class Webpage:
    webpage_url: str

class Course:
    def __init__(self, name, href, cat : str='Available Syllabi'):
        self.name = name
        self.href = urljoin(Constants.CMU_CANVAS_URL.value, href)
        self.cat = cat
    def __repr__(self):
        return self.name
    def get(self):
        self.result = get_and_unwrap(self.href, cookies=Constants.COOKIE.value)
    def analyze(self, html):
        archive = None
        try:
            # Immediate
            syllabus_url = select_unique(html, 'div#content a').get('href')
            file_name = select_unique(html, 'div#content h2').getText()
            archive = Immediate(syllabus_url, file_name)
        except: 
            pass
        
        try:
            select_unique(html, 'div#wiki_page_show')
            archive = Webpage(self.href)
        except:
            pass
        self.archive = archive
        return archive
    
class Department:
    def __init__(self, name, href):
        self.name = name
        self.href = href
    def __repr__(self):
        return self.name
    @staticmethod
    def get_category(html, cat: str):
        courses = html.select(f'div[aria-label="{cat}"] > div.content > ul.context_module_items > li[id^="context_module_item_"] > div.ig-row > div.ig-info > div.module-item-title > span.item_name > a.ig-title')
        return [Course(c.get('title'), c.get('href')) for c in courses]
    def get(self):
        html = get_and_unwrap(self.href, cookies=Constants.COOKIE.value)
        self.courses = {cat: self.get_category(html, cat) for cat in Constants.COURSE_CATEGORIES.value}

class Semester:
    def __init__(self, html):
        self.html = html
        departments = html.select('div.content > ul.context_module_items > li[id^="context_module_item_"] > div.ig-row > div.ig-info > div.module-item-title > span.item_name > a.external_url_link')
        self.departments = [Department(d.get('title'), d.get('href')) for d in departments]
    @property 
    def name(self):
        return self.html.get('aria-label')
    def __repr__(self):
        return self.name
    
class ArchivedSemester:
    def __init__(self, name, href):
        self.name = name
        self.href = urljoin(Constants.CMU_CANVAS_URL.value, href)
        driver = WebDriver(url=self.href)
        html = driver.html
        driver.close()
        departments = html.select('div#wiki_page_show > div.show-content > p > a')
        self.departments = [Department(d.getText(), d.get('href')) for d in departments]
    def __repr__(self):
        return self.name

class SyllabusRegistry:
    def __init__(self, html=None, ignore_archived=False):
        if html is None:
            html = get_and_unwrap(Constants.CMU_SYLLABUS_REGISTRY_URL.value)
        self.html = html
        semesters = html.select('div[aria-label^="Fall"], div[aria-label^="String"], div[aria-label^="Summer"]')
        self.semesters = [Semester(s) for s in semesters]
        
        if not ignore_archived:
            archived_semesters = html.select('div[aria-label="Archive"] > div.content > ul > li > div.ig-row > div.ig-info > div.module-item-title > span.item_name > a')
            self.semesters += [ArchivedSemester(s.get('title'), s.get('href')) for s in archived_semesters]
