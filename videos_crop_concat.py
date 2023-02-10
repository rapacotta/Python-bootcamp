import os
import cv2
from moviepy.editor import VideoFileClip, concatenate_videoclips
import numpy as np

path = "C:/Users/biagini.WISMAIN/Desktop/videos for python final project/"   #to be replaced with the path of the folder containing the starting videos
video_list = os.listdir(path)
path_full_video = path + 'video_full_length.mp4'

#loads the clips in moviepy
video_clips = []
for clip in video_list:
    video_clips.append(VideoFileClip(path + clip))

#select the videos per arena umber and concatenate them saving them as 1 full video
full_length = concatenate_videoclips(video_clips, method='compose')
full_length.write_videofile(path_full_video)



#useful variable for later use
zero, mid_h, mid_w, full_h, full_w = 0, 540, 630, 1080, 1440  #Coordinates
fourcc = cv2.VideoWriter_fourcc(*'avc1')


#iteration over the list of files to open them in opencv(cv2). It also prepares to write the output file for the video of each single arenas. 
cap = cv2.VideoCapture(path_full_video)

#getting some info fro the original files
frame_number, fps = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), int(cap.get(cv2.CAP_PROP_FPS))
frame_w, frame_h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(frame_number, fps, frame_w, frame_h)

#initialize the output of the cropped video (1 video per arena)
arena_1 = cv2.VideoWriter(path + f'arena1.mp4', fourcc, fps, (mid_w, mid_h))
arena_2 = cv2.VideoWriter(path + f'arena2.mp4', fourcc, fps, (full_w - mid_w, mid_h))
arena_3 = cv2.VideoWriter(path + f'arena3.mp4', fourcc, fps, (full_w - mid_w, full_h - mid_h))
arena_4 = cv2.VideoWriter(path + f'arena4.mp4', fourcc, fps, (mid_w, full_h - mid_h))

while(cap.isOpened()):
    ret, frame = cap.read()

    if ret==True:
        crop_frame_1 = frame[zero:zero+mid_h, zero:zero+mid_w]   #crop for arena 1
        crop_frame_2 = frame[zero:zero+mid_h, mid_w:full_w]   #crop for arena 2
        crop_frame_3 = frame[mid_h:full_h, mid_w:full_w]   #crop for arena 3
        crop_frame_4 = frame[mid_h:full_h, zero:mid_w]   #crop for arena 4

        #writing the output files
        arena_1.write(crop_frame_1)
        arena_2.write(crop_frame_2)
        arena_3.write(crop_frame_3)
        arena_4.write(crop_frame_4)

        #showing the files that will be generated; a kind of preview.
        cv2.imshow('arena_1', crop_frame_1)
        cv2.imshow('arena_2', crop_frame_2)
        cv2.imshow('arena_3', crop_frame_3)
        cv2.imshow('arena_4', crop_frame_4)

        #press the key q to quite the current video analysis. Press q to make the script end.
        if cv2.waitKey(10) == ord('q'):
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()