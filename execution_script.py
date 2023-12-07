from PIL import Image
import json
import hashlib

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
    
def find_signature_in_hashmaps(signature, hashmaps):
    for hashmap in hashmaps:
        if signature in hashmap:
            return hashmap[signature]
    return None
    
def load_json_files(num_files):
    hashmaps = []
    for i in range(1, num_files + 1):
        file_name = f"signatures{i}.json"
        with open(file_name, "r") as file:
            hashmap = json.load(file)
            hashmaps.append(hashmap)
    return hashmaps

all_hashmaps = load_json_files(20)

rgb_file_path = 'video1_1.rgb'
first_frame_data = extract_first_frame_rgb(rgb_file_path)
rgb_pixels = parse_rgb_data(first_frame_data)

image = create_image_from_rgb(rgb_pixels, 352, 288)

image.show()

print(first_frame_data[:30])

file_path = "signatures.json"

# with open(file_path, "r") as file:
#     frame_signatures = json.load(file)

# print(frame_signatures)

signature = create_image_signature(rgb_pixels)
print("Digital Signature:", signature)

signature_match = find_signature_in_hashmaps(signature, all_hashmaps)
if signature_match is not None:
    print("Match found in hashmaps:", signature_match)
else:
    print("No match found in hashmaps.")
    
# print("###################################")
# print(frame_signatures[signature])