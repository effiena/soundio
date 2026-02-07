import os
from urllib.parse import quote
from flask import Flask, render_template, send_file, send_from_directory, jsonify

app = Flask(__name__)

MUSIC_DIR = os.path.join(app.static_folder, "music")

# ------------------ Flask Routes ------------------
@app.route("/")
def index():
    # Only include actual MP3 files that exist
    files = [
        f for f in os.listdir(MUSIC_DIR)
        if f.lower().endswith(".mp3") and os.path.isfile(os.path.join(MUSIC_DIR, f))
    ]
    files.sort(key=str.lower)

    # URL-encode for frontend
    encoded_playlist = [quote(f) for f in files]

    return render_template(
        "index.html",
        playlist=files,
        encoded_playlist=encoded_playlist,
        zip=zip
    )

@app.route("/music/<path:filename>")
def music(filename):
    file_path = os.path.join(MUSIC_DIR, filename)
    if os.path.isfile(file_path):
        return send_file(file_path, mimetype="audio/mpeg", as_attachment=False, conditional=True)
    else:
        # Return 404 if file not found
        return "File not found", 404

@app.route("/songs")
def songs():
    files = [
        f for f in os.listdir(MUSIC_DIR)
        if f.lower().endswith(".mp3") and os.path.isfile(os.path.join(MUSIC_DIR, f))
    ]
    return jsonify({"playlist": files})

@app.route("/manifest.json")
def manifest():
    return send_from_directory('.', 'manifest.json')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
