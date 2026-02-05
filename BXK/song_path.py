from tkinter import Tk, Button, filedialog
from playsound import playsound
import threading

playlist = []
current_index = 0
song_thread = None

def add_songs():
    global playlist
    files = filedialog.askopenfilenames(filetypes=[("MP3 Files", "*.mp3")])
    playlist.extend(files)
    print("Added songs:", playlist)

def play_song():
    global song_thread
    if playlist:
        # Play in separate thread to avoid freezing GUI
        def play():
            playsound(playlist[current_index], block=True)
        song_thread = threading.Thread(target=play)
        song_thread.start()

root = Tk()
root.title("MP3 Player")
Button(root, text="Add Songs", command=add_songs).pack()
Button(root, text="Play", command=play_song).pack()
root.mainloop()
