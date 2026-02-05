document.addEventListener("DOMContentLoaded", () => {
    // ---------- DOM ELEMENTS ----------
    const player = document.getElementById("player");
    const playlistItems = Array.from(document.querySelectorAll("#playlist li"));
    const progressBar = document.getElementById("progress-bar");
    const currentTimeEl = document.getElementById("current");
    const durationEl = document.getElementById("duration");
    const currentSongTitle = document.getElementById("current-song");

    const playPauseBtn = document.getElementById("play-pause-btn"); // add id in HTML
    const stopBtn = document.getElementById("stop-btn");
    const nextBtn = document.getElementById("next-btn");
    const prevBtn = document.getElementById("prev-btn");
    const shuffleBtn = document.getElementById("shuffle-btn");
    const repeatBtn = document.getElementById("repeat-btn");

    // ---------- PLAYER STATE ----------
    let playlist = playlistItems.map(li => li.dataset.src);
    let currentIndex = 0;
    let isPlaying = false;
    let isRepeat = false;

    // ---------- HELPER FUNCTION: FORMAT TIME ----------
    function formatTime(sec) {
        if (isNaN(sec)) return "00:00";
        const m = Math.floor(sec / 60);
        const s = Math.floor(sec % 60);
        return `${m.toString().padStart(2,'0')}:${s.toString().padStart(2,'0')}`;
    }

    // ---------- LOAD SONG ----------
    function loadSong(index) {
        playlistItems.forEach(li => li.classList.remove("active"));
        playlistItems[index].classList.add("active");

        player.src = playlist[index];
        player.play();
        isPlaying = true;
        playPauseBtn.textContent = "⏸";

        const songName = playlistItems[index].textContent;
        currentSongTitle.style.animation = "none";
        currentSongTitle.textContent = `🎶 Now Playing: ${songName}`;

        const containerWidth = document.getElementById("current-song-container").offsetWidth;
        const textWidth = currentSongTitle.scrollWidth;
        if (textWidth > containerWidth) {
            const duration = textWidth / 50;
            currentSongTitle.style.animation = `scroll ${duration}s linear infinite`;
        }
    }

    // ---------- PLAY / PAUSE ----------
    function playPause() {
        if (!player.src && playlist.length > 0) {
            loadSong(currentIndex);
            return;
        }
        if (isPlaying) {
            player.pause();
            isPlaying = false;
            playPauseBtn.textContent = "▶️";
        } else {
            player.play();
            isPlaying = true;
            playPauseBtn.textContent = "⏸";
        }
    }

    // ---------- STOP ----------
    function stopSong() {
        player.pause();
        player.currentTime = 0;
        isPlaying = false;
        playPauseBtn.textContent = "▶️";
    }

    // ---------- NEXT / PREV ----------
    function nextSong() {
        if (isRepeat) {
            loadSong(currentIndex);
        } else {
            currentIndex = (currentIndex + 1) % playlist.length;
            loadS
