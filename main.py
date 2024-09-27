# Basic  Structure of Program:
from timmy import Timmy
import pygame

if __name__ == "__main__":
    timmy = Timmy()

    try:
        while True:
            timmy.listen()
    except KeyboardInterrupt:
        pygame.quit()
        quit()