const sqlite3 = require('sqlite3').verbose();
syllabus_registry_path = '../syllabus_registry.sqlite';

const db = new sqlite3.Database(syllabus_registry_path, (err) => {
    if(err) {
        console.error(`Error opening ${syllabus_registry_path}:`, err);
    } else {
        console.log(`Successfully opened ${syllabus_registry_path}`);
    }
});

function find_course(course_number) {
    const is_five_digit_string = /^\d{5}$/.test(course_number); 
    if(is_five_digit_string) {
        return { err: `Argument course_number (${course_number}) is not a 5-digit string` };
    }
    const sql = `
        select semesters.acronym, departments.acronym, courses.name, courses.syllabus_category, courses.href from courses 
        inner join departments on courses.department_id = departments.department_id 
        inner join semesters on departments.semester_id = semesters.semester_id 
        where courses.name like '%?%'
    `;
    db.all(sql, [course_number], (err, rows) => {
        if(err) {
            console.log('Query failed:', err);
        } else {
            return rows;
        }
    });
}

modules.exports = {
    find_course,
};