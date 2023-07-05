from pytube import YouTube
import cv2
import os


def download_video(url, output_path):
    yt = YouTube(url)
    streams = yt.streams.filter(progressive=True, file_extension='mp4')
    video = streams.order_by('resolution').first()
    video.download(output_path)
    title = yt.title
    title_updated = title.replace(" | ", " ")
    print(title_updated)


def extract_frame(video_path, output_path, sec):
    capture = cv2.VideoCapture(video_path)
    fps = capture.get(cv2.CAP_PROP_FPS)
    frame_number = int(fps * sec)

    # Set the capture position to the desired frame
    capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    # Read the frame
    ret, frame = capture.read()

    # Save the frame as an image
    cv2.imwrite(output_path, frame)

video_url = "https://www.youtube.com/watch?v=pn0wynLO5G8&ab_channel=ResearchRocks"
output_video_directory = f"{os.getcwd()}\\video"
#download_video(video_url, output_directory)
saved_video_directory = f"{output_video_directory}\\Download any Video using Python Build Python Program to Download YouTube Videos"
output_image_directory = f"{os.getcwd()}\\image"
second = 40
extract_frame(saved_video_directory, output_image_directory, second)