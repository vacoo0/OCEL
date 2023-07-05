import yt_dlp as youtube_dl

class YouTubeDownloader:
    def __init__(self, save_directory, resolution='360', format='mp4', framerate=None):
        self.save_directory = save_directory
        self.resolution = resolution
        self.format = format
        self.framerate = framerate
    
    def download_video(self, video_url):
        ydl_opts = {
            'format': self._build_format_string(),
            'outtmpl': self._build_output_template(),
        }
        
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    
    def _build_format_string(self):
        format_string = f'bestvideo[height<={self.resolution}][ext={self.format}]+bestaudio[ext={self.format}]/best[height<={self.resolution}][ext={self.format}]'
        
        if self.framerate:
            format_string += f'/best[height<={self.resolution}][ext={self.format}][fps={self.framerate}]'
        
        return format_string
    
    def _build_output_template(self):
        return f'{self.save_directory}/%(title)s.%(ext)s'

# Usage example
if __name__ == '__main__':
    downloader = YouTubeDownloader(save_directory='./videos', resolution='360', format='mp4', framerate=None)
    video_url = 'https://www.youtube.com/watch?v=iNBTSDryewM'
    downloader.download_video(video_url)