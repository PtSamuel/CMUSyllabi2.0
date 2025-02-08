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
    let syllabus_entries;
    chrome.runtime.sendMessage({ course_number: course_number }, (response) => {
        if(response === undefined) {
            return;
        }
        if (response.data) {
            console.log(`Data: ${response.data.length} syllabus entries.`);
            syllabus_entries = response.data;

            thead = table.querySelector('thead');
            tbody = table.querySelector('tbody');            
            offerings = tbody.children;
            
            let current;
            let count = 0;
            for(let i = 0; i < offerings.length; i++) {
                offering = offerings[i];
                semester = offering.children[0];
                semester_name = semester.innerHTML;
                
                if(semester_name.indexOf('</a>') != -1) {
                    continue;
                }
                const acronym = get_acronym(semester_name);
                if(acronym === undefined) {
                    console.error(`Unable to process semester name: ${semester_name}`);
                    continue;
                }
                
                console.log(`${course_number}: ${acronym}`);
                
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
                    // console.log(`<a class="letter-container" href=${filtered[count].syllabus_href}>S</a> ${semester_name}`);
                    semester.innerHTML = `<a class="letter-container match" target="_blank" href=${filtered[count].syllabus_href}>S</a> ${semester_name}`;
                }
                
                // semester.innerHTML = "hello";
            }
        } else {
            console.error('Error:', response.error);
        }
    });
    console.log('Done sending message.');
}

function get_course_info(course) {
    course_data = course.children[0];
    course_number = course_data.querySelector('div > div > a > div > span')
    course_number = course_number.innerHTML.replaceAll('-', '');
    table = course.children[1];
    populate_table(course_number, table);
}

function run() {
    
    // This throws an error but seems unnecessary.
    // const link = document.createElement('link');
    // link.rel = 'stylesheet';
    // link.type = 'text/css';
    // link.href = chrome.runtime.getURL('style.css'); // URL to the CSS file
    // document.head.appendChild(link);

    setTimeout(() => {

        console.log('Arriving at CMUCourses.');
        courses = document.querySelectorAll('div.bg-white.border-gray-100.rounded.border.p-6')
        courses.forEach(course => {
            get_course_info(course);
        });

    }, 1000);

}

let observer;

function check_website() {
    if(document.location.href.startsWith(CMUCourses_href)) {
        search_results = document.querySelector('div.flex-1.overflow-y-auto > div.p-6')
        
        console.log(search_results);
        if(search_results.length > 0) {
            if(!observer) {
                observer = new MutationObserver(() => {
                    console.log('Dynamic content has changed!');
                    console.log('Wait for a bit.');
                    setTimeout(() => {
                        run();
                    }, 500);
                    
                });
                const config = { childList: true, subtree: true };
                observer.observe(search_results, config);
            }
        }
    }
}

window.addEventListener('load', function() {
    console.log('Page has finished loading!');
    check_website();
});

check_website();
