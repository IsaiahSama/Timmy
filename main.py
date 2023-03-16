# Basic  Structure of Program:
from timmy import Timmy
from keyboard import wait

if __name__ == "__main__":
    running = True
    timmy = Timmy()

    # Utils.tts(Utils.prompt([*context, "Introduce yourself"]))

    while running:
        wait('x')
        timmy.listen()