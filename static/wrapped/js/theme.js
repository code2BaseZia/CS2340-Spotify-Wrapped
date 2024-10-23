const themeButton = document.getElementById('theme');
const themeControl = document.getElementById('themeControl')
let dark = true;

themeControl.addEventListener('change', (e) => {
    if (!e.target.checked) {
        document.documentElement.setAttribute('data-theme', 'spotifyDark');
        themeButton.classList.add('btn-primary');
        themeButton.classList.remove('btn-secondary');
    } else {
        document.documentElement.setAttribute('data-theme', 'spotifyLight');
        themeButton.classList.add('btn-secondary');
        themeButton.classList.remove('btn-primary');
    }
});