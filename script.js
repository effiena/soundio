document.addEventListener("DOMContentLoaded", () => {
    const playlistItems = Array.from(document.querySelectorAll("#playlist li"));
    const playPauseBtn = document.getElementById("play-pause-btn");
    const prevBtn = document.getElementById("prev-btn");
    const nextBtn = document.getElementById("next-btn");
    const shuffleBtn = document.getElementById("shuffle-btn");
    const repeatBtn = document.getElementById("repeat-btn");

    let playlist = playlistItems.map(li => li.dataset.src);
    let currentIndex = 0;
    let isRepeat = false;

    // -------------------- FUNCTIONS --------------------
    function shufflePlaylist() {
        for (let i = playlist.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [playlist[i], playlist[j]] = [playlist[j], playlist[i]];
            [playlistItems[i].textContent, playlistItems[j].textContent] = [playlistItems[j].textContent, playlistItems[i].textContent];
            [playlistItems[i].dataset.src, playlistItems[j].dataset.src] = [playlistItems[j].dataset.src, playlistItems[i].dataset.src];
        }
        currentIndex = 0;
        document.dispatchEvent(new Event("playlistShuffled"));
    }

    function toggleRepeat() {
        isRepeat = !isRepeat;
        alert("Repeat " + (isRepeat ? "ON" : "OFF"));
    }

    // -------------------- EVENT LISTENERS --------------------
    shuffleBtn.addEventListener("click", shufflePlaylist);
    repeatBtn.addEventListener("click", toggleRepeat);

    playlistItems.forEach((li, idx) => {
        li.addEventListener("click", () => {
            currentIndex = idx;
            document.dispatchEvent(new CustomEvent("songSelected", { detail: { index: idx } }));
        });
    });

    prevBtn.addEventListener("click", () => document.dispatchEvent(new Event("prevSong")));
    nextBtn.addEventListener("click", () => document.dispatchEvent(new Event("nextSong")));
    playPauseBtn.addEventListener("click", () => document.dispatchEvent(new Event("togglePlayPause")));
});

document.body.addEventListener("click", unlockAudio, { once: true });
document.body.addEventListener("touchstart", unlockAudio, { once: true });

