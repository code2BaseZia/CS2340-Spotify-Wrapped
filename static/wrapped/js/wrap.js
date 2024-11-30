const container = document.getElementById("slides");
const slides = container.children;
const indicators = document.getElementById("indicators").getElementsByClassName("progress");
const buttons = {
    left: document.getElementById("left"),
    right: document.getElementById("right"),
};
const visibility = document.getElementById("visibility")
const visibilityText = document.getElementById("visibilityText")

visibility.checked = isPublic
visibilityText.innerText = isPublic ? 'Public' : 'Private'

const extraContainer = document.getElementsByClassName("extra-visibility")
const extraVisibility = document.getElementById("extraVisibility")

let current = 0;
let progress = 0;

const audio = new Audio();
audio.loop = true;
audio.volume = 0;

const volume = document.getElementById('volume')
const icon = document.getElementById('volumeIcon')
volume.addEventListener('input', (e) => {
    audio.volume = e.target.value / 100
    if (e.target.value == 0) {
        icon.innerHTML = `<path stroke-linecap="round" stroke-linejoin="round" d="M17.25 9.75 19.5 12m0 0 2.25 2.25M19.5 12l2.25-2.25M19.5 12l-2.25 2.25m-10.5-6 4.72-4.72a.75.75 0 0 1 1.28.53v15.88a.75.75 0 0 1-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.009 9.009 0 0 1 2.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75Z" />`
    } else {
        icon.innerHTML = `<path stroke-linecap="round" stroke-linejoin="round" d="M19.114 5.636a9 9 0 0 1 0 12.728M16.463 8.288a5.25 5.25 0 0 1 0 7.424M6.75 8.25l4.72-4.72a.75.75 0 0 1 1.28.53v15.88a.75.75 0 0 1-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.009 9.009 0 0 1 2.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75Z" />`
    }
})

audio.addEventListener('ended', () => {
    this.currentTime = 0;
    this.play();
}, false);

visibility.addEventListener('change', async (e) => {
    isPublic = e.target.checked
    await changeVisibility(id, isPublic)
    visibilityText.innerText = isPublic ? 'Public' : 'Private'
})
extraVisibility.addEventListener('change', async (e) => {
    visibility.click()
})

function updateModal() {
    for (let extra of extraContainer) {
        if (isPublic) {
            extra.classList.add('hidden')
        } else {
            extra.classList.remove('hidden')
        }
    }
}

function updateSlide() {
    animations[current].start()
    gsap.to(slides, {xPercent: current * -100, duration: 0.5, ease: 'power2.inOut'});

    if (audio.src !== tracks[current]) {
        audio.pause()
        audio.currentTime = 0
        audio.src = tracks[current]
        audio.play()
    }
}

function nextSlide() {
    if (current === 10) return;

    animations[current].end(updateSlide);

    indicators[current].classList.remove("active");
    indicators[current].value = 100;

    current++;
    progress = 0;

    indicators[current].classList.add("active");
}

function prevSlide() {
    if (current === 0) return;

    animations[current].end(updateSlide);

    indicators[current].classList.remove("active");
    indicators[current].value = 0;

    current--;
    progress = 0;

    indicators[current].classList.add("active");
}

function goToSlide(index) {
    animations[current].end(updateSlide);

    indicators[current].classList.remove("active");
    current = index;
    progress = 0;
    indicators[current].classList.add("active");

    for (let i = 0; i < indicators.length; i++) {
        indicators[i].value = i < current ? 100 : 0;
    }
}

function updateProgress() {
    indicators[current].value = progress;
    if (current === 6 && !gameComplete) return

    progress += 0.1;
    if (progress > 100) {
        nextSlide();
    }
}

buttons.left.addEventListener("click", prevSlide);
buttons.right.addEventListener("click", nextSlide);

for (let i = 0; i < indicators.length; i++) {
    indicators[i].addEventListener("click", () => goToSlide(i));
}

setInterval(updateProgress, 15);
updateSlide()
updateModal()