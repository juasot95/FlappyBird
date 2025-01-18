import pygame
pygame.init()
pygame.mixer.pre_init(
    frequency=44100, size=-16, channels=8,
    buffer=512, devicename=None)
pygame.mixer.init()
