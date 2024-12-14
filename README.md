# Timmy

Timmy is designed to be an avatar assistant, supporting Speech Recognition, Text to Speech, LLM capabilities, and of course, an avatar.

## Getting started

You can clone the repository using `git clone https://github.com/IsaiahSama/Timmy` to your device! You'll also need Python 3.10 or higher for the program to run properly.
You can then install the libraries by running `pip install -r requirements.txt`. I highly recommend modifying the `config.yaml` file, primarily the ROLES section, and changing the prompt for the `GENERAL` one (or making your own and updating the `ROLE` entry to match). With this, the last thing you'll need is an API key for either GEMINI, or Open AI, and placing that key in a `.env` file based off of the `.env.sample` file. Be sure to update the `MODEL` entry of the `config.yaml` file to reflect the model you wish to use.

From here, you can run `python main.py` or `python3 main.py` to get started. Have fun!

## Installing other voices
https://puneet166.medium.com/how-to-added-more-speakers-and-voices-in-pyttsx3-offline-text-to-speech-812c83d14c13

## My Medium Post
I recently created a post on Medium that goes into my thought process and implementation when creating this, so feel free to give that a read and some claps as well if you enjoy 😄. [Timmy The AI Assistant](https://github.com/IsaiahSama/Timmy).
