from pytube import YouTube
import os


def download_video(url, output_path):
    """
    Alternative to yt_dlp
    """
    yt = YouTube(url)
    streams = yt.streams.filter(progressive=True, file_extension='mp4')
    video = streams.order_by('resolution').first()
    video.download(f"{output_path}")


video_url = "https://www.youtube.com/watch?v=pn0wynLO5G8&ab_channel=ResearchRocks"
output_video_directory = f"{os.getcwd()}\\video"

'''downloading'''
download_video(video_url, output_video_directory)

