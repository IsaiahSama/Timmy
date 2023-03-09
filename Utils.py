# This is the utility file, where all of the "magic" will occur.

import pyaudio, wave

# First we need a class to handle recording the audio

class Recorder:
    chunk = 1024
    channels = 2
    sample_rate = 44100
    record_seconds = 10
    filename = "output.wav"

    def __init__(self, record_seconds=10):
        self.record_seconds = record_seconds

    def record(self) -> list:
        audio = pyaudio.PyAudio()
        with audio.open(format=pyaudio.paInt16, channels=self.channels, rate=self.sample_rate, inut=True, frames_per_buffer=self.chunk) as stream:
            print("I'm listening")

            frames = []

            for _ in range(0, int(self.sample_rate / self.chunk * self.record_seconds)):
                data = stream.read(self.chunk)
                frames.append(data)
            
            stream.stop_stream()

        audio.terminate()

        return frames
    
    def save_frames(self, frames: list):
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b''.join(frames))
        wf.close()
