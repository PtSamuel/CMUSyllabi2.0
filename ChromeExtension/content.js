const searchString = "example"; // Change this to the string you want to highlight

function highlightOccurrences(text) {
  const regex = new RegExp(`(${text})`, 'gi');
  const bodyText = document.body.innerHTML;
  document.body.innerHTML = bodyText.replace(regex, '<span class="highlight">$1</span>');
}

highlightOccurrences(searchString);