from flask import Flask, render_template, send_from_directory, jsonify
import os

app = Flask(__name__)

# -------- CONFIG --------
MUSIC_DIR = os.path.join(app.static_folder, "music")

malay_keywords = [
    "siti","sharifah","s.jibeng","s. jibeng","muda","janda","a.ramlee","cek","yang","hati",
    "search","exists","ukays","spring","angan","sepi","flybaits","yale","kazar","impian","sinaran",
    "hajat","haida","ini","malam","kita","minyak","nasi","rasa","rintihan","lagu","ramlah","melayu",
    "jamal","amy","cinta","sayang","sendiri","kau","hampa","aishah","janji","aku","ku","ziana","dan",
    "di","dag","intan","kasih","kasihku","kasihmu","ella"
]

korean_keywords = [
    "bts","blackpink","twice","seventeen","exo","got7","redvelvet","straykids","ateez"
]

# -------- LANGUAGE DETECTION --------
def detect_language(filename):
    name = filename.lower()

    # 1️⃣ Korean characters → Korean
    for c in filename:
        if '\uac00' <= c <= '\ud7af':
            return "Korean"

    # 2️⃣ Chinese characters → Mandarin
    for c in filename:
        if '\u4e00' <= c <= '\u9fff':
            return "Mandarin"

    # 3️⃣ Korean artist keywords → Korean (English-only K-pop)
    for k in korean_keywords:
        if k in name:
            return "Korean"

    # 4️⃣ Malay keywords → Malay
    for k in malay_keywords:
        if k in name:
            return "Malay"

    # 5️⃣ Fallback → English
    return "English"

# -------- FLASK ROUTES --------
@app.route("/")
def index():
    files = [f for f in os.listdir(MUSIC_DIR) if f.lower().endswith(".mp3")]
    files.sort(key=str.lower)
    return render_template("index.html", playlist=files, zip=zip)

@app.route("/music/<path:filename>")
def music(filename):
    return send_from_directory(MUSIC_DIR, filename)

@app.route("/songs")
def songs():
    files = [f for f in os.listdir(MUSIC_DIR) if f.lower().endswith(".mp3")]
    playlist = []
    for f in files:
        playlist.append({
            "name": f,
            "url": f"/static/music/{f}",
            "genre": detect_language(f)
        })
    return jsonify(playlist)

@app.route('/manifest.json')
def manifest():
    return send_from_directory('.', 'manifest.json')

@app.route('/license.txt')
def license_file():
    return send_from_directory('.', 'license.txt')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
