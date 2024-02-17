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
  --foreground: #DDCCBB;
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

