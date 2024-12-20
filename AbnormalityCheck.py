import pickle
sr = pickle.load(open('syllabus_registry.pkl', 'rb'))
for s in sr.semesters:
    for d in s.departments:
        if d.processed:
            for c in d.courses['Available Syllabi'] + d.courses['Individualized Experiences']:
                if c.processed and c.archive is None:
                    print(c)
