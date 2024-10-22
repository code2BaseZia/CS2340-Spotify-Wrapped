const control = document.getElementById('menuControl');
const [ svg, burger, x ] = control.getElementsByTagName('path');
let menu = false;

control.addEventListener('click', (e) => {
    menu = !menu;
    if (menu) {
        control.classList.add('x');
        gsap.to('#menu', { height: 'calc(100vh - 4rem)', duration: 0.25, ease: 'power2.in' });
        gsap.to(svg, { morphSVG: x, duration: 0.25, ease: 'power2.in' });
    } else {
        control.classList.remove('x');
        gsap.to('#menu', { height: '0', duration: 0.25, ease: 'power2.out' });
        gsap.to(svg, { morphSVG: burger, duration: 0.25, ease: 'power2.out' });
    }
});