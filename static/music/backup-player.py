import tkinter as tk
from tkinter import filedialog
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Create window
root = tk.Tk()
root.title("Simple MP3 Player")
root.geometry("350x200")
root.configure(bg="black")

# Global variable for file
current_song = None

# Functions
def load_song():
    global current_song
    current_song = filedialog.askopenfilename(
        filetypes=[("MP3 Files", "*.mp3")]
    )
    song_label.config(text=current_song.split("/")[-1])

def play_song():
    if current_song:
        pygame.mixer.music.load(current_song)
        pygame.mixer.music.play()

def pause_song():
    pygame.mixer.music.pause()

def resume_song():
    pygame.mixer.music.unpause()

def stop_song():
    pygame.mixer.music.stop()

# UI Elements
song_label = tk.Label(
    root,
    text="No song loaded",
    bg="black",
    fg="yellow",
    font=("Arial", 10)
)
song_label.pack(pady=10)

btn_style = {
    "bg": "yellow",
    "fg": "black",
    "width": 10,
    "font": ("Arial", 10, "bold")
}

load_btn = tk.Button(root, text="Load", command=load_song, **btn_style)
load_btn.pack(pady=2)

play_btn = tk.Button(root, text="Play", command=play_song, **btn_style)
play_btn.pack(pady=2)

pause_btn = tk.Button(root, text="Pause", command=pause_song, **btn_style)
pause_btn.pack(pady=2)

resume_btn = tk.Button(root, text="Resume", command=resume_song, **btn_style)
resume_btn.pack(pady=2)

stop_btn = tk.Button(root, text="Stop", command=stop_song, **btn_style)
stop_btn.pack(pady=2)

# Run app
root.mainloop()
