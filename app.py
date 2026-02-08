from flask import Flask, render_template, jsonify, send_file, send_from_directory
import os

app = Flask(__name__)

# Path to your music folder
MUSIC_DIR = os.path.join(app.static_folder, "music")

# -------- AUTO LANGUAGE DETECTION --------
malay_keywords = [
    "siti","sharifah","s.jibeng","muda","janda","a.ramlee","cek","yang","hati","search",
    "exists","ukays","spring","angan", "sepi","flybaits","yale","kazar","impian","sinaran",
    "hajat","haida","ini","malam","kita","minyak","nasi","rasa","rintihan","lagu","ramlah",
    "melayu","jamal","amy","cinta","sayang","sendiri","kau","hampa","aishah","janji","aku",
    "ku","ziana","dan","di","dag","intan","kasih","kasihku","kasihmu","ella"
]

korean_keywords = [
    "bts","blackpink","twice","seventeen","exo","got7","redvelvet","straykids","ateez",
    "sudden","dynamite","butter"  # add English-named K-pop songs here
]

def detect_language(filename):
    name = filename.lower()

    # 1️⃣ Korean Unicode
    for c in filename:
        if '\uac00' <= c <= '\ud7af':
            return "Korean"

    # 2️⃣ Mandarin Unicode
    for c in filename:
        if '\u4e00' <= c <= '\u9fff':
            return "Mandarin"

    # 3️⃣ Korean keywords (English-named songs)
    for k in korean_keywords:
        if k in name:
            return "Korean"

    # 4️⃣ Malay keywords
    for k in malay_keywords:
        if k in name:
            return "Malay"

    # 5️⃣ Fallback
    return "English"

# ------------------ Flask Routes ------------------
@app.route("/")
def index():
    files = os.listdir(MUSIC_DIR)
    playlist = [f for f in files if f.lower().endswith(".mp3")]
    playlist.sort(key=str.lower)
    return render_template("index.html", playlist=playlist)

@app.route("/music/<path:filename>")
def music(filename):
    file_path = os.path.join(MUSIC_DIR, filename)
    return send_file(file_path, mimetype="audio/mpeg", as_attachment=False, conditional=True)

@app.route('/songs')
def songs():
    # Return playlist with genre assigned
    files = [f for f in os.listdir(MUSIC_DIR) if f.lower().endswith(".mp3")]
    playlist = []
    for f in files:
        playlist.append({
            "name": f.rsplit('.',1)[0],
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
