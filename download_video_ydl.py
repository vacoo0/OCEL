import yt_dlp as youtube_dl

ydl_opts = {
    'format': 'bestvideo[height<=720][ext=mp4]'
}
ydl = youtube_dl.YoutubeDL(ydl_opts)
ydl.download(['https://www.youtube.com/watch?v=iNBTSDryewM'])
