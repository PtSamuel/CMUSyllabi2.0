import pickle
import argparse

from Crawler.Utils import get_and_unwrap
from Crawler.Data import SyllabusRegistry
from Crawler.Constants import Constants
from Crawler.Parallel import Parallel

def main(args):
    try:        
        # Store to avoid accessing this page multiple times.
        print('Fetching syllabus registry base url:', Constants.CMU_SYLLABUS_REGISTRY_URL.value)
        html = get_and_unwrap(Constants.CMU_SYLLABUS_REGISTRY_URL.value)
        
        if args.debug:
            sr = SyllabusRegistry(html=html, ignore_archived=True)
            semesters = sr.semesters[:1]
        else:
            sr = SyllabusRegistry(html=html, ignore_archived=False)
            semesters = sr.semesters
        
        manager = Parallel()

        for s in semesters:
            for d in s.departments:
                print(f'Creating task for courses under {s}, {d}.')
                def action(dep):
                    dep.get()
                manager.add(action, d)
        manager.wait()
        
        if args.debug:
            breakpoint()
        
        for s in semesters:
            for d in s.departments:
                for c in d.courses['Available Syllabi']:
                    print(f'Fetching course {c} under {s}, {d}')
                    def action(course):
                        course.get()
                    manager.add(action, c)
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
    parser = argparse.ArgumentParser(prog='Runner')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()
    main(args)
