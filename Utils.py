# This is the utility file, where all of the "magic" will occur.

import pyaudio, wave
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
    def __init__(self, record_seconds=5):
        self.record_seconds = record_seconds
        self.filename = filename

    def record(self) -> list:
        """This function will record record_seconds number of seconds worth of audio"""
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=self.channels, rate=self.sample_rate, input=True, frames_per_buffer=self.chunk)
        print("I'm listening")

        frames = []

        for _ in range(0, int(self.sample_rate / self.chunk * self.record_seconds)):
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

def transcribe():
    with open(filename, 'rb') as fp:
        transcript = openai.Audio.transcribe("whisper-1", fp)
        return transcript['text']
