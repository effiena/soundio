from urllib.parse import quote
from flask import Flask, render_template, send_from_directory, url_for, request, jsonify, send_file
import os
import random

app = Flask(__name__)

#[build]#
builder = "NIXPACKS"

#[deploy]#
startCommand = "gunicorn app:app"

# Path to the music folder
MUSIC_DIR = os.path.join(app.static_folder, "music")

# ------------------ Flask Routes ------------------
@app.route("/")
def index():
    files = os.listdir(MUSIC_DIR)
    playlist = [f for f in files if f.lower().endswith(".mp3")]
    playlist.sort(key=str.lower)
    encoded_playlist = [quote(f) for f in playlist]

    # Pass zip explicitly to Jinja2
    return render_template(
        "index.html",
        playlist=playlist,
        encoded_playlist=encoded_playlist,
        zip=zip  # <-- add this
    )

@app.route("/music/<path:filename>")
def music(filename):
    file_path = os.path.join("static", "music", filename)
    return send_file(
        file_path,
        mimetype="audio/mpeg",
        as_attachment=False,
        conditional=True
    )
@app.route('/manifest.json')
def manifest():
    return send_from_directory('.', 'manifest.json')


@app.route('/license.txt')
def license_file():
    return send_from_directory('.', 'license.txt')


# -------- AUTO LANGUAGE DETECTION --------
malay_keywords = [
    "siti","search","exists","ukays","spring","angan", "sepi",
    "lagu","melayu","jamal","amy","cinta","sayang", "sendiri","kau","hampa","aishah","janji","aku","ku","ziana","dan","di","dag","intan","kasih","kasihku","kasihmu","ella"
]

def detect_language(filename):
    # detect Chinese characters
    for c in filename:
        if '\u4e00' <= c <= '\u9fff':
            return "Mandarin"  # matches dropdown

    name = filename.lower()

    for k in malay_keywords:
        if k in name:
            return "Malay"

    return "English"

@app.route("/songs")
def songs():
    files = [f for f in os.listdir(MUSIC_DIR) if f.lower().endswith(".mp3")]
    data = []

    for f in files:
        lang = detect_language(f)
        encoded = quote(f)
        data.append({
            "name": f,
            "url": f"/music/{encoded}",
            "genre": lang
        })

    return jsonify(data)
    for f in files:
        lang = detect_language(f)
        encoded = quote(f)
        path = f"/music/{encoded}"
        data[lang].append({
            "name": f,
            "url": path
        })

    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


