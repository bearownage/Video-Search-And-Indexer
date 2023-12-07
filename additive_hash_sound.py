import wave
import numpy as np
import time
from media_player_app import MediaPlayerApp

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
if __name__ == "__main__":
    app = MediaPlayerApp("./dataset/Videos/video6.mp4", 408.125161)
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
"""
