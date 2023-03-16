# This is the utility file, where all of the "magic" will occur.

import pyaudio, wave, pyttsx3
import openai, os

from openai.error import Timeout, RateLimitError

from dotenv import load_dotenv
from keyboard import is_pressed

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
        print("I'm listening")

        # for i in range(0, int(self.sample_rate / self.chunk * self.record_seconds)):
        while not (is_pressed("c")):
            data = stream.read(self.chunk)
            frames.append(data)
        
        print("Thinking...")
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
    print("Thinking about how to respond...")
    with open(filename, 'rb') as fp:
        transcript = openai.Audio.transcribe("whisper-1", fp)
        return transcript['text'].strip()


def prompt(context:list) -> str:
    """Prompts the text-davinci-003 model for a response given the recorded text"""
    content = "CONTEXT:\n"+ "\n".join(context[1:-1]) + "\nQUERY:\n" + context[-1]
    print(content)
    try:
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role":context[0],
                    "content":content,
                }], 
                temperature=1,
                request_timeout=10

            )
    except (Timeout, RateLimitError):
        try:
            print("The ChatCompletion model is occupied. Trying Completion model.")
            response = openai.Completion.create(
                model="text-davinci-003", 
                prompt=content, 
                temperature=1,
                request_timeout=10
                )
        except (RateLimitError):
            tts("My brain seems to be occupied doing other things. Very busy I am. Sorry. Try again later.")
        except (Timeout):
            tts("The wifi you're currently connected to is not good enough and the requests are taking too long.")

    return response["choices"][0]['text'].replace("RESPONSE:", "")


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

def clean_up_text_for_speech(text:str):
    return text.replace("|", ".").replace("-", "")