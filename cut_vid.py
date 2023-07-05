import cv2
import os

def extractImages(pathIn, pathOut, frame_list):
    count = 0
    vidcap = cv2.VideoCapture(pathIn)
    success, image = vidcap.read()
    #success = True
    while success:
        vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))    # added this line
        success, image = vidcap.read()
        print('Read a new frame: ', success)
        if count in frame_list:
            cv2.imwrite(pathOut + "\\frame%d.jpg" % count, image)     # save frame as JPEG file
        count = count + 1

saved_video_directory = f"{os.getcwd()}\\video\\Download any Video using Python  Build Python Program to Download YouTube Videos.mp4"
output_image_directory = f"{os.getcwd()}\\image"

''' function '''

frame_list = [10, 20, 30]
extractImages(saved_video_directory, output_image_directory, frame_list)
