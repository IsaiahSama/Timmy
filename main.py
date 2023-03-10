# Basic  Structure of Program:
import Utils

# Step 1, Run the program and LOOP!

text = ""
prev_text = ""

r = Utils.prompt("Introduce yourself.")
Utils.tts(r)

filler = "<Everything before this is just for context of past conversations. So don't respond to it>"

while ("goodbye" not in text.lower()):
    # Step 2, record x seconds worth of audio
    prev_text = prev_text.replace(filler, "")
    rc = Utils.Recorder(5)

    frames = rc.record()

    # Step 3, save the audio to a file
    rc.save_frames(frames)

    # Step 4, transcribe the audio from the file to text
    text = Utils.transcribe()
    if not text or "timmy" not in text.lower(): continue
    print("I heard: ", text)
    prev_text += ". "+ filler + text
    if len(prev_text) >= 1500: prev_text = ""

    # Step 5, pass the text to the AI if there is text
    # Step 6, let the magic happen
    # Step 7, save the response
    response = Utils.prompt(prev_text)

    # Step 8, Read out the response.

    Utils.tts(response)