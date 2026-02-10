async function loadTrackHistory() {
    const response = await fetch("/api/tracks/history");
    const tracks = await response.json();

    const list = document.getElementById("track-list");
    list.innerHTML = "";

    tracks.forEach(track => {
        const li = document.createElement("li");
        li.textContent = track.title;
        li.onclick = () => setLocalTrack(track.url);
        list.appendChild(li);
    });
}

function setLocalTrack(url) {
    localStorage.setItem("localTrackUrl", url)
    updatePlayer(url)
}

function updatePlayer(url)}{
    const iframe = document.getElementById("player")
}

async function loadInitialTrack() {
    const localTrack = localStorage.getItem("localTrackUrl");

    if (localTrack) {
        updatePlayer(localTrack);
        return;
    }

    const response = await fetch("/api/tracks/current");
    const track = await response.json();
    updatePlayer(track.url);
}
document.addEventListener("DOMContentLoaded", () => {
    const iframe = document.querySelector(".player iframe");
    const items = document.querySelectorAll("#track-list li");

    items.forEach(item => {
        item.addEventListener("click", () => {
            const trackId = item.dataset.trackId;
            iframe.src = 'https://music.yandex.ru/iframe/#track/${trackId}';
        });
    });
});

document.addEventListener("DOMContentLoaded", () => {
    loadInitialTrack();
    loadTrackHistory();
});

