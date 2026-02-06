<script>
document.addEventListener("DOMContentLoaded", () => {
    // ---------- DOM ELEMENTS ----------
    const player = document.getElementById("player");
    const playlistItems = Array.from(document.querySelectorAll("#playlist li"));
    const progressBar = document.getElementById("progress-bar");
    const currentTimeEl = document.getElementById("current");
    const durationEl = document.getElementById("duration");
    const currentSongTitle = document.getElementById("current-song");

    const playPauseBtn = document.getElementById("play-pause-btn");
    const stopBtn = document.getElementById("stop-btn");
    const nextBtn = document.getElementById("next-btn");
    const prevBtn = document.getElementById("prev-btn");
    const shuffleBtn = document.getElementById("shuffle-btn");
    const repeatBtn = document.getElementById("repeat-btn");

    const logo = document.getElementById("soundio-logo");

    // ---------- PLAYER STATE ----------
    let playlist = playlistItems.map(li => li.dataset.src);
    let currentIndex = 0;
    let isPlaying = false;
    let isRepeat = false;

    // ---------- AUDIO CONTEXT ----------
    let audioCtx = null;
    let analyser = null;
    let source = null;
    let dataArray = null;
    let animationStarted = false;

    function initAudioContext() {
        if (!audioCtx) {
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            source = audioCtx.createMediaElementSource(player);
            analyser = audioCtx.createAnalyser();
            source.connect(analyser);
            analyser.connect(audioCtx.destination);
            analyser.fftSize = 256;
            dataArray = new Uint8Array(analyser.frequencyBinCount);

            if (!animationStarted) {
                animationStarted = true;
                animateLogo();
            }
        }
    }

    function unlockAudio() {
        if (audioCtx && audioCtx.state === "suspended") {
            audioCtx.resume().then(() => {
                console.log("AudioContext resumed!");
            });
        }
    }

    document.body.addEventListener("click", unlockAudio, { once: true });
    document.body.addEventListener("touchstart", unlockAudio, { once: true });

    function animateLogo() {
        if (!analyser) return;
        requestAnimationFrame(animateLogo);
        analyser.getByteFrequencyData(dataArray);

        let sum = 0;
        for (let i = 0; i < dataArray.length; i++) sum += dataArray[i];
        const avg = sum / dataArray.length;
        const scale = 0.9 + (avg / 255) * 0.3;
        const glow = (avg / 255) * 20;

        logo.style.transform = `scale(${scale})`;
        logo.style.boxShadow = `0 0 ${glow}px rgba(230,194,41,0.8)`;
    }

    // ---------- HELPERS ----------
    function formatTime(sec) {
        if (isNaN(sec)) return "00:00";
        const m = Math.floor(sec / 60);
        const s = Math.floor(sec % 60);
        return `${m.toString().padStart(2,'0')}:${s.toString().padStart(2,'0')}`;
    }

    function updateCurrentSongTitle() {
        const songName = playlistItems[currentIndex].textContent;
        currentSongTitle.style.animation = "none";
        currentSongTitle.textContent = `🎶 Now Playing: ${songName}`;

        const containerWidth = document.getElementById("current-song-container").offsetWidth;
        const textWidth = currentSongTitle.scrollWidth;
        if (textWidth > containerWidth) {
            const duration = textWidth / 50;
            currentSongTitle.style.animation = `scroll ${duration}s linear infinite`;
        }
    }

    // ---------- SONG CONTROL ----------
    function loadSong(index) {
        initAudioContext();
        unlockAudio();

        playlistItems.forEach(li => li.classList.remove("active"));
        playlistItems[index].classList.add("active");

        player.src = playlist[index];
        player.play().catch(err => console.log("Playback failed:", err));
        isPlaying = true;
        playPauseBtn.textContent = "⏸";

        updateCurrentSongTitle();
    }

    function playPause() {
        if (!player.src && playlist.length > 0) { loadSong(currentIndex); return; }
        if (isPlaying) { player.pause(); isPlaying=false; playPauseBtn.textContent="▶️"; }
        else { player.play(); isPlaying=true; playPauseBtn.textContent="⏸"; }
    }

    function stopSong() {
        player.pause();
        player.currentTime = 0;
        isPlaying = false;
        playPauseBtn.textContent = "▶️";
    }

    function nextSong() {
        currentIndex = isRepeat ? currentIndex : (currentIndex + 1) % playlist.length;
        loadSong(currentIndex);
    }

    function prevSong() {
        currentIndex = (currentIndex - 1 + playlist.length) % playlist.length;
        loadSong(currentIndex);
    }

    function shufflePlaylist() {
        for (let i = playlist.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [playlist[i], playlist[j]] = [playlist[j], playlist[i]];
            [playlistItems[i].textContent, playlistItems[j].textContent] = [playlistItems[j].textContent, playlistItems[i].textContent];
            [playlistItems[i].dataset.src, playlistItems[j].dataset.src] = [playlistItems[j].dataset.src, playlistItems[i].dataset.src];
        }
        currentIndex = 0;
        loadSong(currentIndex);
    }

    function toggleRepeat() {
        isRepeat = !isRepeat;
        alert("Repeat " + (isRepeat ? "ON" : "OFF"));
    }

    // ---------- EVENT LISTENERS ----------
    playlistItems.forEach((li, idx) => li.addEventListener("click", () => { currentIndex = idx; loadSong(currentIndex); }));
    playPauseBtn.addEventListener("click", playPause);
    stopBtn.addEventListener("click", stopSong);
    nextBtn.addEventListener("click", nextSong);
    prevBtn.addEventListener("click", prevSong);
    shuffleBtn.addEventListener("click", shufflePlaylist);
    repeatBtn.addEventListener("click", toggleRepeat);

    player.addEventListener("ended", nextSong);
    player.addEventListener("timeupdate", () => {
        if (player.duration) {
            progressBar.max = player.duration;
            progressBar.value = player.currentTime;
            currentTimeEl.textContent = formatTime(player.currentTime);
            durationEl.textContent = formatTime(player.duration);
        }
    });
    progressBar.addEventListener("input", () => { player.currentTime = progressBar.value; });
});
</script>
