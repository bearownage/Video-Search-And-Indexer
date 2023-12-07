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
                    "video12_shots.txt",
                    "video13_shots.txt",
                    "video14_shots.txt",
                    "video15_shots.txt",
                    "video16_shots.txt",
                    "video17_shots.txt",
                    "video18_shots.txt",
                    "video19_shots.txt",
                    "video20_shots.txt",]

if __name__ == "__main__":
    queryvideopath = sys.argv[1]
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
    # remove first and last
    query_shotlengths.pop(0) 
    query_shotlengths.pop()

    # make list of shot lengths from query video (excluding first and last)
    # for each source shotlist
        # keep list of possible sequences 
        # for each shot length in source shotlist 
            # if first shot length matches first shot length
                # for each shot length after first 
                    # if shot length matches, add to sequence
                # add sequence to list of possible sequences
        # store list of possible sequences in list of sequences by source video 

    sequences_by_source = []
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
        for source_index in range(len(source_shotlengths) - 1):
            # print("source_index = " + str(source_index))
            seq_index = 0
            sequence = []
            while True:
                if seq_index >= len(query_shotlengths):
                    break
                if (source_index + seq_index) >= len(source_shotlengths):
                    break

                source_shot_length = source_shotlengths[source_index + seq_index]
                query_shot_length = query_shotlengths[seq_index]
                diff = abs(source_shot_length - query_shot_length)
                if diff > 1:
                    break

                print("  match " + str(seq_index) + " at index " + str(source_index + seq_index) + ": " + str(source_shot_length) + " and " + str(query_shot_length))
                sequence.append(source_shotstarts[source_index + seq_index])
                seq_index += 1
            if len(sequence) > 0:
                sequence_candidates.append(sequence)

        # only keep longest sequence as best sequence from this source
        if len(sequence_candidates) > 0:
            print("all candidates:")
            max_length = 0
            max_index = 0
            for candidate in sequence_candidates:
                print(*candidate)
                if len(candidate) > max_length:
                    max_length = len(candidate)
                    max_index = sequence_candidates.index(candidate)
            longest_sequence = sequence_candidates[max_index]
            sequences_by_source.append(longest_sequence)
        else:
            print("no candidates")
            empty_seq = []
            sequences_by_source.append(empty_seq)

    # pick source with the longest sequence
    max_length = 0
    max_index = 0
    for sequence in sequences_by_source:
        if len(sequence) > max_length:
            max_length = len(sequence)
            max_index = sequences_by_source.index(sequence)
    print("\nquery is from " + source_shotlists[max_index])


