CMUCourses_href = 'https://courses.scottylabs.org/'

function get_acronym(semester_name) {
    let acronym;
    try {
        const [term, year] = semester_name.split(' ').filter(Boolean);
        switch (term) {
            case 'Fall':
                acronym = `F${year.substring(2, 4)}`;
                break;
            case 'Spring':
                acronym = `S${year.substring(2, 4)}`;
                break;
            default:
                break;
        }
    } catch {

    }
    return acronym;
}

function populate_table(course_number, table) {
    let tbody = table.querySelector('tbody');            
    let offerings = tbody.children;
    if(offerings.length > 0) {
        if(offerings[0].children[0].innerHTML.indexOf('</a>') != -1) {
            return;
        }
    }

    chrome.runtime.sendMessage({ course_number: course_number }, (response) => {
        if(response === undefined) {
            return;
        }
        if (response.data) {
            console.log(`${course_number}: ${response.data.length} syllabus entries.`);
            const syllabus_entries = response.data;
            
            let current;
            let count = 0;
            for(let i = 0; i < offerings.length; i++) {
                offering = offerings[i];
                semester = offering.children[0];
                semester_name = semester.innerHTML;
                
                const acronym = get_acronym(semester_name);
                if(acronym === undefined) {
                    console.error(`Unable to process semester name: ${semester_name}`);
                    continue;
                }
                
                if(current === undefined) {
                    current = acronym;
                    count = 0;
                } else if(current == acronym) {
                    count += 1;
                } else {
                    current = acronym;
                    count = 0;
                }
                const filtered = syllabus_entries.filter(entry => entry.semester == acronym);
                
                if(filtered.length == 0) {
                    const substitute = syllabus_entries.filter(
                        entry => entry.semester[0] == current[0]
                    );
                    if(count < substitute.length) {
                        console.log(count, substitute[count]);
                        semester.innerHTML = `<a class="letter-container substitute" target="_blank" href=${substitute[count].syllabus_href}>S</a> ${semester_name}`;
                    }

                } else {
                    if(count < filtered.length) {
                        console.log(count, filtered[count]);
                    }
                    semester.innerHTML = `<a class="letter-container match" target="_blank" href=${filtered[count].syllabus_href}>S</a> ${semester_name}`;
                }
            }
        } else {
            console.error('Error:', response.error);
        }
    });
}

function get_course_info(course) {
    course_data = course.children[0];
    course_number = course_data.querySelector('div > div > a > div > span')
    course_number = course_number.innerHTML.replaceAll('-', '');
    table = course.children[1];
    populate_table(course_number, table);
}

function run() {
    courses = document.querySelectorAll('div.bg-white.border-gray-100.rounded.border.p-6')
    if(courses.length > 0) {
        courses.forEach(course => {
            get_course_info(course);
        });
    }
}

window.addEventListener('load', function() {

    console.log('Page has finished loading!');
    
    let timeout_id;
    if(document.location.href.startsWith(CMUCourses_href)) {
        search_results = document.querySelector('div.flex-1.overflow-y-auto > div.p-6')
        const observer = new MutationObserver(() => {
            console.log('Dynamic content has changed!');
            console.log('Wait for a bit.');
            clearTimeout(timeout_id);
            timeout_id = setTimeout(() => {
                run();
            }, 1000);
        });
        const config = { childList: true, subtree: true };
        observer.observe(search_results, config);
    } 
});

