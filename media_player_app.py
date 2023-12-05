import os
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')

import tkinter as tk
import vlc
from tkinter import filedialog
from datetime import timedelta

class MediaPlayerApp(tk.Tk):
    def __init__(self, file_path, offset):
        super().__init__()
        self.title("Media Player")
        self.geometry("800x600")
        self.configure(bg="#f0f0f0")
        self.initialize_player(file_path, offset)

    def initialize_player(self, file_path, offset):
        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()
        # Load the video file
        self.media = self.instance.media_new(file_path)
        self.media.add_option('start-time=' + str(int(offset/1000)))
        # Set the media to the player
        self.media_player.set_media(self.media)
        #self.current_file = file_path
        self.playing_video = False
        self.video_paused = False
        self.create_widgets()
        self.start_time=offset
        self.set_video_position(int(self.start_time))
    
    def create_widgets(self):
        self.media_canvas = tk.Canvas(self, bg="black", width=800, height=400)
        self.media_canvas.pack(pady=10, fill=tk.BOTH, expand=True)
        self.control_buttons_frame = tk.Frame(self, bg="#f0f0f0")
        self.control_buttons_frame.pack(pady=5)

        self.play_button = tk.Button(
            self.control_buttons_frame,
            text="Play",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self.play_video,
        )
        self.play_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.pause_button = tk.Button(
            self.control_buttons_frame,
            text="Pause",
            font=("Arial", 12, "bold"),
            bg="#FF9800",
            fg="white",
            command=self.pause_video,
        )
        self.pause_button.pack(side=tk.LEFT, padx=10, pady=5)
        self.stop_button = tk.Button(
            self.control_buttons_frame,
            text="Reset",
            font=("Arial", 12, "bold"),
            bg="#F44336",
            fg="white",
            command=self.reset,
        )
        self.stop_button.pack(side=tk.LEFT, pady=5)
    
    def play_video(self):
        if not self.playing_video:
            #media = self.instance.media_new(self.current_file)
            #self.media_player.set_media(media)
            self.media_player.set_hwnd(self.media_canvas.winfo_id())
            # self.media_player.set_time(self.start_time)
            self.media_player.play()
            self.playing_video = True

    def pause_video(self):
        if self.playing_video:
            if self.video_paused:
                self.media_player.play()
                self.video_paused = False
                self.pause_button.config(text="Pause")
            else:
                self.media_player.pause()
                self.video_paused = True
                self.pause_button.config(text="Resume")

    def reset(self):
        self.media.add_option('start-time=0')
        # Set the media to the player
        self.media_player.set_media(self.media)
        if self.playing_video:
            self.media_player.stop()
            self.playing_video = False

    def set_video_position(self, value):
        print(value)
        if self.playing_video == False:
            print("Here!")
            total_duration = self.media.get_duration()
            start_position = value / total_duration
            self.media_player.set_position(start_position)
            #self.media_player.get_media_player().set_time(value)
            #print(self.media_player.get_time())
        if self.playing_video:
            total_duration = self.media_player.get_length()
            position = int((float(value) / 100) * total_duration)
            self.media_player.set_time(position)