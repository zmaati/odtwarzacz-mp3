import loadsound
import pygame
from pause import pause_var


def zagraj():
    global pause_var
    if pause_var == 1:
        pygame.mixer.music.unpause()
        pause_var = 0
    elif pause_var == 0:
        pygame.mixer.music.play(loops=1)
        pause_var = 0
