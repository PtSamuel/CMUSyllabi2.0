from Crawler.Utils import get_and_unwrap
from Crawler.Data import SyllabusRegistry
from Crawler.Constants import Constants
from Crawler.Parallel import Parallel

def main():
    try:        
        # Store to avoid accessing this page multiple times.
        print('Fetching syllabus registry base url:', Constants.CMU_SYLLABUS_REGISTRY_URL.value)
        html = get_and_unwrap(Constants.CMU_SYLLABUS_REGISTRY_URL.value)
        sr = SyllabusRegistry(html=html, ignore_archived=True)
        
        manager = Parallel()

        for s in sr.semesters:
            for d in s.departments:
                d.get(manager=manager)
                print(f'Creating task for courses under {s}, {d}.')
            break
        manager.wait()
        breakpoint()
        
        for s in sr.semesters:
            for d in s.departments:
                for c in d.courses['Available Syllabi']:
                    print(f'Fetching course {c} under {s}, {d}')
                    c.get(manager=manager)
            break
        manager.wait()
        breakpoint()
        
    except Exception as e:
        print(e)
        breakpoint()
    
if __name__ == '__main__':
    main()
