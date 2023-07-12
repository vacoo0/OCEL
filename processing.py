from events import *
from events import EventLog, Event
from cut_vid import *
from download_video_ydl import *
from youtube_transcript_api import YouTubeTranscriptApi
from extracting_gpt import extracting_gpt
import re
import os
import openai

openai.api_key = "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"


class Processing:
    def __init__(self, yt_url) -> None:
        self.url = yt_url
        self.transcript = self.download_transcripts()
        self.timestamps = None
        self.objects_text = None
        self.actions = None
        self.event_log = EventLog()

    def download_transcripts(self):
        film_id = extract_youtube_id(self.url)
        transcript_list = YouTubeTranscriptApi.list_transcripts(film_id)
        transcript = transcript_list.find_transcript(['en'])
        return transcript.fetch()

    def gpt_processing(self):
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt = """{}, based on timestamps and text give an objects, action and start for every step in format: 
                Step i: ; Action: ; Objects: ,... ; Start: """.format(self.transcript),
        temperature=1,
        max_tokens=2048,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )
        text = response["choices"][0]["text"]
        print(text)
        objects, actions, start = extracting_gpt(text)
        self.timestamps = start 
        self.objects_text = objects 
        self.actions = actions 

    def generate_OCEL(self):
        self.gpt_processing()
        length = len(self.actions)
        for i in range(length):
            event = Event(i, "{:.2f}".format(round(self.timestamps[i],2)), self.actions[i], None, None, " AND ".join(self.objects_text[i]), None)
            self.event_log.add_event(event)
        self.event_log.save_OCEL_standard(file_name='ocel_test3.csv')

def extract_youtube_id(url):
    pattern = r"(?:youtu.be\/|youtube.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))([^&\/]+)"
    match = re.search(pattern, url)

    if match:
        return match.group(1)
    else:
        return None
















if __name__ == "__main__":
    obj = Processing('https://www.youtube.com/watch?v=NbRDzNx1I5A')
    obj.generate_OCEL()
    
    