import sqlite3
import argparse
from Crawler.Data import ArchivedSemester, PDF, Webpage, Unknown, Status
from Crawler.Constants import Constants

def compose_instructions(department, department_id, cat):
    
    global conn
    global cursor

    instruction = '''
        INSERT INTO courses (name, acronym, href, department_id, category, syllabus_category, syllabus_href, syllabus_name) values (?, ?, ?, ?, ?, ?, ?, ?)
    '''
    data = []
    for c in department.courses[cat]:
        if c.status == Status.SUCCESS:
            archive = c.archive
            if archive is not None:
                # If processing is unsuccessful, do not insert.
                if isinstance(archive, PDF):
                    syllabus_category = 'PDF'
                    syllabus_href = archive.href
                    syllabus_name = archive.name
                elif isinstance(archive, Webpage):
                    syllabus_category = 'Webpage'
                    syllabus_href = archive.href
                    syllabus_name = None
                elif isinstance(archive, Unknown):
                    syllabus_category = 'Unknown'
                    syllabus_href = archive.href
                    syllabus_name = None
                else:
                    # Unreachable.
                    breakpoint()
                data.append(
                    (c.name, c.acronym, c.href, department_id, cat, syllabus_category, syllabus_href, syllabus_name)    
                )
    cursor.executemany(instruction, data)
    conn.commit()
   
def make_sqlite(pkl_path, sqlite_path):
    
    global conn
    global cursor

    conn = sqlite3.connect(sqlite_path)
    cursor = conn.cursor()

    create_database_script = f'''
        CREATE TABLE semesters (
            semester_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL, 
            acronym TEXT, 
            href TEXT, 
            archived INTEGER NOT NULL
        );
        PRAGMA foreign_keys = ON;
        CREATE TABLE departments (
            department_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL, 
            acronym TEXT, 
            href TEXT NOT NULL, 
            semester_id INTEGER, 
            FOREIGN KEY (semester_id) REFERENCES semesters (semester_id) ON DELETE CASCADE
        );
        CREATE TABLE courses (
            course_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL, 
            acronym TEXT, 
            href TEXT NOT NULL, 
            department_id INTEGER NOT NULL, 
            category TEXT NOT NULL CHECK(category in ({', '.join("'" + s + "'" for s in Constants.COURSE_CATEGORIES.value)})),
            syllabus_category TEXT CHECK(syllabus_category in ('PDF', 'Webpage', 'Unknown')), 
            syllabus_href TEXT, 
            syllabus_name TEXT, 
            FOREIGN KEY (department_id) REFERENCES departments (department_id) ON DELETE CASCADE
        );
    '''
    cursor.executescript(create_database_script)

    import pickle
    with open(pkl_path, 'rb') as f:
        sr = pickle.load(f) 

    for s in sr.semesters:
        cursor.execute('''
            INSERT INTO semesters (name, acronym, href, archived) values (?, ?, ?, ?)
        ''', (s.name, s.acronym, s.href if isinstance(s, ArchivedSemester) else None, int(isinstance(s, ArchivedSemester))))
        conn.commit()
        semester_id = cursor.lastrowid
        for d in s.departments:
            cursor.execute('''
                INSERT INTO departments (name, acronym, href, semester_id) values (?, ?, ?, ?)
            ''', (d.name, d.acronym, d.href, semester_id))
            conn.commit()
            department_id = cursor.lastrowid
            if d.status == Status.SUCCESS:
                assert d.courses is not None
                compose_instructions(d, department_id, 'Available Syllabi')
                compose_instructions(d, department_id, 'Individualized Experiences')
                
    conn.close()
                        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pkl_path', '-p')
    parser.add_argument('--sqlite_path', '-s')
    args = parser.parse_args()
    make_sqlite(args.pkl_path, args.sqlite_path)
    
if __name__ == '__main__':
    main()
                        