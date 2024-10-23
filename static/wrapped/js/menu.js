const control = document.getElementById('menuControl');
const [ menuSvg, burger, x ] = control.getElementsByTagName('path');
let menu = false;

control.addEventListener('click', (e) => {
    menu = !menu;
    if (menu) {
        gsap.to('#menu', { height: 'calc(100vh - 4rem)', duration: 0.25, ease: 'power2.in' });
        gsap.to(menuSvg, { morphSVG: x, duration: 0.25, ease: 'power2.in' });
    } else {
        gsap.to('#menu', { height: '0', duration: 0.25, ease: 'power2.out' });
        gsap.to(menuSvg, { morphSVG: burger, duration: 0.25, ease: 'power2.out' });
    }
});