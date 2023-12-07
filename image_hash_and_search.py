import hashlib
import json

from PIL import Image
from tqdm import tqdm


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
    
def frame_generator(file_path, width=352, height=288, channels=3):
    frame_size = width * height * channels

    with open(file_path, 'rb') as file:
        while True:
            frame_data = file.read(frame_size)
            if not frame_data:
                break
            yield frame_data

rgb_file_path = 'video2.rgb'
frame_signatures = {}
frame_number = 0
for frame_data in tqdm(frame_generator(rgb_file_path)):
    hashsign = create_image_signature(parse_rgb_data(frame_data))
    frame_signatures[hashsign] = frame_number
    frame_number += 1
    # print(signature)
    
# Specify the file path where you want to save the data
file_path = "signatures2.json"

# Serialize the dictionary to a JSON string and write it to the file
with open(file_path, "w") as file:
    json.dump(frame_signatures, file)

# Keep in mind that image dims are 352x288