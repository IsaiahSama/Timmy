import Utils, openai

from openai.error import Timeout, RateLimitError

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
        self.recorder = Utils.Recorder()
        self.text = ""
        self.role = "You're an assistant. Be helpful!"
        self.context = [self.role]
        self.model = 'chat'
        self.clear = "Clear history"
        self.setup()

    def setup(self):
        try:
            config = Utils.load_config()
            self.role = config["ROLES"][config["ROLE"]]
            self.context = [self.role]
            self.voice = config["VOICE"]
            self.model = config["MODELS"][config["MODEL"]]
        except FileNotFoundError:
            print("Could not find config file `config.yaml`")
        except KeyError as e:
            print("One of the fields I was looking for do not exist. Everything else has been set.\n", str(e))

        self.model = Utils.model_check()


    def listen(self):
        if self.recorder.recording: return False
        self.recorder.recording = True
        frames = self.recorder.record()
        if not [f.strip() for f in frames]: return
        self.recorder.save_frames(frames)
        self.transcribe()
        self.context.append(self.text)
        self.prompt_api()

    def stop_listening(self):
        self.recorder.recording = False
        print("Processing")

    def transcribe(self):
        self.text = Utils.transcribe()
        if not self.text: return False
        if self.clear.lower() in self.text.lower(): 
            self.clear_context()
            self.text = self.text.lower().replace(self.clear, "")

        Utils.tts("I heard: ", self.text)
        if len(self.context) >= 21: self.clear_context()

    def prompt_api(self):
        response = self.prompt()
        if not response: return False
        # Step 8, Read out the response.
        Utils.Utils.tts(response)

    def clear_context(self):
        self.context.clear()
        self.context = [self.role]

    def prompt_chat(self):
        # Prompts the gpt-3.5-turbo model. Not recommended for slow networks.
        content = Utils.contextify(self.context)
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

    def prompt_text(self):
        """Prompts the text-davinci-003 model for a response given the recorded text"""
        content = Utils.contextify(self.context, True)
        response = openai.Completion.create(
            model="text-davinci-003", 
            prompt=content, 
            temperature=1,
            request_timeout=40,
            max_tokens=1000
            )
        return response["choices"][0]['text'].replace("ANSWER:", "")

    def prompt(self) -> str:
        model = self.prompt_chat if self.model == "chat" else self.prompt_text

        try:
            return model()        
        except (RateLimitError):
            Utils.tts("My brain seems to be occupied doing other things. Very busy I am. Sorry. Try again later.")
        except (Timeout):
            Utils.tts("The wifi you're currently connected to is not good enough and the requests are taking too long.")
        finally:
            return ""

