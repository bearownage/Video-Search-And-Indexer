import wave
import numpy as np
import os
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
    path = "./dataset/Videos/Audios"
    files = os.listdir(path)
    for file in files:
        if os.path.isfile(os.path.join(path, file)):
            full_video_audio, dummy2 = get_audio_values(os.path.join(path, file), False)
            file_path = str(file) + "_audio_signatures.json"
            with open(file_path, "w") as file:
                json.dump(full_video_audio, file)

    # wav_file_path = './dataset/Videos/Audios/video6.wav'
    # query_file_path = './dataset/Queries/Audios/video6_1.wav'
    # start_frame_val = frame_index_to_audio_map_query[1]
    # print(full_video_audio[start_frame_val])
    # Specify the file path where you want to save the data

    # Serialize the dictionary to a JSON string and write it to the file
    

    # dummy , frame_index_to_audio_map_query = get_audio_values(query_file_path, True)