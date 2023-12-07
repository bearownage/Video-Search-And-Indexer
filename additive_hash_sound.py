import wave
import numpy as np
import os
import time
import json
from media_player_app import MediaPlayerApp

def get_audio_values(file_path, is_query_wav):
    with wave.open(file_path, 'rb') as wave_file:
        # Get audio file parameters
        frames_per_second = 30
        channels = wave_file.getnchannels()
        num_frames = wave_file.getnframes()
        frame_rate = wave_file.getframerate()
        frames_to_skip = int(frame_rate / frames_per_second)
        audio_value_to_frame_index_map={}
        frame_index_to_audio_map={}
        # print("Number of frames:" + str(num_frames))
        # print("Framerate: " + str(wave_file.getframerate()))

        # Read all frames
        frames = wave_file.readframes(num_frames)
        # print(frames)

        # Convert frames to NumPy array
        audio_array = np.frombuffer(frames, dtype=np.int16)
        # print("1Audio array len: " + str(len(audio_array)))

        # Split the array into channels
        audio_array = audio_array.reshape((-1, channels))

        # Iterate over frames and get audio values
        frame_num = 0
        # print("Audio array len: " + str(len(audio_array)))
        for i in range(0, len(audio_array), frames_to_skip):
            frame = audio_array[i]
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
            print("Processing file: " + str(file))
            full_video_audio, dummy2 = get_audio_values(os.path.join(path, file), False)
            file_path = "audio_signatures_" + str(file).split(".")[0] + ".json"
            with open(file_path, "w") as file:
                json.dump(full_video_audio, file)

    """
    query_file_path = './dataset/Queries/Audios/video6_1.wav'
    query_file_mp4_path = "./dataset/Videos/video6.mp4"
    dummy1, frame_index_to_audio_map_query = get_audio_values(query_file_path, True)
    start_frame_val = frame_index_to_audio_map_query[1]

    signature_name = query_file_path.split("/")[-1].split("_")[0] + ".wav_audio_signatures.json"
    file_path = "./" + signature_name
    with open(file_path, "r") as file:
        frame_signatures = json.load(file)
        print(frame_signatures[str(start_frame_val)])
    
    app = MediaPlayerApp(query_file_mp4_path, float(12241)/30)
    app.mainloop()
    """
    