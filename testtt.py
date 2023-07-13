import wave
import json
from vosk import Model, KaldiRecognizer, SetLogLevel
import Word as custom_Word

''' mp4 to wav'''
# video_file = 'C:\\Users\\Lenovo\\Desktop\\studia\\dw-project\\video\\Cosmopolitan cocktail recipe.mp4'
#
# # Extract audio from the MP4 file
# clip = mp.VideoFileClip(video_file)
# audio = clip.audio
# audio_file = 'C:\\Users\\Lenovo\\Desktop\\studia\\dw-project\\speech\\Cosmopolitan cocktail recipe.wav'
# audio.write_audiofile(audio_file)


model_path = "C:\\Users\\Lenovo\\Desktop\\studia\\dw-project\\models\\vosk-model-pt-fb-v0.1.1-pruned"
audio_filename = "C:\\Users\\Lenovo\\Desktop\\studia\\dw-project\\speech\\Cosmopolitan cocktail recipe.wav"

model = Model(model_path)
wf = wave.open(audio_filename, "rb")
rec = KaldiRecognizer(model, wf.getframerate())
rec.SetWords(True)

# get the list of JSON dictionaries
results = []
# recognize speech using vosk model
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        part_result = json.loads(rec.Result())
        results.append(part_result)
part_result = json.loads(rec.FinalResult())
results.append(part_result)

# convert list of JSON dictionaries to list of 'Word' objects
list_of_Words = []
for sentence in results:
    if len(sentence) == 1:
        # sometimes there are bugs in recognition
        # and it returns an empty dictionary
        # {'text': ''}
        continue
    for obj in sentence['result']:
        w = custom_Word.Word(obj)  # create custom Word object
        list_of_Words.append(w)  # and add it to list

wf.close()  # close audiofile

# output to the screen
for word in list_of_Words:
    print(word.to_string())