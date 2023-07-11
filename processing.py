from events import *
from events import EventLog
from cut_vid import *
from download_video_ydl import *
from youtube_transcript_api import YouTubeTranscriptApi
import re
import os
import openai

openai.api_key = "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"


class Processing:
    def __init__(self, yt_url) -> None:
        self.url = yt_url
        self.transcript = self.download_transcripts()
        self.timestamps = None
        self.event_log = EventLog()

    def download_transcripts(self):
        film_id = extract_youtube_id(self.url)
        transcript_list = YouTubeTranscriptApi.list_transcripts(film_id)
        transcript = transcript_list.find_transcript(['en'])
        return transcript.fetch()

    def gpt_processing(self):
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt = """{}, based on timestamps text give an object, action and start for every step""".format(self.transcript),
        temperature=1,
        max_tokens=512,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )
        text = response["choices"][0]["text"]
        self.timestamps = re.findall(r"Start - (\d+)", text)
        self.timestamps = [int(ts) for ts in self.timestamps]
        # print("Rounded Timestamps:", timestamps)

def extract_youtube_id(url):
    pattern = r"(?:youtu.be\/|youtube.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))([^&\/]+)"
    match = re.search(pattern, url)

    if match:
        return match.group(1)
    else:
        return None
















if __name__ == "__main__":
    obj = Processing('https://www.youtube.com/watch?v=iNBTSDryewM')
    print(obj.transcript)
    
    