function updatePlayer(trackId) {
    const iframe = document.getElementById("main-player");

    // анимация исчезновения
    iframe.classList.add("fade-out");

    setTimeout(() => {
        iframe.src = `https://music.yandex.ru/iframe/#track/${trackId}`;
        iframe.classList.remove("fade-out");
    }, 300);

    setActiveTrack(trackId);
}

function setActiveTrack(trackId) {
    const items = document.querySelectorAll("#track-list li");

    items.forEach(item => {
        if (item.dataset.trackId === trackId) {
            item.classList.add("active");
        } else {
            item.classList.remove("active");
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {

    // История
    const items = document.querySelectorAll("#track-list li");

    items.forEach(item => {
        item.addEventListener("click", () => {
            const trackId = item.dataset.trackId;
            updatePlayer(trackId);
        });
    });

    // Кнопка "Слушать текущий"
    const currentBtn = document.getElementById("current-track-btn");

    currentBtn.addEventListener("click", () => {
        const trackId = currentBtn.dataset.trackId;
        updatePlayer(trackId);
    });

});