# Basic  Structure of Program:
import Utils

# Step 1, Run the program

# Step 2, record 10 seconds worth of audio
rc = Utils.Recorder()

frames = rc.record()

# Step 3, save the audio to a file
rc.save_frames(frames)

# Step 4, transcribe the audio from the file to text
text = Utils.transcribe()

# Step 5, pass the text to the AI

# Step 6, let the magic happen

# Step 7, save the response

# Step 8, Read out the response.