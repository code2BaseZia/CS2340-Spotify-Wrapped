function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function getAuthenticationLink() {
    // The "Log in With Spotify" button only exists when the account isn't linked yet
    const link = document.getElementById('authLink');
    if (!link) return;

    const response = await fetch('/api/authenticate');
    const json = await response.json();

    link.setAttribute('href', json.url);
}

async function getLinkToken() {
    const response = await fetch('/api/link');
    const status = response.status;

    if (status === 200) {
        const url = document.getElementById('goHome').getAttribute('href');
        window.location.replace(url);
    }
}

async function getStats(term) {
    const response = await fetch(`/api/taste?term=${term}`);
    if (response.status === 401) {
        // Spotify link expired or user logged out: reload so the page shows the right login prompt
        window.location.replace('/wrapped/');
        return new Promise(() => {});
    }
    return await response.json();
}

async function getProfilePicture() {
    const response = await fetch('/api/picture');
    if (!response.ok) return null;
    const json = await response.json();
    return json.url;
}

async function createWrap(term) {
    const csrftoken = getCookie('csrftoken');

    const response = await fetch('/api/wrap', {
        method: 'POST',
        body: JSON.stringify({term}),
        headers: {
            'Content-type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrftoken
        }
    });
    const json = await response.json();

    return json.id;
}

async function changeVisibility(id, visibility) {
    const csrftoken = getCookie('csrftoken');

    const response = await fetch(`/api/wrap/${id}/visibility`, {
        method: 'POST',
        body: JSON.stringify({public: visibility}),
        headers: {
            'Content-type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrftoken
        }
    });
}

async function completeGame(id, score) {
    const csrftoken = getCookie('csrftoken');

    const response = await fetch(`/api/wrap/${id}/game`, {
        method: 'POST',
        body: JSON.stringify({score}),
        headers: {
            'Content-type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrftoken
        }
    });
}