from frame import *
import cv2
import numpy as np
import sys

def process_shot_list(videopath) :
    print("Processing shot list for " + videopath)
    videopath_name = videopath[:videopath.index('.')]
    capture = cv2.VideoCapture(str(videopath))
    curr_frame = None
    prev_frame = None
    frame_diffs = []
    frames = []
    success, frame = capture.read()
    i = 0
    FRAME = Frame(0, 0)
    print("Calculating frame differences...")
    while (success):
        luv = cv2.cvtColor(frame, cv2.COLOR_BGR2LUV)
        curr_frame = luv
        """
        
        calculate the difference between frames 
        
        """

        if curr_frame is not None and prev_frame is not None:
            diff = cv2.absdiff(curr_frame, prev_frame)
            diff_sum = np.sum(diff)
            diff_sum_mean = diff_sum / (diff.shape[0] * diff.shape[1])

            frame_diffs.append(diff_sum_mean)
            frame = Frame(i, diff_sum_mean)
            frames.append(frame)
        elif curr_frame is not None and prev_frame is None:
            diff_sum_mean = 0

            frame_diffs.append(diff_sum_mean)
            frame = Frame(i, diff_sum_mean)
            frames.append(frame)

        prev_frame = curr_frame
        i = i + 1
        success, frame = capture.read()
    capture.release()


    # detect the possible frame
    print("Detecting possible frames...")
    frame_return, start_id_spot_old, end_id_spot_old = FRAME.find_possible_frame(frames)

    # optimize the possible frame
    print("Optimizing possible frames...")
    try:
        new_frame, start_id_spot, end_id_spot = FRAME.optimize_frame(frame_return, frames)
    except:
        new_frame = []
        start_id_spot = []
        end_id_spot = []

    # store the result
    output_filepath = videopath_name + '_shots.txt'
    print("Writing shot list to " + output_filepath)
    start = np.array(start_id_spot)[np.newaxis, :]
    end = np.array(end_id_spot)[np.newaxis, :]
    spot = np.concatenate((start.T, end.T), axis=1)
    np.savetxt('./' + output_filepath, spot, fmt='%d', delimiter='\t')


if __name__ == "__main__":
    process_shot_list(sys.argv[1])