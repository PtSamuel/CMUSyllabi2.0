chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log(request.data);
    

    // sendResponse({ error: 'this is some error' });
    // fetch('http://3.230.154.38:3000/api/find_course?course_number=15122')
    //     .then(response => response.json())
    //     .then(data => sendResponse({ data: 'data' }))
    //     .catch(error => sendResponse({ error: 'failed' }));

    fetch('http://3.230.154.38:3000/api/find_course?course_number=15122')
        .then(response => response.json())
        .then(data => sendResponse({ data: data }))
        .catch(error => sendResponse({ error: error }));

    return true;
});
