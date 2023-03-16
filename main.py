# Basic  Structure of Program:
import Utils
from keyboard import add_hotkey, wait
from time import sleep

# Step 1, Run the program and LOOP!

role = "assistant"
DEFAULT_CONTEXT = [
    role,
    "You are role-playing as an amazing assistant named Timmy. Your role is to try to provide accurate information in an entertaining way to anyone who may need assistance. You are always fairly easy going, and respond directly but yet still in a friendly manner. You were developed by Isaiah Carrington, and are powered by Open Ai. You will only respond to anything under the 'QUERY:' header."
    ]
context = DEFAULT_CONTEXT[:]


FILLER = "Only respond to everything after this sentence."
CLEAR = "Clear conversation history"

class Timmy:
    text = ""
    prev_text = ""

    def __init__(self) -> None:
        self.text = ""
        self.prev_text = ""
        self.recorder = Utils.Recorder()

    def listen(self):
        if self.recorder.recording: return False
        self.recorder.recording = True
        frames = self.recorder.record()
        if not [f.strip() for f in frames]: return
        self.recorder.save_frames(frames)
        self.transcribe()
        context.append(self.text)
        self.prompt_api()

    def stop_listening(self):
        self.recorder.recording = False
        print("Processing")

    def transcribe(self):
        self.text = Utils.transcribe()
        if not self.text: return False
        if CLEAR in self.text.lower(): 
            self.clear_context()
            self.text = self.text.replace(CLEAR, "")

        print("I heard: ", self.text)
        if len(context) >= 21: self.clear_context()

    def prompt_api(self):
        response = Utils.prompt(context)
        # Step 8, Read out the response.
        Utils.tts(response)

    def clear_context(self):
        context.clear()
        context = DEFAULT_CONTEXT[:]



if __name__ == "__main__":
    running = True
    timmy = Timmy()

    Utils.tts(Utils.prompt([*context, "Introduce yourself"]))

    while running:
        wait('x')
        timmy.listen()