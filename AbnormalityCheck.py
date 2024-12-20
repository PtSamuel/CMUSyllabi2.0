import pickle
sr = pickle.load(open('syllabus_registry.pkl', 'rb'))
for s in sr.semesters:
    for d in s.departments:
        if d.processed:
            if d.course_count == 0:
                pass
                # print(f'Zero course found in department {d} @ {d.href} under {s}.')
            for c in d.courses['Available Syllabi'] + d.courses['Individualized Experiences']:
                if c.processed: 
                    if c.archive is None:
                        print(f'Abnormal archive: course {c} @ {c.href} under {s}, {d}.')
                else:
                    print(f'Unprocessed course {c} @ {c.href} under {s}, {d}.')
        else:
            print(f'Unprocessed department {d} @ {d.href} under {s}.')

