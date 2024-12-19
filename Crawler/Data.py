from dataclasses import dataclass
from urllib.parse import urljoin
import json
from bs4 import BeautifulSoup
import re

from .Constants import Constants
from .Utils import get_and_unwrap, select_unique, WebDriver, WebDriverException, index_back

@dataclass
class Immediate:
    syllabus_url: str
    file_name: str
    
@dataclass
class Webpage:
    webpage_url: str

class Course:
    def __init__(self, name, href):
        self.name = name
        try:
            self.acronym = re.search(r'\d{5}(-\w*)?', name).group()
        except:
            self.acronym = name
            print(f'Failed to acronymize course {name}.')
        self.href = urljoin(Constants.CMU_CANVAS_URL.value, href)
        self.processed = False
        self.archive = None
    def __repr__(self):
        return self.name
    def get(self):
        html = get_and_unwrap(self.href, cookies=Constants.COOKIE.value)
        if html is not None:
            self.processed = True
            self.archive = self.analyze(html)
            if self.archive is None:
                print('abnormal:', self.href)       
    def analyze(self, html):
        try:
            # Immediate
            syllabus_url = select_unique(html, 'div#content a').get('href')
            file_name = select_unique(html, 'div#content h2').getText()
            return Immediate(syllabus_url, file_name)
        except: 
            pass
        try:
            select_unique(html, 'div#wiki_page_show')
            return Webpage(self.href)
        except:
            pass
        return None
    def __reduce__(self):
        return (
            self.__class__.__new__,
            (self.__class__,),
            {
                'name': self.name,
                'acronym': self.acronym,
                'href': self.href,
                'processed': self.processed,
                'archive': self.archive
            }
        )
    
class Department:
    def __init__(self, name, href):
        self.name = name
        try:
            self.acronym = name[index_back(name, '(') + 1:index_back(name, ')')]
        except:
            self.acronym = name
            print(f'Failed to acronymize department {name}.')
        self.href = href
        self.processed = False
        self.courses = None
    def __repr__(self):
        return self.name
    @staticmethod
    def get_category(html, cat: str):
        courses = html.select(f'div[aria-label="{cat}"] > div.content > ul.context_module_items > li[id^="context_module_item_"] > div.ig-row > div.ig-info > div.module-item-title > span.item_name > a.ig-title')
        return [Course(c.get('title'), c.get('href')) for c in courses]
    def get(self):
        html = get_and_unwrap(self.href, cookies=Constants.COOKIE.value)
        if html is not None:
            self.courses = {cat: self.get_category(html, cat) for cat in Constants.COURSE_CATEGORIES.value} 
            self.processed = True
    @property
    def course_count(self):
        if self.courses is None:
            return 0
        return len(self.courses['Available Syllabi']) + len(self.courses['Individualized Experiences'])
    def __reduce__(self):
        return (
            self.__class__.__new__,
            (self.__class__,),
            {
                'name': self.name,
                'acronym': self.acronym,
                'href': self.href,
                'processed': self.processed,
                'courses': self.courses
            }
        )

class Semester:
    def __init__(self, html):
        name = html.get('aria-label')
        self.name = name
        try:
            self.acronym = name[index_back(name, '(') + 1:index_back(name, ')')]
        except:
            self.acronym = name
            print(f'Failed to acronymize semester {name}.')
        departments = html.select('div.content > ul.context_module_items > li[id^="context_module_item_"] > div.ig-row > div.ig-info > div.module-item-title > span.item_name > a.external_url_link')
        self.departments = [Department(d.get('title'), d.get('href')) for d in departments]
    def __repr__(self):
        return self.name
    def __reduce__(self):
        return (
            self.__class__.__new__,
            (self.__class__,),
            {
                'name': self.name,
                'acronym': self.acronym,
                'departments': self.departments
            }
        )
    
class ArchivedSemester:
    def __init__(self, name, href, use_js=True):
        self.name = name
        self.acronym = name[index_back(name, '(') + 1:index_back(name, ')')]
        self.href = urljoin(Constants.CMU_CANVAS_URL.value, href)
        print(F'Fetching {self.name} @ {self.href}.')
        if use_js:
            html = get_and_unwrap(self.href)
            # Second <script>.
            script = html.select('script')[1].getText()
            # Select definition of variable 'ENV'.
            script = script[script.index('ENV'):script.index('BRANDABLE_CSS_HANDLEBARS_INDEX')]
            # Strip away trailing characters.
            script = script[script.index('{'):index_back(script, ';')]
            page = json.loads(script)
            soup = BeautifulSoup(page['WIKI_PAGE']['body'], 'html.parser')
            departments = soup.select('a')
            self.departments = [Department(d.getText(), d.get('href')) for d in departments]
        else:
            try:
                driver = WebDriver(url=self.href)
                html = driver.html
                driver.close()    
                departments = html.select('div#wiki_page_show > div.show-content > p > a')
                self.departments = [Department(d.getText(), d.get('href')) for d in departments]
                print(f'Found {len(self.departments)} departments.')
            except WebDriverException:
                print(f'Failed to fetch {self.name} @ {self.href}, skipping.')
                self.departments = []
    def __repr__(self):
        return self.name
    def __reduce__(self):
        return (
            self.__class__.__new__,
            (self.__class__,),
            {
                'name': self.name,
                'acronym': self.acronym,
                'href': self.href,
                'departments': self.departments
            }
        )

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
    def __reduce__(self):
        return (
            self.__class__.__new__,
            (self.__class__,),
            {
                'semesters': self.semesters
            }
        )
