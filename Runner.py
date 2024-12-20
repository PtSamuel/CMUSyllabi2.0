import pickle
import argparse
from tqdm import tqdm
import traceback

from Crawler.Utils import get_and_unwrap
from Crawler.Data import SyllabusRegistry, Status
from Crawler.Constants import Constants
from Crawler.Parallel import Parallel

def main(args):
    
    try:        
        
        if args.checkpoint is not None:
            print(f'Loading checkpoint: {args.checkpoint}.')
            sr = pickle.load(open(args.checkpoint, 'rb'))
        else:
            # Store to avoid accessing this page multiple times.
            print(f'Fetching syllabus registry base url: {Constants.CMU_SYLLABUS_REGISTRY_URL.value}.')
            html = get_and_unwrap(Constants.CMU_SYLLABUS_REGISTRY_URL.value)
            sr = SyllabusRegistry(html=html, ignore_archived=args.debug)
                
        if args.debug:
            semesters = sr.semesters[:1]
        else:
            semesters = sr.semesters
        
        manager = Parallel()

        if args.checkpoint is None:
            print('Creating a job for every semester.')
            pbar = tqdm(total=sum(len(semester.departments) for semester in semesters))
            for s in semesters:
                for d in s.departments:
                    pbar.set_description(f'{s.acronym}-{d.acronym}')
                    pbar.update()
                    def action(dep):
                        dep.get()
                    manager.add(action, d)
            manager.wait()
        
        if args.debug:
            breakpoint()
        
        print('Creating a job for every course.')
        pbar = tqdm(total=sum(sum(department.course_count for department in semester.departments) for semester in semesters))
        for s in semesters:
            for d in s.departments:
                if d.status == Status.SUCCESS:
                    for c in d.courses['Available Syllabi'] + d.courses['Individualized Experiences']:
                        pbar.set_description(f'{s.acronym}-{c.acronym}')
                        pbar.update()
                        def action(course):
                            course.get()
                        manager.add(action, c)
                else:
                    print(f'Department {d} under {s} is not visited or failed, skipping.')
                    
        manager.wait()
        
    except Exception as e:
        print(f'Encountered error: {e}.')
        traceback.print_exc()
        breakpoint()
    
    print('Pickling checkpoint.')
    try:
        with open('syllabus_registry.pkl', 'wb') as pkl:
            pickle.dump(sr, pkl, pickle.HIGHEST_PROTOCOL)
    except:
        print('Failed to pickle.')
        breakpoint()
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Runner')
    parser.add_argument('-c', '--checkpoint')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()
    main(args)
