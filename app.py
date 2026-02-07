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


@app.route('/LICENSE.txt')
def license_file():
    return send_from_directory('.', 'LICENSE.txt')

@app.route("/songs")
def songs():
    playlist = [f for f in os.listdir(MUSIC_DIR) if f.lower().endswith(".mp3")]
    return jsonify({"playlist": playlist})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


