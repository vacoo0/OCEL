# Creating object-centric event logs from instructional/tutorial/how to videos

A brief description of your project goes here.

## Table of Contents

- [Project Description](#project-description)
- [Installation](#installation)
- [Usage](#usage)
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
git clone https://huggingface.co/hustvl/yolos-tiny
```

To make use of GPT-3.5, follow these steps:

1. Open the `processing.py` file in your project.
2. Locate line 13 and find the code snippet `openai.api_key = ""`.
3. Replace the empty string `""` with your own API key within the quotation marks.

## Usage

Explain how to use your project. Provide examples and code snippets if necessary. Include any configuration options or environment variables that need to be set.

## Features

List the key features of your project here. Highlight the main functionalities or components that make your project stand out.

## Contributing

Explain how others can contribute to your project. Provide guidelines for submitting bug reports, feature requests, or pull requests. Include a code of conduct if applicable.

## License

Specify the license under which your project is distributed. Include any relevant copyright or attribution notices.

## Acknowledgements

If your project relies on or was inspired by other works, mention them here. Provide links or references to any external resources that were helpful in creating your project.

## Contact

Provide your contact information or links to your social media profiles. Encourage users to reach out with questions, feedback, or suggestions.
