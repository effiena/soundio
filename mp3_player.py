import tkinter as tk
from tkinter import filedialog, ttk
import pygame
import os
from mutagen.mp3 import MP3
import time

# ------------------ Initialize ------------------
pygame.mixer.init()

playlist = []
current_index = -1
paused = False
song_length = 0
start_time = 0
user_dragging = False

# ------------------ Functions ------------------
def add_songs():
    files = filedialog.askopenfilenames(filetypes=[("MP3 Files", "*.mp3")])
    for file in files:
        playlist.append(file)
        listbox.insert(tk.END, os.path.basename(file))

def highlight_song():
    listbox.selection_clear(0, tk.END)
    if 0 <= current_index < len(playlist):
        listbox.selection_set(current_index)
        listbox.see(current_index)

def play_song():
    global current_index, paused, song_length, start_time
    if listbox.curselection():
        selected = listbox.curselection()[0]
    else:
        selected = current_index

    if selected == current_index and paused:
        pygame.mixer.music.unpause()
        paused = False
        start_time = time.time() - progress_slider.get()
        return

    if 0 <= selected < len(playlist):
        current_index = selected
        pygame.mixer.music.load(playlist[current_index])
        pygame.mixer.music.play()
        paused = False
        highlight_song()
        try:
            audio = MP3(playlist[current_index])
            song_length = int(audio.info.length)
        except:
            song_length = 0
        progress_slider.config(to=song_length)
        start_time = time.time()

def pause_song():
    global paused
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        paused = True

def stop_song():
    global paused
    pygame.mixer.music.stop()
    paused = False
    progress_slider.set(0)
    current_time_label.config(text="00:00")

def next_song():
    global current_index
    if playlist:
        current_index = (current_index + 1) % len(playlist)
        play_song()

def prev_song():
    global current_index
    if playlist:
        current_index = (current_index - 1 + len(playlist)) % len(playlist)
        play_song()

def elapsed_time():
    if paused:
        return progress_slider.get()
    elif pygame.mixer.music.get_busy():
        return time.time() - start_time
    else:
        return 0

# ------------------ Progress ------------------
def update_progress():
    if 0 <= current_index < len(playlist):
        if pygame.mixer.music.get_busy() and not user_dragging:
            t = elapsed_time()
            progress_slider.set(t)
            current_time_label.config(text=format_time(int(t)))
            total_time_label.config(text=format_time(song_length))
        elif not pygame.mixer.music.get_busy() and not paused and playlist:
            # Song ended -> auto-next
            next_song()
    root.after(500, update_progress)

def seek_start(event):
    global user_dragging
    user_dragging = True

def seek_end(event):
    global user_dragging, start_time
    if 0 <= current_index < len(playlist):
        val = progress_slider.get()
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.play(start=val)
            start_time = time.time() - val
            if paused:
                pygame.mixer.music.pause()
        except:
            pass
    user_dragging = False

def format_time(sec):
    m = sec // 60
    s = sec % 60
    return f"{m:02d}:{s:02d}"

# ------------------ GUI ------------------
root = tk.Tk()
root.title("SOUNDIO")
root.geometry("400x500")
root.configure(bg="#1a1a1a")

# Playlist
listbox = tk.Listbox(root, bg="#333333", fg="#FFD700", selectbackground="#FFA500", font=("Helvetica",12))
listbox.pack(pady=10, fill=tk.BOTH, expand=True)

# Controls
btn_style = {"bg":"#FFD700","fg":"#1a1a1a","width":6,"height":1,"font":("Helvetica",10,"bold"),"relief":"flat"}
ctrl_frame = tk.Frame(root, bg="#1a1a1a")
ctrl_frame.pack(pady=5)
tk.Button(ctrl_frame, text="Add", command=add_songs, **btn_style).grid(row=0,column=0,padx=2)
tk.Button(ctrl_frame, text="Prev", command=prev_song, **btn_style).grid(row=0,column=1,padx=2)
tk.Button(ctrl_frame, text="Play", command=play_song, **btn_style).grid(row=0,column=2,padx=2)
tk.Button(ctrl_frame, text="Pause", command=pause_song, **btn_style).grid(row=0,column=3,padx=2)
tk.Button(ctrl_frame, text="Next", command=next_song, **btn_style).grid(row=0,column=4,padx=2)
tk.Button(ctrl_frame, text="Stop", command=stop_song, **btn_style).grid(row=0,column=5,padx=2)

# Progress
progress_frame = tk.Frame(root, bg="#1a1a1a")
progress_frame.pack(pady=10)
current_time_label = tk.Label(progress_frame, text="00:00", bg="#1a1a1a", fg="#FFD700")
current_time_label.pack(side=tk.LEFT)
progress_slider = ttk.Scale(progress_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=250)
progress_slider.pack(side=tk.LEFT, padx=5)
total_time_label = tk.Label(progress_frame, text="--:--", bg="#1a1a1a", fg="#FFD700")
total_time_label.pack(side=tk.LEFT)

progress_slider.bind("<ButtonPress-1>", seek_start)
progress_slider.bind("<ButtonRelease-1>", seek_end)

update_progress()
root.mainloop()
