// const searchString = "example"; // The string to search and highlight

// function highlightOccurrences(text) {
//   const regex = new RegExp(`(${text})`, 'gi');
//   const bodyText = document.body.innerHTML;
//   document.body.innerHTML = bodyText.replace(regex, '<span class="highlight">$1</span>');
// }

// function observeDOMChanges() {
//   const observer = new MutationObserver(() => {
//     highlightOccurrences(searchString); // Reapply the highlight when the DOM changes
//   });

//   // Observe changes to the body of the document
//   observer.observe(document.body, {
//     childList: true,
//     subtree: true, // Observe changes within the entire body (not just direct children)
//     characterData: true,
//   });
// }

// // Initial highlighting on page load
// highlightOccurrences(searchString);

// // Start observing DOM changes
// observeDOMChanges();

CMUCourses_href = 'https://courses.scottylabs.org/'


function populate_table(table) {
    thead = table.querySelector('thead')
    tbody = table.querySelector('tbody')
    
    offerings = tbody.children

    for(let i = 0; i < offerings.length; i++) {
        offering = offerings[i]

        semester = offering.children[0];
        semester.innerHTML = `<a href="/">S</a> ${semester.innerHTML}`;
    }
}

function get_course_info(course) {
    course_data = course.children[0];
    table = course.children[1];
    populate_table(table);
}

if(document.location.href.startsWith(CMUCourses_href)) {
    setTimeout(() => {

        console.log('Arriving at CMUCourses.');
        courses = document.querySelectorAll('div.bg-white.border-gray-100.rounded.border.p-6')
        courses.forEach(course => {
            get_course_info(course);
        });

    }, 1000);
}

// table = courses[0].querySelector('div.m-auto.space-y-4 > div.mt-3.overflow-x-auto.rounded.p-4.bg-gray-50 > table.w-full.min-w-fit.table-auto')


