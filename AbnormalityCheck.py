import pickle
from Crawler.Data import Status

sr = pickle.load(open('syllabus_registry.pkl', 'rb'))
for s in sr.semesters:
    for d in s.departments:
        if d.status == Status.SUCCESS:
            if d.course_count == 0:
                pass
                # print(f'Zero course found in department {d} @ {d.href} under {s}.')
            for c in d.courses['Available Syllabi'] + d.courses['Individualized Experiences']:
                if c.status != Status.SUCCESS: 
                    print(f'Abnormal status {c.status} of course {c} @ {c.href} under {s}, {d}.')
        else:
            print(f'Unvisited or failed department {d} @ {d.href} under {s}.')


breakpoint()
