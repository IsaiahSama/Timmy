# This is the utility file, where all of the "magic" will occur.

import pyaudio, wave, pyttsx3
import openai, os

from dotenv import load_dotenv
from keyboard import is_pressed
from speedtest import Speedtest

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

testing = True

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
    recording = False
    

    # Initilalize the number of seconds to record
    def __init__(self, record_seconds=10):
        self.record_seconds = record_seconds
        self.filename = filename

    def record(self) -> list:
        """This function will record record_seconds number of seconds worth of audio"""
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=self.channels, rate=self.sample_rate, input=True, frames_per_buffer=self.chunk)
        
        frames = []
        tts("I'm listening")

        # for i in range(0, int(self.sample_rate / self.chunk * self.record_seconds)):
        counter = 0
        while not (is_pressed("c")):
            if not( counter % 10): print('.', end='', flush=True)
            counter += 1
            data = stream.read(self.chunk)
            frames.append(data)
        
        print("")
        print("Attempting to understand what you said...")
        self.recording = False
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
        return transcript['text'].strip()

def tts(text:str):
    """Speaks out the given speech"""
    engine = pyttsx3.init()

    # Set the voice
    voices = engine.getProperty("voices")
    engine.setProperty('voice', voices[1].id) 
    engine.runAndWait()

    # Set the rate
    engine.setProperty('rate', 170)
    # Set the volume
    engine.setProperty('volume', 1.0)

    # Say something
    print(text)
    engine.say(clean_up_text_for_speech(text))
    engine.runAndWait()
    print()

def clean_up_text_for_speech(text:str):
    return text.replace("|", ".").replace("-", "")

def contextify(ctx:list, include_role:bool=False):
    return "CONTEXT:\n"+ "\n".join(ctx[1 if include_role else 0:-1]) + "\nQUERY:\n" + ctx[-1]

def load_config() -> dict:
    with open("config.yaml") as fp:
        return load(fp, Loader)["CONFIG"]
    
def model_check(prev:str):
    if prev == "text": return prev
    tts("Testing Network speed")
    st = Speedtest()
    if st.download() / (1024 * 1024) < 30 and prev != "text":
        tts("Your network speed is limited. Switching to a different model!")
        return "text"
    return 'chat'