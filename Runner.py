from Crawler.Utils import get_and_unwrap
from Crawler.Data import SyllabusRegistry
from Crawler.Constants import Constants
from Crawler.Parallel import Parallel

import pickle

def main():
    try:        
        # Store to avoid accessing this page multiple times.
        print('Fetching syllabus registry base url:', Constants.CMU_SYLLABUS_REGISTRY_URL.value)
        html = get_and_unwrap(Constants.CMU_SYLLABUS_REGISTRY_URL.value)
        sr = SyllabusRegistry(html=html, ignore_archived=True)
        
        manager = Parallel()

        for s in sr.semesters:
            for d in s.departments:
                print(f'Creating task for courses under {s}, {d}.')
                def action(dep):
                    dep.get()
                manager.add(action, d)
            break
        manager.wait()
        breakpoint()
        
        for s in sr.semesters:
            for d in s.departments:
                for c in d.courses['Available Syllabi']:
                    print(f'Fetching course {c} under {s}, {d}')
                    def action(course):
                        course.get()
                    manager.add(action, c)
            break
        manager.wait()
        
    except Exception as e:
        print(f'Encountered error: {e}.')
    
    print('Pickling checkpoint.')
    try:
        with open('syllabus_registry.pkl', 'wb') as pkl:
            pickle.dump(sr, pkl, pickle.HIGHEST_PROTOCOL)
    except:
        print('Failed to pickle.')
        breakpoint()
        
if __name__ == '__main__':
    main()
