from shotdetection import *
import numpy as np
import sys

source_shotlists = ["video1_shots.txt", 
                    "video2_shots.txt", 
                    "video3_shots.txt",
                    "video4_shots.txt",
                    "video5_shots.txt",
                    "video6_shots.txt",
                    "video7_shots.txt",
                    "video8_shots.txt",
                    "video9_shots.txt",
                    "video10_shots.txt",
                    "video11_shots.txt",
                    "video12_shots.txt",
                    "video13_shots.txt",
                    "video14_shots.txt",
                    "video15_shots.txt",
                    "video16_shots.txt",
                    "video17_shots.txt",
                    "video18_shots.txt",
                    "video19_shots.txt",
                    "video20_shots.txt",]

def check_query_by_shots(queryvideopath):
    queryvideopath_name = queryvideopath[:queryvideopath.index('.')]
    
    print("query video is " + queryvideopath)

    process_shot_list(queryvideopath)

    query_shotlist = open(queryvideopath_name + "_shots.txt")
    query_shotlengths = []
    for line in query_shotlist.readlines():
        elems = line.split()
        start = int(elems[0])
        end = int(elems[1])
        shot_length = end - start
        query_shotlengths.append(shot_length)

    # only if query has more than 2 shotlengths
    if len(query_shotlengths) <= 2:
        print("inconclusive")
    else:
        sequences_by_source = []
        sequences_by_source_start_frames = []
        # for each source shotlist
        for sourceshotlist_path in source_shotlists:
            print("\nchecking " + sourceshotlist_path)
            source_shotlist = open(sourceshotlist_path)
            source_shotlengths = []
            source_shotstarts = []
            # read source file and store data in lists
            for line in source_shotlist.readlines():
                elems = line.split()
                start = int(elems[0])
                end = int(elems[1])
                length = end - start
                source_shotlengths.append(length)
                source_shotstarts.append(start)

            sequence_candidates = []
            sequence_candidates_start_frames = []
            for source_index in range(len(source_shotlengths) - 1):
                # print("source_index = " + str(source_index))
                seq_index = 0
                sequence = []
                sequence_start_frame = 0
                while True:
                    if seq_index >= len(query_shotlengths):
                        break
                    if (source_index + seq_index) >= len(source_shotlengths):
                        break

                    source_shot_length = source_shotlengths[source_index + seq_index]
                    query_shot_length = query_shotlengths[seq_index]

                    # if first or last in sequence, source length must be greater than query length
                    if seq_index == 0 or seq_index == len(query_shotlengths) - 1:
                        if source_shot_length < query_shot_length:
                            break
                    # if in middle, diff must be negligible
                    else:
                        diff = abs(source_shot_length - query_shot_length)
                        if diff > 1:
                            break

                    if seq_index >= 2:
                        print("  match " + str(seq_index) + " at index " + str(source_index + seq_index) + ": " + str(source_shot_length) + " and " + str(query_shot_length))

                    if seq_index == 0:
                        sequence_start_frame = source_index
                    sequence.append(source_shotstarts[source_index + seq_index])
                    seq_index += 1
                if len(sequence) >= 2:
                    sequence_candidates.append(sequence)
                    sequence_candidates_start_frames.append(sequence_start_frame)

            # only keep longest sequence as best sequence from this source
            print("sequence candidates:")
            print(*sequence_candidates)
            if len(sequence_candidates) > 0:
                max_length = 0
                max_index = 0
                for candidate in sequence_candidates:
                    if len(candidate) > max_length:
                        max_length = len(candidate)
                        max_index = sequence_candidates.index(candidate)
                longest_sequence = sequence_candidates[max_index]
                sequences_by_source.append(longest_sequence)
                sequences_by_source_start_frames.append(sequence_candidates_start_frames[max_index])
            else:
                print("no candidates")
                empty_seq = []
                sequences_by_source.append(empty_seq)
                sequences_by_source_start_frames.append(-1)

        # pick source with the longest sequence
        print("sequences by source")
        print(*sequences_by_source)
        print(*sequences_by_source_start_frames)
        max_length = 0
        max_index = None
        for sequence in sequences_by_source:
            if (max_length is None and len(sequence) > 0) or (max_length is not None and len(sequence) > max_length):
                max_length = len(sequence)
                max_index = sequences_by_source.index(sequence)
        if max_index is None:
            print("not sure")
            return None, None
        else:
            sourcefile = source_shotlists[max_index]
            startframe = sequences_by_source[max_index][0]

            sourcevideo = sourcefile[:sourcefile.index("_shots.txt")] + ".mp4"

            print("\nquery is from " + sourcevideo + " at frame " + str(startframe))
            return sourcevideo, startframe


if __name__ == "__main__":
    queryvideopath = sys.argv[1]
    check_query_by_shots(queryvideopath)