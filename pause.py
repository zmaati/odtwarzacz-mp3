import loadsound
import pygame


def pauza():
    global pause_var
    pygame.mixer.music.pause()
    pause_var = 1
