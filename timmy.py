import utils, state

import openai
from openai import Timeout, RateLimitError

from keyboard import wait

DISCLAIMER = "You will only respond to anything under the 'QUERY:' header."

class Timmy:
    text = ""
    recorder = None
    role = ""
    context = []
    voice = 0
    model = ""
    clear = ""

    def __init__(self) -> None:
        print("Setting up")
        self.recorder = utils.Recorder()
        self.text = ""
        self.role = "You're an assistant. Be helpful!"
        self.context = [self.role]
        self.model = 'chat'
        self.clear = "Clear history"
        self.record_key = 'x'
        self.process_key = 'c'
        self.state = "sleeping"
        self.states = {
            "SLEEPING": "Sleeping/",
            "TALKING": "Talking/",
            "THINKING": "Thinking/", 
            "LISTENING": "Listening/"
        }
        self.path = "./States/"
        self.setup()
        print("Ready!")


    def setup(self):
        try:
            config = utils.load_config()
            self.role = config["ROLES"][config["ROLE"]]
            self.context = [self.role]
            self.voice = config["VOICE"]
            self.model = config["MODELS"][config["MODEL"]]
            self.record_key = config["RECORDKEY"]
            self.process_key = config["PROCESSKEY"]
            self.state = config["STATES"][config["STATE"]]
            self.states = config["STATES"]
            self.path = config["STATES"]["PATH"]
        except FileNotFoundError:
            print("Could not find config file `config.yaml`")
        except KeyError as e:
            print("One of the fields I was looking for do not exist. Everything else has been set.\n", str(e))

        self.model = utils.model_check(self.model)
        self.state_manager = state.State(self.state, self.path)
        self.speak("I'm ready now. Press " + self.record_key + " for me to listen, and press "+ self.process_key + " when you're finished speaking.")


    def listen(self):
        wait('x')
        if self.recorder.recording: return False
        self.recorder.recording = True
        self.state_manager.change_state(self.states["LISTENING"])
        frames = self.recorder.record()
        if not [f.strip() for f in frames]: return
        self.state_manager.change_state(self.states["THINKING"])
        self.recorder.save_frames(frames)
        if self.transcribe():
            self.context.append(self.text)
            self.speak("I heard: " + self.text)
            self.prompt_api()

    def stop_listening(self):
        self.recorder.recording = False
        print("Processing")

    def transcribe(self):
        self.text = utils.transcribe()
        if not self.text.strip(): 
            print("No actual text")
            self.speak("I didn't hear anything...")
            return False
        if self.clear.lower() in self.text.lower(): 
            self.clear_context()
            self.text = self.text.lower().replace(self.clear, "")

        if len(self.context) >= 21: self.clear_context()
        return True

    def prompt_api(self):
        self.speak("Thinking...")
        self.state_manager.change_state(self.states["WAKING"])
        response = self.prompt()
        if not response: return False
        # Step 8, Read out the response.

        self.speak(response)
        self.clear_context()

    def speak(self, text:str):
        self.state_manager.change_state(self.states["TALKING"])
        utils.tts(text)
        self.state_manager.change_state(self.states["SLEEPING"])


    def clear_context(self):
        self.context.clear()
        self.context = [self.role]

    def prompt_chat(self) ->str:
        # Prompts the gpt-3.5-turbo model. Not recommended for slow networks.
        content = utils.contextify(self.context)
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role":'system', "content":self.context[0]},
                    {"role":'user', "content":content},
                    ], 
                temperature=1,
                request_timeout=30
            )
        return response["choices"][0]["message"]['content'].replace("RESPONSE:", "")

    def prompt_text(self) ->str:
        """Prompts the text-davinci-003 model for a response given the recorded text"""
        content = utils.contextify(self.context, True)
        response = openai.Completion.create(
            model="text-davinci-003", 
            prompt=content, 
            temperature=1,
            request_timeout=40,
            max_tokens=1000
            )
        return response["choices"][0]['text'].replace("RESPONSE:", "")

    def prompt(self) -> str:
        model = self.prompt_chat if self.model == "chat" else self.prompt_text
        try:
            return model()     
        except (RateLimitError):
            self.speak("My brain seems to be occupied doing other things. Very busy I am. Sorry. Try again later.")
            return ""
        except (Timeout):
            self.speak("The wifi you're currently connected to is not good enough and the requests are taking too long.")
            return ""

