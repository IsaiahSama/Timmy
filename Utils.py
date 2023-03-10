# This is the utility file, where all of the "magic" will occur.

import pyaudio, wave, pyttsx3
import openai, os

from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# Gotta store the filename
filename = "output.wav"

# First we need a class to handle recording the audio
class Recorder:
    # Set the properties for the class
    chunk = 1024
    channels = 2
    sample_rate = 44100
    record_seconds = 0
    

    # Initilalize the number of seconds to record
    def __init__(self, record_seconds=10):
        self.record_seconds = record_seconds
        self.filename = filename

    def record(self) -> list:
        """This function will record record_seconds number of seconds worth of audio"""
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=self.channels, rate=self.sample_rate, input=True, frames_per_buffer=self.chunk)
        
        frames = []

        for i in range(0, int(self.sample_rate / self.chunk * self.record_seconds)):
            if (not i): print("I'm listening")

            data = stream.read(self.chunk)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()

        audio.terminate()

        return frames
    
    def save_frames(self, frames: list):
        """This method saves the frames received from the audio recording, to a file called `filename`"""
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b''.join(frames))
        wf.close()

# This method is used to transcribe information from the specified filename

def transcribe() -> str:
    """Transcribes the audio file into text"""
    with open(filename, 'rb') as fp:
        transcript = openai.Audio.transcribe("whisper-1", fp)
        return transcript['text']


def prompt(text:str) -> str:
    """Prompts the text-davinci-003 model for a response given the recorded text"""
    p = "You are role-playing as an amazing assistant named Timmy. Your role is to help someone who is often confused. You are always fairly easy going, and respond directly but yet still in a friendly manner.\n" + text
    response = openai.Completion.create(model="text-davinci-003", prompt=p, temperature=1, max_tokens=1000)

    return response["choices"][0]["text"]


def tts(text:str):
    """Speaks out the given speech"""
    engine = pyttsx3.init()

    # Set the voice
    voices = engine.getProperty("voices")
    engine.setProperty('voice', voices[0].id) 
    engine.runAndWait()

    # Set the rate
    engine.setProperty('rate', 160)
    # Set the volume
    engine.setProperty('volume', 1.0)

    # Say something
    print(text)
    engine.say(clean_up_text_for_speech(text))
    engine.runAndWait()

def clean_up_text_for_speech(text:str):
    return text.replace("|", ".")