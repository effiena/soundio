from flask import Flask, render_template, send_from_directory, url_for, request, jsonify
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
    # get all mp3 files
    playlist = [f for f in os.listdir(MUSIC_DIR) if f.lower().endswith(".mp3")]
    return render_template("index.html", playlist=playlist)

@app.route("/music/<path:filename>")
def music(filename):
    file_path = os.path.join(MUSIC_DIR, filename)
    if not os.path.exists(file_path):
        return "File not found", 404

    # serve mp3 with headers for mobile/Cloudflare
    response = send_from_directory(MUSIC_DIR, filename, mimetype="audio/mpeg")
    response.headers["Accept-Ranges"] = "bytes"
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

@app.route("/songs")
def songs():
    playlist = [f for f in os.listdir(MUSIC_DIR) if f.lower().endswith(".mp3")]
    return jsonify({"playlist": playlist})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

