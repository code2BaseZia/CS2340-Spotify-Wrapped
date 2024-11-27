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
    const response = await fetch('https://54ijdxhtxd.execute-api.us-east-1.amazonaws.com/production/api/authenticate');
    const json = await response.json();

    const link = document.getElementById('authLink');
    link.setAttribute('href', json.url);
}

async function getLinkToken() {
    const response = await fetch('https://54ijdxhtxd.execute-api.us-east-1.amazonaws.com/production/api/link');
    const status = response.status;

    if (status === 200) {
        const url = document.getElementById('goHome').getAttribute('href');
        window.location.replace(url);
    }
}

async function getStats(term) {
    const response = await fetch(`https://54ijdxhtxd.execute-api.us-east-1.amazonaws.com/production/api/taste?term=${term}`);
    return await response.json();
}

async function getProfilePicture() {
    const response = await fetch('https://54ijdxhtxd.execute-api.us-east-1.amazonaws.com/production/api/picture');
    const json = await response.json();
    return json.url;
}

async function createWrap(term) {
    const csrftoken = getCookie('csrftoken');

    const response = await fetch('https://54ijdxhtxd.execute-api.us-east-1.amazonaws.com/production/api/wrap', {
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