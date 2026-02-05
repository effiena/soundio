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
        // highlight active song
        playlistItems.forEach(li => li.classList.remove("active"));
        playlistItems[index].classList.add("active");

        // set audio src
        player.src = playlist[index];
        player.play();
        isPlaying = true;
        playPauseBtn.textContent = "⏸"; // update icon

        // update title
        const songName = playlistItems[index].textContent;
        currentSongTitle.style.animation = "none"; // reset previous animation
        currentSongTitle.textContent = `🎶 Now Playing: ${songName}`;

        // scroll animation if text too wide
        const containerWidth = document.getElementById("current-song-container").offsetWidth;
        const textWidth = currentSongTitle.scrollWidth;
        if (textWidth > containerWidth) {
            const duration = textWidth / 50; // adjust speed
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
            loadSong(currentIndex);
        }
    }

    function prevSong() {
        currentIndex = (currentIndex - 1 + playlist.length) % playlist.length;
        loadSong(currentIndex);
    }

    // ---------- SHUFFLE ----------
    function shufflePlaylist() {
        for (let i = playlist.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [playlist[i], playlist[j]] = [playlist[j], playlist[i]];
            [playlistItems[i].textContent, playlistItems[j].textContent] =
                [playlistItems[j].textContent, playlistItems[i].textContent];
            [playlistItems[i].dataset.src, playlistItems[j].dataset.src] =
                [playlistItems[j].dataset.src, playlistItems[i].dataset.src];
        }
        currentIndex = 0;
        loadSong(currentIndex);
    }

    // ---------- REPEAT ----------
    function toggleRepeat() {
        isRepeat = !isRepeat;
        alert("Repeat " + (isRepeat ? "ON" : "OFF"));
    }

    // ---------- EVENT LISTENERS ----------
    playlistItems.forEach((li, idx) => {
        li.addEventListener("click", () => {
            currentIndex = idx;
            loadSong(currentIndex);
        });
    });

    player.addEventListener("ended", nextSong);

    player.addEventListener("timeupdate", () => {
        if (player.duration) {
            progressBar.max = player.duration;
            progressBar.value = player.currentTime;
            currentTimeEl.textContent = formatTime(player.currentTime);
            durationEl.textContent = formatTime(player.duration);
        }
    });

    progressBar.addEventListener("input", () => {
        player.currentTime = progressBar.value;
    });

    // ---------- BUTTONS ----------
    playPauseBtn.addEventListener("click", playPause);
    stopBtn.addEventListener("click", stopSong);
    nextBtn.addEventListener("click", nextSong);
    prevBtn.addEventListener("click", prevSong);
    shuffleBtn.addEventListener("click", shufflePlaylist);
    repeatBtn.addEventListener("click", toggleRepeat);

    // ---------- INITIAL SONG ----------
    if (playlist.length > 0) loadSong(currentIndex);
});

if ("mediaSession" in navigator) {
  navigator.mediaSession.metadata = new MediaMetadata({
    title: "Soundio",
    artist: "Now Playing",
    artwork: [
      { src: "/static/picture/soundiologo.png", sizes: "512x512", type: "image/png" }
    ]
  });

  navigator.mediaSession.setActionHandler("play", () => player.play());
  navigator.mediaSession.setActionHandler("pause", () => player.pause());
  navigator.mediaSession.setActionHandler("nexttrack", nextSong);
  navigator.mediaSession.setActionHandler("previoustrack", prevSong);
}

// Ensure first song loads on user interaction (mobile autoplay)
document.body.addEventListener("click", () => {
    if (!isPlaying && playlist.length > 0) loadSong(currentIndex);
}, { once: true });

@app.route("/music/<path:filename>")
def music(filename):
    # this will look inside static/music/
    return send_from_directory(MUSIC_DIR, filename, mimetype="audio/mpeg")

