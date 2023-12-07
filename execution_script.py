from PIL import Image
import json
import hashlib
import os
import time
import wave
import numpy as np

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
        frames = wave_file.readframes(num_frames)
    
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

def create_image_from_rgb(rgb_data, width, height):
    image = Image.new('RGB', (width, height))

    image.putdata(rgb_data)

    return image
    
def create_image_signature(rgb_image_info):
    rgb_bytes = bytes([val for tup in rgb_image_info for val in tup])

    hash_obj = hashlib.sha256()

    hash_obj.update(rgb_bytes)

    hex_digest = hash_obj.hexdigest()

    return hex_digest

def extract_first_frame_rgb(file_path, width=352, height=288, channels=3):
    frame_size = width * height * channels

    with open(file_path, 'rb') as file:
        frame_data = file.read(frame_size)

    return frame_data

def parse_rgb_data(raw_data):
    pixels = [raw_data[i:i+3] for i in range(0, len(raw_data), 3)]

    rgb_pixels = [(pixel[0], pixel[1], pixel[2]) for pixel in pixels]

    return rgb_pixels
    
def find_signature_in_hashmaps(signature, hashmaps, video_names):
    matches=[]
    for index in range(len(video_names)):
        hashmap = hashmaps[video_names[index]]
        if signature in hashmap:
            # TODO convert index into video name
            matches.append((video_names[index], hashmap[signature]))
    return matches
    
def load_json_files(keyword):
    #TODO convert this to a hashmap
    hashmaps = {}
    video_names= []
    path = "./"
    files = os.listdir(path)
    for file in files:
        if os.path.isfile(os.path.join(path, file)):
            # print("Processing file: " + str(file))
            if keyword in file and "json" in file:
                file_name=os.path.join(path, file)
                print(file_name)
                with open(file_name, "r") as file:
                    hashmap = json.load(file)
                    video_name = file_name.split("_")[-1]
                    hashmaps[video_name] = hashmap
                    video_names.append(video_name)
                    #hashmaps.append(hashmap)
    return hashmaps, video_names

if __name__ == "__main__":
    image_hashmaps, video_names = load_json_files("image")
    audio_hashmaps, _ = load_json_files("video")
    #print(image_hashmaps)
    start_time = time.time()
    #{"video1": {all the image signaure hashmap}}

    # TODO set these to command line args
    rgb_file_path = './dataset/Queries/RGB_Files/video1_1.rgb'
    query_file_path = './dataset/Queries/Audios/video1_1.wav'
    first_frame_data = extract_first_frame_rgb(rgb_file_path)
    first_frame_audio_data = dummy1, frame_index_to_audio_map_query = get_audio_values(query_file_path, True)
    rgb_pixels = parse_rgb_data(first_frame_data)


    # TODO Make mapping between image and audio hashmaps
    start_frame=0

    #TODO use video_name, not query
    video_name=""
    signature = create_image_signature(rgb_pixels)
    print("Digital Signature:", signature)
    image_signature_matches = find_signature_in_hashmaps(signature, image_hashmaps, video_names)
    if len(image_signature_matches) > 0:
        if (len(image_signature_matches) == 1):
            print("Match found in hashmaps:", image_signature_matches)

            start_frame=image_signature_matches[0][1]

            video_name = "./dataset/Videos/" + image_signature_matches[0][0].split(".")[0] + ".mp4"
        else:
            print("Multiple image matches found!")
            for matches in image_signature_matches:
                print("lol")
                # Take value in matches[0]
                # Grab corresponding audio hashmap
                # get(first_frame_audio_data)
                # check if frame number in images frame number  in audio values
            # Tiebreak
    else:
        print("No match found in hashmaps.")
    end_time = time.time()
    total_time = end_time - start_time
    print("Total time taken: " + str(total_time))
        
    # print("###################################")
    # print(frame_signatures[signature])
    print("###################################")
    print("Frame number of video start: " + str(start_frame))

    app = MediaPlayerApp(video_name, float(start_frame)/30)
    app.mainloop()
