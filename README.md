# Creating object-centric event logs from instructional/tutorial/how to videos

A brief description of your project goes here.

## Table of Contents

- [Project Description](#project-description)
- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Example Results](#example-results)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Project Description

The aim of this project is to develop a system that can automatically generate object-centric event logs from instructional, tutorial, or how-to videos. In today's digital age, there is an abundance of video content available online, providing step-by-step instructions for various tasks and activities. However, it can be challenging to extract structured data from these videos to create event logs that capture the sequence of actions performed on specific objects.

By leveraging computer vision techniques and natural language processing, this project aims to bridge the gap between unstructured video content and structured event logs. The system will analyze the video frames to detect and track objects of interest, such as tools, equipment, or items being manipulated by the instructor in the video. It will also process the accompanying transcriptions to extract relevant textual instructions or annotations.

The extracted information will be used to construct object-centric event logs, which will capture the temporal order of actions performed on each object. These event logs can be invaluable for various applications, including process automation, knowledge extraction, or interactive tutorials.

## Overview

Below is a simplified diagram of how our project works.

<div align="center">
  <img src="simple_diagram.png" alt="Project Architecture" width="400px" />
</div>

As you can see above, the link to the video on youtube is selected first. Then the transcript is downloaded with timestamps, which are fed to gpt-3.5, which combines fragments of the transcript and returns new timestamps (several timestamps may have been combined) and detected objects and actions. In the next step, the entire film is downloaded, from which the appropriate frames are selected, using previously corrected timestamps. Objects are detected on each frame. Based on all the information collected in this way, an object-centric event log is created.

## Installation

To successfully run the code, ensure that you have installed all the libraries listed in the `requirements.txt` file. You can do this by running the following command:

```bash
pip install -r requirements.txt
```

The next step is to download the *yolos-tiny* model to the `models` folder, this can be done with the following command:

```bash
git lfs clone https://huggingface.co/hustvl/yolos-tiny
```

To make use of GPT-3.5, follow these steps:

1. Open the `processing.py` file in your project.
2. Locate line 13 and find the code snippet `openai.api_key = ""`.
3. Replace the empty string `""` with your own API key within the quotation marks.

## Usage

To generate an OCEL (Object-centric event logs), follow these steps:

1. Create a `Processing` class object and provide a link to a YouTube video as an argument.
2. Call the `.generate_OCEL()` method on the processing class object.
   - Optionally, specify the name of the file where the eventlog is to be saved.
3. The generated event log can be found in the `logs/events` folder.
4. The generated objects can be found in the `logs/objects` folder.

Example (from `processing.py`):
```python
if __name__ == "__main__":
    obj = Processing('https://www.youtube.com/watch?v=Y5UqE_hpuSw')
    obj.generate_OCEL('ocel_example.csv')
```
It is important that the link does not contain 'shorts'. 

## Example Results

Example for [https://www.youtube.com/watch?v=Y5UqE_hpuSw](https://www.youtube.com/watch?v=Y5UqE_hpuSw).

| ocel:eid | ocel:activity | ocel:timestamp | duration | ocel:type:ocel:type:items_text | ocel:type:ocel:type:items_image |
|----------|----------|----------|----------|----------|----------|
| 0  | Making soup dumplings    | 0.08     | 8.00   | ['ingredients']   | ['person', 'dining table', 'cup']   |
| 1  | Adding foie gras         | 8.08  | 3.84 | ['two tablespoons foie gras']  | ['person', 'cup']  |
| 2  | Boiling Stock            | 11.92  | 6.56 | ['chicken stock']  | ['person', 'cup'] |
| 3  | Cooling  | 18.48         | 1.68  | ['gelatin mixture']  | ['person', 'cup'] |
| 4  | Preparing filling        | 20.16  | 13.04  | ['one minced green onion', 'one tablespoon of rice wine', 'one and a half teaspoon of sesame oil', 'teaspoon of soy sauce', 'one and a half teaspoons of sugar', 'about a half a pound of ground pork', 'a little salt and a little pepper', 'gelatin mixture']  | ['person', 'bowl']  |
| 5  | Building dumplings       | 33.20  | 10.80  | ['filling']  |   |
| 6  | Steaming dumplings       | 44.00  | 2.24  | ['bamboo steamer', 'aluminum foil ball plate', 'dumplings']  | ['person']  |
| 7  | Making sauce             | 46.24  | 8.32 | ['balsamic vinegar', 'soy sauce', 'julienned ginger']  | ['person'] |
| 8  | Eating                   | 54.56  | 0.00  | ['soup dumplings']  | ['person', 'spoon', 'bowl']  |

## Files description - Step by step
# 1. processing.py
   
 - Class Definition - Processing: The main class is defined, which represents the processing of a YouTube video. It contains methods for downloading transcripts, 
   processing with GPT (Generative Pre-trained Transformer), object recognition, summarization, generating durations, and creating an OCEL file.
 - Initialization: The Processing class is initialized with a YouTube video URL. It sets up various instance variables and creates an empty EventLog object.
 - Downloading Transcripts: The download_transcripts method is called to download the video's transcripts using the YouTubeTranscriptApi library.
 - GPT Processing: The gpt_processing method is called, which utilizes the OpenAI GPT-3.5 model to process the transcripts and generate objects, actions, and start times 
   for each step.
 - Object Recognition: The object_recognition method is called to download the YouTube video and extract frames at the specified timestamps. It then uses an object 
   detection model to identify objects in the extracted frames.
 - Summary Generation (Commented Out): There is a commented-out section for generating summaries of the video using the bart-large-cnn model. It is currently disabled in 
   the code.
 - Duration Calculation: The generate_durations method calculates the durations between each timestamp to determine the time duration for each step.
 - Generating OCEL: The generate_OCEL method is called to generate an OCEL file. It combines the processed data from GPT, object recognition, durations, and other         
   information to create Event objects. These objects are added to the EventLog object, which is then saved as an OCEL file.
 - Helper Function - extract_youtube_id: This function extracts the YouTube video ID from a given URL using regular expressions.
 - Main Execution: An instance of the Processing class is created, and the generate_OCEL method is called with a YouTube video URL. The resulting OCEL file is saved as        'ocel_example_2.csv'.
   
# 2. events.py

 This code defines two classes: Event and EventLog, and provides methods for creating an OCEL (Object-Action-Start-End Log) file from an EventLog object.
 - Event Class:
   - The Event class represents an event in the log and has attributes such as event_id, timestamp, activity, duration, summary, items_text, and items_image.
   - It provides an initializer method to set the attribute values.
 - EventLog Class:
   - The EventLog class represents a collection of events.
   - It maintains a list of Event objects in the events attribute.
   - The class provides methods to add and remove events from the log, retrieve all events, create a pandas DataFrame from the log data, and convert the log to an OCEL 
    format.
   - add_event(event: Event): Adds an event to the log by appending it to the events list.
   - remove_event(event_id): Removes an event from the log based on its event_id.
   - get_events(): Returns the list of events in the log.
   - create_dataframe(): Creates a pandas DataFrame from the log data, where each column corresponds to an attribute of an event.
   - create_ocel(): Converts the log to the OCEL format using the pm4py.convert.convert_log_to_ocel function. The log data is converted to a DataFrame and passed as an          argument along with other OCEL-related parameters.
   - save_OCEL_standard(file_name='ocel_test.csv'): Saves the OCEL log to CSV files (ocel_test.csv and ocel_test_cd.csv).
 - pm4py.convert.convert_log_to_ocel:
   - This is a function provided by the pm4py library.
   - It converts a log (EventLog, EventStream, or DataFrame) to the OCEL format.
   - It takes parameters such as log, activity_column, timestamp_column, object_types, obj_separator, and additional_event_attributes to specify the columns and attributes      in the OCEL log.
 - Main Execution (Commented Out):
   - There is a commented-out section that demonstrates the usage of the Event and EventLog classes.
   - An Event object is created, added to an EventLog object, and converted to OCEL format.
   - The OCEL log is then saved to CSV files.
# 3. download_video_ydl.py
5. extracting_gpt.py
6. detect_objects.py

## Features

List the key features of your project here. Highlight the main functionalities or components that make your project stand out.

## Contributing

Explain how others can contribute to your project. Provide guidelines for submitting bug reports, feature requests, or pull requests. Include a code of conduct if applicable.

## License

Specify the license under which your project is distributed. Include any relevant copyright or attribution notices.

## Acknowledgements

Below are some useful links.
1. [https://openai.com/](https://openai.com/)
2. [https://huggingface.co/hustvl/yolos-tiny](https://huggingface.co/hustvl/yolos-tiny)
3. [https://ocel-standard.org/](https://ocel-standard.org/)

## Contact

Provide your contact information or links to your social media profiles. Encourage users to reach out with questions, feedback, or suggestions.
