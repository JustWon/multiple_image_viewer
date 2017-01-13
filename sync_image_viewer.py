import cv2
import numpy as np


def seq_range(seq_idx):
    if seq_idx == "20161204_231541":
        start = 30
        end = 100
        sync_list=[]
    elif seq_idx == "20161204_232513":
        start = 60
        end = 100
        sync_list = [74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 100]
    elif seq_idx == "20161204_232836":
        start = 30
        end = 150
        sync_list = []
    elif seq_idx == "20161204_233533":
        start = 33
        end = 80
        sync_list = [34, 35, 36, 37, 38, 39, 42, 44, 45, 46, 47, 48, 49, 50, 51, 52, 56, 57, 58, 59, 60, 61, 62, 63, 64,
                     65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80]
    elif seq_idx == "20170113_142649":
        start = 0
        end = 100
        sync_list = range(start, end)
    elif seq_idx == "20170113_143623":
        start = 0
        end = 100
        sync_list = range(start, end)

    return start, end, sync_list



seq_idx = "20170113_143623"
sandbox_path = "c:/Users/DONGWON/Desktop/20170113 Experiment/server/%s/still" % (seq_idx)
start_frame=0;
end_frame=0;
mode = 1
start_frame, end_frame, sync_idx_list= seq_range(seq_idx)

frame_idx = start_frame
while(True):

    if frame_idx not in sync_idx_list:
        frame_idx = frame_idx+1
        continue

    total_img_stack = []
    ori_img_stack =[]
    img_stack = []
    for i in [0,1,2,3]:
        # filename = "d:/Sequences/20170106 3D Recon Based MVDG Test/conventional/%s/input/cam%d/color%d_%d.bmp" % (seq_idx,i,i, frame_idx)
        filename = "%s/color%d_%d.bmp" % (sandbox_path,i,frame_idx)

        img = cv2.imread(filename)
        ori_img_stack.append(img)
        res = cv2.resize(img, (0,0), fx=0.25, fy = 0.25)
        img_stack.append(res)
    color_row = np.hstack(img_stack)
    total_img_stack.append(color_row)

    total_img_stack.append(ori_img_stack[0]/4 + ori_img_stack[1]/4 + ori_img_stack[2]/4 + ori_img_stack[3]/4)

    total_img = np.vstack(total_img_stack)
    cv2.imshow("total_img", total_img)
    print frame_idx

    ch = cv2.waitKey()
    # print "ch = %d" %ch
    if ch == 2555904: # Right arrow
        frame_idx = min(frame_idx + 1, end_frame)
    elif ch == 2424832: # Left arrow
        frame_idx = max(frame_idx - 1, start_frame)
    elif ch == 2359296: # Home
        frame_idx = start_frame
    elif ch == 2293760:  # End
        frame_idx = end_frame
    elif ch == 32: # Space
        if frame_idx not in sync_idx_list:
            sync_idx_list.append(frame_idx)
        frame_idx = min(frame_idx + 1, end_frame)
    elif ch == 27: # ESC
        exit()
    elif ch == 112:
        print "sync_idx_list"
        print sync_idx_list