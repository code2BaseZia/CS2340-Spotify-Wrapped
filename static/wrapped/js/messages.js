const messages = document.getElementsByClassName('message');

for (let message of messages) {
    gsap.from(message, {
        opacity: 0,
        y: 25,
        scale: 0.8,
        height: 0,
        ease: 'power2.in'
    });
    const button = message.getElementsByClassName('btn').item(0);
    const timeout = setTimeout(() => {
        gsap.to(message, {
            opacity: 0,
            y: 25,
            scale: 0.8,
            height: 0,
            ease: 'power2.in'
        });
    }, 5000)
    button.addEventListener('click', () => {
        clearTimeout(timeout);
        gsap.to(message, {
            opacity: 0,
            y: 25,
            scale: 0.8,
            height: 0,
            ease: 'power2.in'
        });
    });

}