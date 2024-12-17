from Crawler.Utils import get_and_unwrap
from Crawler.Data import SyllabusRegistry
from Crawler.Constants import Constants

def main():
        
    # Store to avoid accessing this page multiple times.
    html = get_and_unwrap(Constants.CMU_SYLLABUS_REGISTRY_URL.value)
    sr = SyllabusRegistry(html=html)

    for s in sr.semesters:
        for d in s.departments:
            d.get()
            print('Fetching {f}, {d}.')
    
    for s in sr.semesters:
        for d in s.departments:
            for c in d.courses['Available Syllabi']:
                c.get()
                archive = c.analyze(c.result)
                if archive == None:
                    print('abnormal:', c.href)
                else:
                    print(archive)

if __name__ == '__main__':
    main()
