#!/usr/bin/env python
# coding: utf-8

# In[9]:


import wave
import numpy as np
import time

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
    

class VideoProgressBar(tk.Scale):
    def __init__(self, master, command, **kwargs):
        kwargs["showvalue"] = False
        super().__init__(
            master,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=800,
            command=command,
            **kwargs,
        )
        self.bind("<Button-1>", self.on_click)

    def on_click(self, event):
            if self.cget("state") == tk.NORMAL:
                value = (event.x / self.winfo_width()) * 100
                print(value)
                self.set(value)

class WindowInfo:
    def __init__(self, start_frame, end_frame, window_size, start_second, end_second):
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.window_size = window_size
        self.start_second = start_second
        self.end_second = end_second

def additive_hash(frame):
    hash_value = np.sum(frame)
    return hash_value

def create_hash_value_for_audio_window(wav_file, start_frame, window_size_frames):
    wav_file.setpos(start_frame)
    frames = wav_file.readframes(window_size_frames)
    frames_array = np.frombuffer(frames, dtype=np.int16)
    hash_value = additive_hash(frames_array)
    return hash_value

def process_wav_file(file_path, window_size, hop_size):
    windows_dict = {}
    wav_file = wave.open(file_path, 'rb')
    channels = wav_file.getnchannels()
    frame_rate = wav_file.getframerate()
    sample_width = wav_file.getsampwidth()
    num_frames = wav_file.getnframes()
    
    window_size_frames = int(window_size * frame_rate)
    print("Window size frames: " + str(window_size_frames))
    hop_size_frames = int(hop_size * frame_rate)
    
    for start_frame in range(0, num_frames-window_size_frames, hop_size_frames):
        hash_value = create_hash_value_for_audio_window(wav_file, start_frame, window_size_frames)
        window_info = WindowInfo(start_frame, start_frame + window_size_frames, window_size, start_frame / frame_rate, (start_frame + window_size_frames) / frame_rate)
        if hash_value in windows_dict:
            windows_dict[hash_value].append(window_info)
        else:
            windows_dict[hash_value] = [window_info]
    return windows_dict

        # for hash_value, window_info_list in windows_dict.items():
        #    for window_info in window_info_list:
               # print(f"Hash Value: {hash_value}, Start Frame: {window_info.start_frame}, End Frame: {window_info.end_frame}, Window Size: {window_info.window_size}")
"""
if __name__ == "__main__":
    app = MediaPlayerApp("./dataset/Videos/video6.mp4", 408 * 1000)
    app.mainloop()
"""
if __name__ == "__main__":
    wav_file_path = './dataset/Videos/Audios/video6.wav'
    query_file_path = './dataset/Queries/Audios/video6_1.wav'
    query_file_mp4_path = './dataset/Videos/video6.mp4'
    window_size = 20.0  # in seconds
    hop_size = 0.1  # in seconds

    window_values=process_wav_file(wav_file_path, window_size, hop_size)
    query_file = wave.open(query_file_path, 'rb')
    query_hash_value=create_hash_value_for_audio_window(query_file, 0, query_file.getframerate() * 20)
    #print("Query: " + str(query_hash_value))
    if query_hash_value in window_values:
        print("Hit!")
        window_info_list = window_values[query_hash_value]
        for window_info in window_info_list:
            app = MediaPlayerApp(query_file_mp4_path, (window_info.start_second * 1000))
            app.mainloop()
            print(f"Hash Value: {query_hash_value}, Start Frame: {window_info.start_frame}, End Frame: {window_info.end_frame}, Window Size: {window_info.window_size}, Start Second: {window_info.start_second}, End Second: {window_info.end_second}")