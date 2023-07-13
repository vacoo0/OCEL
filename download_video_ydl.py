import yt_dlp as youtube_dl
import cv2
import os

class YouTubeDownloader:
    def __init__(self, save_directory, resolution='360', format='mp4', framerate=None, audio=False):
        self.save_directory = save_directory
        self.resolution = resolution
        self.format = format
        self.framerate = framerate
        self.audio = audio
        self.video_title = None
        self.video_path = None
        self.frame_dir_path = None
    
    def download_video(self, video_url):
        with youtube_dl.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            self.video_title = info_dict.get('title', None)
            self.video_title = self.video_title.replace(' ', '_')

        ydl_opts = {
            'format': self._build_format_string(),
            'outtmpl': self._build_output_template(),
        }
        
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            self.video_title = info_dict.get('title', None)
            self.video_title = self.video_title.replace(' ', '_')
            ydl.download([video_url])
    
    def _build_format_string(self):
        if self.audio:
            format_string = f'bestvideo[height<={self.resolution}][ext={self.format}]+bestaudio[ext={self.format}]/best[height<={self.resolution}][ext={self.format}]'
        else:
            format_string = f'bestvideo[height<={self.resolution}][ext={self.format}]/best[height<={self.resolution}][ext={self.format}]'

        
        if self.framerate:
            format_string += f'/best[height<={self.resolution}][ext={self.format}][fps={self.framerate}]'
        
        return format_string
    
    def _build_output_template(self):
        self.video_path = f'{self.save_directory}/{self.video_title}.{self.format}'
        return self.video_path

    def extract_frames(self, path_out, frame_list):
        frame_list = [int(round(num)) for num in frame_list]
        count = 0
        vidcap = cv2.VideoCapture(self._build_output_template())
        success, image = vidcap.read()
        #success = True
        while success:
            vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))
            success, image = vidcap.read()
            print('Read a new frame: ', success)
            if count in frame_list:
                # cv2.imwrite(path_out + "\\frame%d.jpg" % count, image)
                print(f'{path_out}/{self.video_title}_frame{count:03}.jpg')
                cv2.imwrite(f'{path_out}/{self.video_title}_frame{count:03}.jpg', image)
            count = count + 1
        self.frame_dir_path = f'{path_out}'
        

# Usage example
if __name__ == '__main__':
    downloader = YouTubeDownloader(save_directory='./videos', resolution='360', format='mp4', framerate=None, audio=False)
    video_url = 'https://www.youtube.com/watch?v=iNBTSDryewM'
    downloader.download_video(video_url)
    # new
    downloader.extract_frames('./frames', [1, 3, 5])
    print(downloader.video_path)
    print(downloader.frame_dir_path)
    print(downloader.video_title)