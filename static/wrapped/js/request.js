async function getAuthenticationLink() {
    const response = await fetch('http://localhost:8000/api/authenticate');
    const json = await response.json();

    const link = document.getElementById('authLink');
    link.setAttribute('href', json.url);
}

async function getLinkToken() {
    const response = await fetch('http://localhost:8000/api/link');
    const status = response.status;

    if (status === 200) {
        const url = document.getElementById('goHome').getAttribute('href');
        window.location.replace(url);
    }
}