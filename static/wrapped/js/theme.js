const themeButton = document.getElementById('theme');
const themeControl = document.getElementById('themeControl')

let count = 0;

function toLchStr(color) {
    const lch = color.oklch
    return `${lch.l * 100}% ${lch.c} ${lch.h || 0}`
}

themeControl.addEventListener('change', (e) => {
    count++;

    if (count >= 10) {
        const light = e.target.checked ? 95 : 5
        const int = e.target.checked ? -5 : 5
        const base = [Math.random() * 360, Math.random() * 25]

        const b1 = new Color('hsl', [...base, light])
        const b2 = new Color('hsl', [...base, light + int])
        const b3 = new Color('hsl', [...base, light + 2 * int])
        const n = new Color('hsl', [...base, light + 8 * int])

        const a = new Color('hsl', [Math.random() * 360, Math.random() * 75 + 25, Math.random() * 75 + 25])
        const p = new Color('hsl', [Math.random() * 360, Math.random() * 75 + 25, Math.random() * 75 + 25])
        const s = new Color('hsl', [Math.random() * 360, Math.random() * 75 + 25, Math.random() * 75 + 25])

        const c = new Color('hsl', [0, 0, e.target.checked ? 0 : 100])

        document.documentElement.style.setProperty('--b1', toLchStr(b1))
        document.documentElement.style.setProperty('--b2', toLchStr(b2))
        document.documentElement.style.setProperty('--b3', toLchStr(b3))
        document.documentElement.style.setProperty('--n', toLchStr(n))

        document.documentElement.style.setProperty('--a', toLchStr(a))
        document.documentElement.style.setProperty('--p', toLchStr(p))
        document.documentElement.style.setProperty('--s', toLchStr(s))

        document.documentElement.style.setProperty('--bc', toLchStr(c))
        document.documentElement.style.setProperty('--nc', toLchStr(c))
        document.documentElement.style.setProperty('--ac', toLchStr(c))
        document.documentElement.style.setProperty('--pc', toLchStr(c))
        document.documentElement.style.setProperty('--sc', toLchStr(c))
    }

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