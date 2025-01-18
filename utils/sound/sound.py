from typing import Final
import pygame
from pygame.mixer import Sound, Channel

WOOSH: Final[Sound] = Sound('assets/flappy_whoosh.mp3')
TING: Final[Sound] = Sound('assets/ting.wav')
WIN: Final[Sound] = Sound('assets/win.wav')
LOSE: Final[Sound] = Sound('assets/lose.wav')


class SoundHandler:
    def __init__(self):
        self.win_state = Channel(0)
        self.jump_channel = Channel(1)
        self.sound_effects = Channel(2)

    def jump(self):
        self.jump_channel.play(WOOSH, fade_ms=100)

    def increment_score(self):
        self.sound_effects.play(TING)

    def lose(self):
        self.win_state.play(LOSE)
