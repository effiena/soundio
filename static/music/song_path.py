import tkinter as tk
from tkinter import filedialog, ttk
import pygame
import os
from mutagen.mp3 import MP3
import time
import random

# ------------------ Initialize ------------------
pygame.mixer.init()

playlist = []
current_index = -1
paused = False
duration = 0
user_dragging = False
start_time = 0
elapsed_time = 0
shuffle = False
loop = False

# ------------------ Functions ------------------
def add_songs():
    files = filedialog.askopenfilenames(filetypes=[("MP3 Files", "*.mp3")])
    for file in files:
        playlist.append(file)
        listbox.insert(tk.END, os.path.basename(file))

def delete_song():
    global playlist, current_index
    if listbox.curselection():
        idx = listbox.curselection()[0]
        del playlist[idx]
        listbox.delete(idx)
        if idx == current_index:
            stop_song()
            current_index = -1
        elif idx < current_index:
            current_index -= 1

def highlight_song():
    listbox.selection_clear(0, tk.END)
    if current_index >= 0:
        listbox.selection_set(current_index)
        listbox.see(current_index)

def play_song(index=None):
    global current_index, paused, duration, start_time, elapsed_time

    # Resume if paused
    if paused and index is None and current_index != -1:
        pygame.mixer.music.unpause()
        paused = False
        start_time = time.time() - elapsed_time
        return

    # Choose song
    if index is not None:
        current_index = index
    elif listbox.curselection():
        current_index = listbox.curselection()[0]
    elif current_index == -1:
        return

    pygame.mixer.music.load(playlist[current_index])
    pygame.mixer.music.play()
    paused = False
    elapsed_time = 0
    start_time = time.time()
    highlight_song()

    # Get duration
    try:
        audio = MP3(playlist[current_index])
        duration = int(audio.info.length)
    except:
        duration = 0

    progress_slider.config(to=duration)

def pause_song():
    global paused, elapsed_time
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        paused = True
        elapsed_time = time.time() - start_time

def stop_song():
    global paused, elapsed_time
    pygame.mixer.music.stop()
    paused = False
    elapsed_time = 0
    progress_slider.set(0)
    current_time_label.config(text="00:00")

def next_song():
    global current_index
    if not playlist:
        return

    if shuffle:
        # Pick random song
        current_index = random.randint(0, len(playlist)-1)
    elif loop:
        # Keep the same song
        pass
    else:
        current_index = (current_index + 1) % len(playlist)

    play_song(current_index)

def prev_song():
    global current_index
    if not playlist:
        return
    current_index = (current_index - 1) % len(playlist)
    play_song(current_index)

# ------------------ Progress ------------------
def update_progress():
    global elapsed_time

    if current_index >= 0:
        if pygame.mixer.music.get_busy() and not user_dragging:
            elapsed_time = time.time() - start_time
            if elapsed_time > duration:
                elapsed_time = duration

            progress_slider.set(elapsed_time)
            current_time_label.config(text=format_time(int(elapsed_time)))
            total_time_label.config(text=format_time(duration))

        elif not pygame.mixer.music.get_busy() and not paused and playlist:
            # Auto next song respecting shuffle & loop
            if shuffle:
                next_song()
            elif loop:
                play_song(current_index)
            else:
                if current_index + 1 < len(playlist):
                    next_song()
                else:
                    stop_song()

    root.after(50, update_progress)

def seek_start(event):
    global user_dragging
    user_dragging = True

def seek_end(event):
    global user_dragging, start_time, elapsed_time

    if current_index >= 0 and playlist:
        val = progress_slider.get()
        try:
            pygame.mixer.music.play()
            pygame.mixer.music.set_pos(val)
            start_time = time.time() - val
            elapsed_time = val
            if paused:
                pygame.mixer.music.pause()
        except:
            pass

    user_dragging = False

def play_selected_song(event):
    if listbox.curselection():
        play_song(listbox.curselection()[0])

def shuffle_toggle():
    global shuffle
    shuffle = not shuffle
    shuffle_btn.config(bg="#FFD700" if shuffle else "#FFFACD")

def loop_toggle():
    global loop
    loop = not loop
    loop_btn.config(bg="#FFD700" if loop else "#FFFACD")

def format_time(sec):
    m = sec // 60
    s = sec % 60
    return f"{m:02d}:{s:02d}"

# ------------------ GUI ------------------
root = tk.Tk()
root.title("MP3 Player")
root.geometry("450x550")
root.configure(bg="#FFFACD")  # Softer yellow

# Playlist
listbox = tk.Listbox(root, bg="#FFFFE0", fg="#000000", selectbackground="#FFD700", font=("Helvetica",12))
listbox.pack(pady=10, fill=tk.BOTH, expand=True)
listbox.bind("<Double-Button-1>", play_selected_song)

# Controls
btn_style = {"bg":"#FFFACD","fg":"#000000","width":6,"height":1,"font":("Helvetica",10,"bold"),"relief":"flat"}
ctrl_frame = tk.Frame(root, bg="#FFFACD")
ctrl_frame.pack(pady=5)

tk.Button(ctrl_frame, text="Add", command=add_songs, **btn_style).grid(row=0,column=0,padx=2)
tk.Button(ctrl_frame, text="Del", command=delete_song, **btn_style).grid(row=0,column=1,padx=2)
tk.Button(ctrl_frame, text="Prev", command=prev_song, **btn_style).grid(row=0,column=2,padx=2)
tk.Button(ctrl_frame, text="Play", command=play_song, **btn_style).grid(row=0,column=3,padx=2)
tk.Button(ctrl_frame, text="Pause", command=pause_song, **btn_style).grid(row=0,column=4,padx=2)
tk.Button(ctrl_frame, text="Next", command=next_song, **btn_style).grid(row=0,column=5,padx=2)
tk.Button(ctrl_frame, text="Stop", command=stop_song, **btn_style).grid(row=0,column=6,padx=2)

shuffle_btn = tk.Button(ctrl_frame, text="Shuffle", command=shuffle_toggle, **btn_style)
shuffle_btn.grid(row=1,column=2,padx=2)

loop_btn = tk.Button(ctrl_frame, text="Loop", command=loop_toggle, **btn_style)
loop_btn.grid(row=1,column=3,padx=2)

# Progress bar
progress_frame = tk.Frame(root, bg="#FFFACD")
progress_frame.pack(pady=10)
current_time_label = tk.Label(progress_frame, text="00:00", bg="#FFFACD", fg="#000000")
current_time_label.pack(side=tk.LEFT)

progress_slider = ttk.Scale(progress_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=250)
progress_slider.pack(side=tk.LEFT, padx=5)

total_time_label = tk.Label(progress_frame, text="--:--", bg="#FFFACD", fg="#000000")
total_time_label.pack(side=tk.LEFT)

progress_slider.bind("<ButtonPress-1>", seek_start)
progress_slider.bind("<ButtonRelease-1>", seek_end)

# Start progress updates
update_progress()

root.mainloop()
