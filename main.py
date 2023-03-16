# Basic  Structure of Program:
from timmy import Timmy
from keyboard import wait

if __name__ == "__main__":
    running = True
    print("Setting up")
    timmy = Timmy()

    # Utils.tts(Utils.prompt([*context, "Introduce yourself"]))
    print("Ready!")
    while running:
        wait('x')
        timmy.listen()