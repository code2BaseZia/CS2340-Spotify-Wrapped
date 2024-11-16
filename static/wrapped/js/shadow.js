const scrollers = document.getElementsByClassName('scroll-shadow');

for (let scroller of scrollers) {
    scroller.addEventListener('scroll', () => {
        if (scroller.scrollTop === 0) {
            scroller.classList.add('top');
        } else {
            scroller.classList.remove('top');
        }

        if (scroller.offsetHeight + scroller.scrollTop >= scroller.scrollHeight) {
            scroller.classList.add('bottom');
        } else {
            scroller.classList.remove('bottom');
        }
    })
}