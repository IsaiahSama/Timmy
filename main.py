# Basic  Structure of Program:
import Utils

# Step 1, Run the program and LOOP!

text = ""

r = Utils.prompt("Introduce yourself.")
Utils.tts(r)

while ("goodbye" not in text.lower()):
    # Step 2, record x seconds worth of audio
    rc = Utils.Recorder(5)

    frames = rc.record()

    # # Step 3, save the audio to a file
    rc.save_frames(frames)

    # Step 4, transcribe the audio from the file to text
    text = Utils.transcribe()
    print("I heard: ", text)

    # Step 5, pass the text to the AI if there is text
    if not text: continue
    # Step 6, let the magic happen
    # Step 7, save the response
    response = Utils.prompt(text)

    # Step 8, Read out the response.

    Utils.tts(response)