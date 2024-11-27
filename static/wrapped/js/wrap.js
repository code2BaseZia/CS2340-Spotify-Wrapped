console.log(animations)

const container = document.getElementById("slides");
const slides = container.children;
const indicators = document.getElementById("indicators").getElementsByClassName("progress");
const buttons = {
    left: document.getElementById("left"),
    right: document.getElementById("right"),
};

let current = 2;
let progress = 0;

const audio = new Audio();

function updateSlide() {
    animations[current].preset()
    gsap.to(slides, {xPercent: current * -100, duration: 0.5, ease: 'power2.inOut', onComplete: animations[current].start()})
}

function nextSlide() {
    if (current === 10) return;

    indicators[current].classList.remove("active");
    indicators[current].value = 100;

    current++;
    progress = 0;

    indicators[current].classList.add("active");
    updateSlide();
}

function prevSlide() {
    if (current === 0) return;

    indicators[current].classList.remove("active");
    indicators[current].value = 0;

    current--;
    progress = 0;

    indicators[current].classList.add("active");
    updateSlide();
}

function goToSlide(index) {
    indicators[current].classList.remove("active");
    current = index;
    progress = 0;
    indicators[current].classList.add("active");

    for (let i = 0; i < indicators.length; i++) {
        indicators[i].value = i < current ? 100 : 0;
    }

    updateSlide();
}

function updateProgress() {
    progress += 0.1;
    if (progress > 100) {
        nextSlide();
    }

    indicators[current].value = progress;
}

buttons.left.addEventListener("click", prevSlide);
buttons.right.addEventListener("click", nextSlide);

for (let i = 0; i < indicators.length; i++) {
    indicators[i].addEventListener("click", () => goToSlide(i));
}

//setInterval(updateProgress, 15);
updateSlide();
