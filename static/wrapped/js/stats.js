const radios = document.querySelectorAll('input[type=radio]')
const tables = {
    tracks: document.getElementById('tracks'),
    albums: document.getElementById('albums'),
    artists: document.getElementById('artists'),
    genres: document.getElementById('genres')
}
const volume = document.getElementById('volume')
const create = document.getElementsByClassName('create-wrapped')

const audio = new Audio();
let lastControls = null;
let listener = null;
let interval = null;

let term = 'medium';

function handlePlayClick(target) {
    const controls = {
        play: target.getElementsByClassName('play').item(0),
        pause: target.getElementsByClassName('pause').item(0),
        progress: target.getElementsByClassName('radial-progress').item(0)
    };

    if (audio.currentSrc === target.getAttribute('data-preview')) {
        if (audio.paused) {
            audio.play();
            controls.play.classList.add('hidden');
            controls.pause.classList.remove('hidden');
            controls.progress.classList.remove('invisible');
            setInterval(listener, 10);
        }
        else {
            audio.pause()
            controls.play.classList.remove('hidden');
            controls.pause.classList.add('hidden');
            controls.progress.classList.add('invisible');
            clearInterval(interval);
        }
    } else {
        audio.pause();
        audio.src = target.getAttribute('data-preview');
        audio.play();

        if (interval) {
            clearInterval(interval);
        }
        listener = () => controls.progress.style.setProperty('--value', audio.currentTime / audio.duration * 100);
        interval = setInterval(listener, 10);

        if (lastControls) {
            lastControls.play.classList.remove('hidden');
            lastControls.pause.classList.add('hidden');
            lastControls.progress.classList.add('invisible');
        }
        controls.play.classList.add('hidden');
        controls.pause.classList.remove('hidden');
        controls.progress.classList.remove('invisible');
        lastControls = controls;
        audio.addEventListener('ended', () => {
            controls.play.classList.remove('hidden');
            controls.pause.classList.add('hidden');
            controls.progress.classList.add('invisible');
            clearInterval(interval);
        })
    }
}

function updateStats(data) {
    tables.tracks.innerHTML = data.tracks.map((track, i) => `
        <tr class="group bg-black bg-opacity-0 border-base-300 hover:bg-opacity-5">
            <th class="pr-0 py-2 text-center"><h4>#${i + 1}</h4></th>
            <td class="py-2">
                <div class="flex items-center gap-3">
                    <div class="avatar relative">
                        <div class="h-12 w-12 relative z-10">
                            <img src="${track.album.images[0]?.url || placeholder}" alt="Album Photo"/>
                        </div>
                        <button class="absolute inset-0 bg-black bg-opacity-20 opacity-0 group-hover:opacity-100 flex justify-center items-center z-20" data-preview="${track.preview_url}" onclick="handlePlayClick(this);">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="stroke-accent size-6 pause hidden">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 5.25v13.5m-7.5-13.5v13.5" />
                            </svg>
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" class="stroke-accent fill-accent size-6 play">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M5.25 5.653c0-.856.917-1.398 1.667-.986l11.54 6.347a1.125 1.125 0 0 1 0 1.972l-11.54 6.347a1.125 1.125 0 0 1-1.667-.986V5.653Z" />
                            </svg>
                            <div class="radial-progress text-accent absolute inset-1.5 invisible" style="--value:0; --size: 2.25rem; --thickness: 0.25rem;" role="progressbar"></div>
                        </button>
                    </div>
                    <div>
                        <div class="font-bold"><a target="_blank" rel="noopener norefferer" class="hover:link" href="${track.external_urls.spotify}">${track.name}</a></div>
                        <div class="text-sm opacity-50">
                            ${track.artists.map((artist)=>`<a target="_blank" rel="noopener norefferer" class="hover:link" href="${artist.external_urls.spotify}">
                                ${artist.name}
                            </a>`).join(',\n')}
                        </div>
                    </div>
                </div>
            </td>
            <td><a target="_blank" rel="noopener norefferer" class="hover:link" href="${track.album.external_urls.spotify}">${track.album.name}</a></td>
        </tr>
    `).join('\n')

    tables.albums.innerHTML = data.albums.map((album, i) => `
        <tr class="group bg-black bg-opacity-0 border-base-300 hover:bg-opacity-5 first:border-t-0">
            <th class="pr-0 py-2 text-center"><h4>#${i + 1}</h4></th>
            <td class="py-2">
                <div class="flex items-center gap-3">
                    <div class="avatar relative">
                        <div class="h-12 w-12 relative z-10">
                            <img src="${album.images[0]?.url || placeholder}" alt="Album Photo"/>
                        </div>
                    </div>
                    <div>
                        <div class="font-bold"><a target="_blank" rel="noopener norefferer" class="hover:link" href="${album.external_urls.spotify}">${album.name}</a></div>
                        <div class="text-sm opacity-50">
                            ${album.artists.map((artist)=>`<a target="_blank" rel="noopener norefferer" class="hover:link" href="${artist.external_urls.spotify}">
                                ${artist.name}
                            </a>`).join(',\n')}
                        </div>
                    </div>
                </div>
            </td>
            <td>${album_types[album.album_type]}</td>
            <td>${album.total_tracks}</td>
            <td>${album.release_date.split('-')[0]}</td>
        </tr>
    `).join('\n')

    tables.artists.innerHTML = data.artists.map((artist, i) => `
        <tr class="bg-black bg-opacity-0 border-base-300 hover:bg-opacity-5">
            <th class="pr-0 py-2 text-center"><h4>#${i + 1}</h4></th>
            <td class="py-2">
                <div class="flex items-center gap-3">
                    <div class="avatar">
                        <div class="mask mask-circle h-12 w-12">
                            <img src="${artist.images[0]?.url || placeholder}" alt="Artist Photo"/>
                        </div>
                    </div>
                    <div>
                        <div class="font-bold">
                            <a target="_blank" rel="noopener norefferer" class="hover:link" href="${artist.external_urls.spotify}">
                                ${artist.name}
                            </a>
                        </div>
                        <div class="text-sm opacity-50">
                            ${artist.followers.total.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")} followers
                        </div>
                    </div>
                </div>
            </td>
        </tr>
    `).join('\n')

    tables.genres.innerHTML = data.genres.map((genre, i) => `
        <tr class="bg-black bg-opacity-0 border-base-300 hover:bg-opacity-5">
            <th class="pr-0 text-center"><h5>#${i + 1}</h5></th>
            <td class="whitespace-nowrap">${genre.name}</td>
            <td class="w-full">
                <progress class="progress progress-accent" value="${genre.freq * 100}" max="100"></progress>
            </td>
        </tr>
    `).join('\n')
}

radios.forEach((radio) => {
    radio.addEventListener('change', (e) => {
        if (e.target.checked) {
            term = e.target.value
            getStats(term).then(updateStats)
        }
    })
})

volume.addEventListener('input', (e) => audio.volume = e.target.value / 100)

for (let button of create) {
    button.addEventListener('click', (e) => {
        e.target.innerHTML = '<span class="loading loading-spinner loading-md"></span>'
        e.target.disabled = true
        createWrap(term).then((id) => {
            window.location.href = '../api/wrap/' + id;
        })
    })
}

document.addEventListener("DOMContentLoaded", () => getStats('medium').then(updateStats))