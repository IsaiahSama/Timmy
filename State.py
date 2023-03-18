from threading import Thread
from os import listdir, get_terminal_size
from time import sleep

import pygame

class State:
    state = ""
    path = ""

    def __init__(self, state:str, path:str):
        self.state = state
        self.path=path
        self.setup()

    def setup(self):
        t = Thread(target=self.run, daemon=True)
        t.start()

    def get_path(self):
        return self.path + self.state
    
    def change_state(self, state:str):
        self.state = state

    def run(self):
        cur_path = None

        pygame.init()
        window = pygame.display.set_mode((320, 320))

        frame_index = 0
        animation_speed = 300 # in milliseconds
        animation_timer = pygame.time.get_ticks()

        while True:
            window.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    
            if cur_path == self.get_path(): 
                sleep(0)
            else:
                cur_path = self.get_path()
                files = listdir(cur_path)
                frames = [pygame.image.load(cur_path+file) for file in files]

            # draw the current frame
            window.blit(frames[frame_index], (0, 0))

            # update the frame index based on the animation speed
            if pygame.time.get_ticks() - animation_timer > animation_speed:
                frame_index = (frame_index + 1) % len(frames)
                animation_timer = pygame.time.get_ticks()

            # update the display
            pygame.display.update()

        #     for file in files:
        #         with Image.open(cur_path+file) as image:
        #             width, height = image.size
        #             image = image.resize((width*2, height*2), resample=Image.BICUBIC)
        #             # Show the upsized image
        #             image.show()