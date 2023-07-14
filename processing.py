from events import *
from events import EventLog, Event
from download_video_ydl import YouTubeDownloader
from youtube_transcript_api import YouTubeTranscriptApi
from extracting_gpt import extracting_gpt
from detect_objects import ObjectDetector
import re
import os
import openai
from transformers import pipeline

openai.api_key = "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"


class Processing:
    """
    Main Class of the whole application. Contains all the necessary modules to generate the OCEL.
    """
    def __init__(self, yt_url) -> None:
        self.url = yt_url
        self.transcript = self.download_transcripts()
        self.timestamps = None
        self.objects_text = None
        self.objects_image = None
        self.actions = None
        self.event_log = EventLog()
        self.summarries = None
        self.durrations = None

    def download_transcripts(self):
        """
        Audio transcripts using the YouTubeTranscriptApi.
        """
        film_id = extract_youtube_id(self.url)
        transcript_list = YouTubeTranscriptApi.list_transcripts(film_id)
        transcript = transcript_list.find_transcript(['en'])
        return transcript.fetch()

    def gpt_processing(self):
        """
        Method that uses the openai API to receive and save the actions. The prompt are the video transcripts
        with the timestamps.
        """
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

    def object_recognition(self):
        """
        Method which downloads the video and saves the list of objects detected in the images.
        """
        ytd = YouTubeDownloader(save_directory='./videos', resolution='720',
                                       format='mp4', framerate=None, audio=False)
        ytd.download_video(self.url)
        ytd.extract_frames('./frames', self.timestamps)
        detector = ObjectDetector('./models/yolos-tiny', video_title=ytd.video_title)
        detector.initialize_model()
        self.objects_image = detector.detect_objects()

    def summary(self):
        """
        Unused method for generating summaries for each event in the log.
        """
        summarizer = pipeline("summarization", model="models/bart-large-cnn")
        self.summarries = []
        for dct in self.transcript:
            self.summarries.append(summarizer(dct['text'], max_length=5, min_length=1, do_sample=False))
    
    def generate_durations(self):
        """
        Get the duration of each event.
        """
        self.durrations = []
        for i in range(len(self.timestamps[:-1])):
            self.durrations.append(self.timestamps[i+1]-self.timestamps[i])
        self.durrations.append(0)
    
    def generate_OCEL(self, file_name='ocel_test8.csv'):
        """
        Method which executes all the steps to create the event log.
        """
        self.gpt_processing()
        self.object_recognition()
        # self.summary()
        self.generate_durations()
        length = len(self.actions)
        print(len(self.timestamps), len(self.actions), len(self.durrations), len(self.objects_text), len(self.objects_image))
        for i in range(length):
            event = Event(i, "{:.2f}".format(round(self.timestamps[i],2)), self.actions[i],
                          "{:.2f}".format(round(self.durrations[i],2)), None, " AND ".join(self.objects_text[i]), " AND ".join(self.objects_image[i]))
            self.event_log.add_event(event)
        self.event_log.save_OCEL_standard(file_name)


def extract_youtube_id(url):
    """
    Helper function for extracting the video id from the YouTube link.
    """
    pattern = r"(?:youtu.be\/|youtube.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))([^&\/]+)"
    match = re.search(pattern, url)

    if match:
        return match.group(1)
    else:
        return None


if __name__ == "__main__":
    obj = Processing('https://www.youtube.com/watch?v=Y5UqE_hpuSw')
    obj.generate_OCEL('ocel_example_2.csv')
    
    