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
