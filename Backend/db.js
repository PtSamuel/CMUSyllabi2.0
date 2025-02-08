const sqlite3 = require('sqlite3').verbose();
syllabus_registry_path = '../syllabus_registry.sqlite';

const db = new sqlite3.Database(syllabus_registry_path, (err) => {
    if(err) {
        console.error(`Error opening ${syllabus_registry_path}:`, err);
    } else {
        console.log(`Successfully opened ${syllabus_registry_path}`);
    }
});

function find_course(course_number, callback) {
    const is_five_digit_string = /^\d{5}$/.test(course_number); 
    if(!is_five_digit_string) {
        json = { argument_err: `Argument course_number (${course_number}) is not a 5-digit string` };
        console.log(json);
        callback(json);
        return;
    }
    const sql = `
        select 
            semesters.acronym as semester, 
            departments.acronym as department, 
            courses.name as course_number, 
            courses.syllabus_category as category, 
            courses.href as syllabus_href 
        from courses 
        inner join departments on courses.department_id = departments.department_id 
        inner join semesters on departments.semester_id = semesters.semester_id 
        where courses.name like ?
    `;
    db.all(sql, [`%${course_number}%`], (err, rows) => {
        if(err) {
            json = { database_err: err };
            console.log(json);
            callback(json);
        } else {
            console.log(rows[0]);
            callback(rows);
        }
    });
}

function find(course_title, department, semester, callback) {
    if(course_title === undefined) {
        json = { argument_err: `Argument course_title (${course_title}) is empty` };
        console.log(json);
        callback(json);
        return;
    }
    const sql = `
        select 
            semesters.acronym as semester, 
            departments.acronym as department, 
            courses.name as course_number, 
            courses.syllabus_category as category, 
            courses.href as syllabus_href 
        from courses 
        inner join departments on courses.department_id = departments.department_id 
        inner join semesters on departments.semester_id = semesters.semester_id 
        where courses.name like ? 
            and (departments.acronym = ? or ? is null) 
            and (semesters.acronym = ? or ? is null) 
    `;
    console.log(sql);
    db.all(sql, [`%${course_title}%`, department, department, semester, semester], (err, rows) => {
        if(err) {
            json = { database_err: err };
            console.log(json);
            callback(json);
        } else {
            console.log(rows[0]);
            callback(rows);
        }
    });
}

module.exports = {
    find_course,
    find,
};