const themeButton = document.getElementById('theme');
const themeControl = document.getElementById('themeControl')

let count = parseInt(sessionStorage.getItem('count')) || 0;

function setTheme(theme, colors=null) {
    if (theme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'spotifyDark')
        themeButton.classList.add('btn-primary')
        themeButton.classList.remove('btn-secondary')
        themeControl.checked = true
    }
    if (theme === 'light') {
        document.documentElement.setAttribute('data-theme', 'spotifyLight')
        themeButton.classList.add('btn-secondary')
        themeButton.classList.remove('btn-primary')
        themeControl.checked = false
    }
    if (colors) {
        document.documentElement.style.setProperty('--b1', colors.b1)
        document.documentElement.style.setProperty('--b2', colors.b2)
        document.documentElement.style.setProperty('--b3', colors.b3)
        document.documentElement.style.setProperty('--n', colors.n)
        document.documentElement.style.setProperty('--a', colors.a)
        document.documentElement.style.setProperty('--p', colors.p)
        document.documentElement.style.setProperty('--s', colors.s)
        document.documentElement.style.setProperty('--bc', colors.c)
        document.documentElement.style.setProperty('--nc', colors.c)
        document.documentElement.style.setProperty('--ac', colors.c)
        document.documentElement.style.setProperty('--pc', colors.c)
        document.documentElement.style.setProperty('--sc', colors.c)
        sessionStorage.setItem('randomTheme', JSON.stringify(colors))
    }

    sessionStorage.setItem('theme', theme)
}

function toLchStr(color) {
    const lch = color.oklch
    return `${lch.l * 100}% ${lch.c} ${lch.h || 0}`
}

themeControl.addEventListener('change', (e) => {
    count++;
    sessionStorage.setItem('count', count)

    let randomTheme = null;

    if (count >= 10) {
        const light = e.target.checked ? 90 : 10
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

        randomTheme = {
            b1: toLchStr(b1),
            b2: toLchStr(b2),
            b3: toLchStr(b3),
            n: toLchStr(n),
            a: toLchStr(a),
            p: toLchStr(p),
            s: toLchStr(s),
            c: toLchStr(c)
        }
    }

    if (!e.target.checked) {
        setTheme('light', randomTheme)
    } else {
        setTheme('dark', randomTheme)
    }
})

document.addEventListener('DOMContentLoaded', (e) => {
    const currentTheme = sessionStorage.getItem('theme')
    const randomTheme = JSON.parse(sessionStorage.getItem('randomTheme') || null)
    setTheme(currentTheme, randomTheme)
})