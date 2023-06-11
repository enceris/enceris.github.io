// Search code
let posts = []
let input = document.getElementById('s');
let sections
let main

function init() {
  main = document.getElementsByTagName('main')[0];
  sections = main.getElementsByTagName('section');

  if (posts.length == 0) {
    var title, summary, tags;
    for (var i = 0; i < sections.length; i++) {
      title = sections[i].getElementsByTagName('a')[0].innerText.toLowerCase();
      summary = sections[i].getElementsByTagName('div')[0].innerText.toLowerCase();
      tags = sections[i].getElementsByTagName('span')[0].innerText.toLowerCase();
      posts.push(title + ' ' + summary + ' ' + tags);
    }
  }
}

function search() {
  init()
  let filter = input.value.toLowerCase();
  for (var i = 0; i < posts.length; i++) {
    if (posts[i].indexOf(filter) > -1) {
      sections[i].style.display = "";
    } else {
      sections[i].style.display = "none";
    }
  }
}

input.addEventListener('keyup', (event) => {
  if (location.pathname == '/p/') {
    search();
  } else if (event.key === 'Enter') {
    let url = new URL(location.origin);
    let params = new URLSearchParams(url.search);
    params.set('query', input.value.toLowerCase());
    window.location.href = '/p/?' + params.toString();
  }
});

const url = new URL(location);
const query = url.searchParams.get('query');

if (query) {
  input.value = query
  search();
}


// Dark/Light mode toggle code
const button = document.getElementsByClassName('toggle')[0];

const dark_mode = localStorage.getItem('dark_mode');
if (dark_mode === 'true') {
  applyStyle();
  button.textContent = 'light mode';
}

button.addEventListener('click', function() {
  if (button.textContent === 'dark mode') {
    applyStyle();
    button.textContent = 'light mode';
    localStorage.setItem('dark_mode', 'true');
  } else {
    removeStyle();
    button.textContent = 'dark mode';
    localStorage.setItem('dark_mode', 'false');
  }
});

function applyStyle() {
  const styleBlock = document.createElement('style');
  styleBlock.id = 'dark_mode';
  styleBlock.textContent = `
  :root {
  --background: #090909;
  --foreground: #eeeeee;
  --foreground-mild: #999999;
  --hyperlink: #ffffff;
  --hyperlink-visited: #ffffff;
  --highlight: #202020;
  --highlight-dark: #5c5c5c;
  --highlight-mild: #111111;
  --small: 1rem;
}
  `;
  document.head.appendChild(styleBlock);
}

function removeStyle() {
  const styleBlock = document.getElementById('dark_mode');
  if (styleBlock) {
    styleBlock.remove();
  }
}

