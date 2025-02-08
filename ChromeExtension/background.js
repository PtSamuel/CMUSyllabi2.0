chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log(request.data);
    
    fetch(`http://3.230.154.38:3000/api/find_course?course_number=${request.course_number}`)
        .then(response => response.json())
        .then(data => sendResponse({ data: data }))
        .catch(error => sendResponse({ error: error }));

    return true;
});
