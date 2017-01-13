import cv2
import numpy as np


def seq_range(seq_idx):
    if seq_idx == "20161204_231541":
        start = 30
        end = 100
        sync_list = range(start,end)
    elif seq_idx == "20161204_232513":
        start = 60
        end = 100
        sync_list = [74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 100]
    elif seq_idx == "20161204_232836":
        start = 30
        end = 150
        sync_list = range(start, end)
    elif seq_idx == "20161204_233533":
        start = 33
        end = 80
        sync_list = [34, 35, 36, 37, 38, 39, 42, 44, 45, 46, 47, 48, 49, 50, 51, 52, 56, 57, 58, 59, 60, 61, 62, 63, 64,
                     65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80]

    return start, end, sync_list

seq_idx = "20170113_142649"
sandbox_path = "c:/Users/DONGWON/Desktop/20170113 Experiment/server/%s/still/" % (seq_idx)
start_frame=0;
end_frame=0;
mode = 1
start_frame, end_frame, sync_list= seq_range(seq_idx)
frame_idx=start_frame

while(True):

    if frame_idx not in sync_list:
        frame_idx = frame_idx+1
        continue

    total_img_stack = []
    # # proposed depth
    img_stack = []
    for i in [0,1,2,3]:
        # filename = "d:/Sequences/20170106 3D Recon Based MVDG Test/proposed/%s/view%d_%d.png" % (seq_idx, i, frame_idx)
        img = cv2.imread(filename,0)
        equ = cv2.equalizeHist(img)
        res = cv2.resize(equ, (0,0), fx=0.25, fy = 0.25)
        res = cv2.cvtColor(res, cv2.COLOR_GRAY2BGR)
        img_stack.append(res)
    proposed_depth_row = np.hstack(img_stack)
    total_img_stack.append(proposed_depth_row)

    # conventional depth
    img_stack=[]
    for i in [1,2,3,4]:
        filename = "d:/Sequences/20170106 3D Recon Based MVDG Test/conventional/%s/output/Cam%d/cam_%d_%d.png" % (seq_idx,i,i, frame_idx)
        img = cv2.imread(filename,0)
        equ = cv2.equalizeHist(img)
        res = cv2.resize(equ, (0,0), fx=0.25, fy = 0.25)
        res = cv2.cvtColor(res, cv2.COLOR_GRAY2BGR)
        img_stack.append(res)
    conventional_depth_row = np.hstack(img_stack)
    total_img_stack.append(conventional_depth_row)
    # cv2.imshow("conventional_depth_row", conventional_depth_row)

    # color
    img_stack = []
    for i in [1,2,3,4]:
        filename = "d:/Sequences/20170106 3D Recon Based MVDG Test/conventional/%s/input/cam%d/color%d_%d.bmp" % (seq_idx,i,i, frame_idx)
        img = cv2.imread(filename)
        res = cv2.resize(img, (0,0), fx=0.25, fy = 0.25)
        img_stack.append(res)
    color_row = np.hstack(img_stack)
    total_img_stack.append(color_row)
    # cv2.imshow("color_row", color_row)

    img_stack = []
    for i in [1, 2, 3, 4]:
        depth_filename = "d:/Sequences/20170106 3D Recon Based MVDG Test/conventional/%s/output/Cam%d/cam_%d_%d.png" % (seq_idx,i, i, frame_idx)
        color_filename = "d:/Sequences/20170106 3D Recon Based MVDG Test/conventional/%s/input/cam%d/color%d_%d.bmp" % (seq_idx,i, i, frame_idx)
        depth_img = cv2.imread(depth_filename, 0)
        color_img = cv2.imread(color_filename)

        equ = cv2.equalizeHist(depth_img)
        depth_res = cv2.resize(equ, (0, 0), fx=0.25, fy=0.25)
        color_res = cv2.resize(color_img, (0, 0), fx=0.25, fy=0.25)
        depth_res = cv2.cvtColor(depth_res, cv2.COLOR_GRAY2BGR)

        overlay = cv2.addWeighted(depth_res, 0.5, color_res, 0.5,0)
        img_stack.append(overlay)

    overlay_row = np.hstack(img_stack)
    total_img_stack.append(overlay_row)
    # cv2.imshow("overlay_row", overlay_row)

    img_stack = []
    for i in [1,2,3,4]:
        depth_filename = "d:/Sequences/20170106 3D Recon Based MVDG Test/proposed/%s/view%d_%d.png" % (seq_idx,i-1, frame_idx)
        color_filename = "d:/Sequences/20170106 3D Recon Based MVDG Test/conventional/%s/input/cam%d/color%d_%d.bmp" % (seq_idx,i, i, frame_idx)
        depth_img = cv2.imread(depth_filename, 0)
        color_img = cv2.imread(color_filename)

        equ = cv2.equalizeHist(depth_img)
        depth_res = cv2.resize(equ, (0, 0), fx=0.25, fy=0.25)
        color_res = cv2.resize(color_img, (0, 0), fx=0.25, fy=0.25)
        depth_res = cv2.cvtColor(depth_res, cv2.COLOR_GRAY2BGR)

        overlay = cv2.addWeighted(depth_res, 0.5, color_res, 0.5, 0)
        img_stack.append(overlay)

    overlay_row = np.hstack(img_stack)
    total_img_stack.append(overlay_row)
    # cv2.imshow("overlay_row", overlay_row)


    total_img = np.vstack(total_img_stack)
    cv2.imshow("total_img", total_img)

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
    elif ch == 27: # ESC
        exit()