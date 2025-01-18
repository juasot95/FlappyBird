from typing import Final
import os
import pygame
from pygame.mixer import Sound, Channel

WOOSH: Final[Sound] = Sound(os.path.join('assets/sounds/flappy_whoosh.mp3'))
TING: Final[Sound] = Sound(os.path.join('assets/sounds/ting.wav'))
CLICK: Final[Sound] = Sound(os.path.join('assets/sounds/click.wav'))
WIN: Final[Sound] = Sound(os.path.join('assets/sounds/win.wav'))
LOSE: Final[Sound] = Sound(os.path.join('assets/sounds/lose.wav'))


class SoundHandler:
    win_state = Channel(0)
    jump_channel = Channel(1)
    sound_effects = Channel(2)
    _ambient_volume = 1.

    @classmethod
    def set_ambient_volume(cls, vol: float):
        cls._ambient_volume = max(0., min(1., vol))

    @classmethod
    def update_vol(cls, sound: Sound):
        sound.set_volume(cls._ambient_volume)

    @staticmethod
    def jump() -> None:
        SoundHandler.update_vol(WOOSH)
        SoundHandler.jump_channel.play(WOOSH, fade_ms=100)

    @staticmethod
    def increment_score() -> None:
        SoundHandler.update_vol(TING)
        SoundHandler.sound_effects.play(TING)

    @staticmethod
    def click() -> None:
        SoundHandler.update_vol(CLICK)
        SoundHandler.sound_effects.play(CLICK)

    @staticmethod
    def lose() -> None:
        SoundHandler.update_vol(LOSE)
        SoundHandler.win_state.play(LOSE)

    @staticmethod
    def win() -> None:
        SoundHandler.update_vol(WIN)
        SoundHandler.win_state.play(WIN)
