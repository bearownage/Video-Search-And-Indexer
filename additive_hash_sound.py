import wave
import numpy as np
import time
import json
from media_player_app import MediaPlayerApp

def get_audio_values(file_path, is_query_wav):
    audio_values = []

    with wave.open(file_path, 'rb') as wave_file:
        # Get audio file parameters
        channels = wave_file.getnchannels()
        sample_width = wave_file.getsampwidth()
        frame_rate = wave_file.getframerate()
        num_frames = wave_file.getnframes()
        audio_value_to_frame_index_map={}
        frame_index_to_audio_map={}

        # Read all frames
        frames = wave_file.readframes(num_frames)

        # Convert frames to NumPy array
        audio_array = np.frombuffer(frames, dtype=np.int16)

        # Split the array into channels
        audio_array = audio_array.reshape((-1, channels))

        # Iterate over frames and get audio values
        frame_num = 0
        print("Audio array len: " + str(len(audio_array)))
        for frame in audio_array:
            frame_num += 1
            # For mono audio, frame contains a single value
            # For stereo audio, frame contains two values (left and right)
            sum = frame[0]
            if is_query_wav:
                audio_value_to_frame_index_map[int(sum)] = [frame]
                frame_index_to_audio_map[frame_num] = int(sum)
                return audio_value_to_frame_index_map, frame_index_to_audio_map

            frame_index_to_audio_map[frame_num] = sum
            if sum in audio_value_to_frame_index_map:
                audio_value_to_frame_index_map[int(sum)].append(frame_num)
            else:
                audio_value_to_frame_index_map[int(sum)] = [frame_num]

            # print(frame.tolist())
            # audio_values.append(frame.tolist())

    return audio_value_to_frame_index_map, frame_index_to_audio_map

if __name__ == "__main__":
    wav_file_path = './dataset/Videos/Audios/video6.wav'
    query_file_path = './dataset/Queries/Audios/video6_1.wav'
    full_video_audio, dummy2 = get_audio_values(wav_file_path, False)
    dummy , frame_index_to_audio_map_query = get_audio_values(query_file_path, True)
    start_frame_val = frame_index_to_audio_map_query[1]
    print(full_video_audio[start_frame_val])
    # Specify the file path where you want to save the data
    file_path = "audio_signatures.json"

    # Serialize the dictionary to a JSON string and write it to the file
    with open(file_path, "w") as file:
        json.dump(full_video_audio, file)



"""
if __name__ == "__main__":
    app = MediaPlayerApp("./dataset/Videos/video6.mp4", 408.125161)
    app.mainloop()
"""

"""
if __name__ == "__main__":
    wav_file_path = './dataset/Videos/Audios/video6.wav'
    query_file_path = './dataset/Queries/Audios/video6_1.wav'
    query_file_mp4_path = './dataset/Videos/video6.mp4'
    window_size = 20.0  # in seconds
    hop_size = 0.1  # in seconds

    window_values=process_wav_file(wav_file_path, window_size, hop_size)
    query_file = wave.open(query_file_path, 'rb')
    query_hash_value=create_hash_value_for_audio_window(query_file, 0)
    #print("Query: " + str(query_hash_value))
    if query_hash_value in window_values:
        print("Hit!")
        window_info_list = window_values[query_hash_value]
        for window_info in window_info_list:
            app = MediaPlayerApp(query_file_mp4_path, (window_info.start_second * 1000))
            app.mainloop()
            print(f"Hash Value: {query_hash_value}, Start Frame: {window_info.start_frame}, End Frame: {window_info.end_frame}, Window Size: {window_info.window_size}, Start Second: {window_info.start_second}, End Second: {window_info.end_second}")
"""
