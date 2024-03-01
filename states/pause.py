import pygame

from states.state import State


class Pause(State):
    def __init__(self, game, pause_button):
        super().__init__(game)
        self.game = game
        self.pause_button = pause_button

    def update(self, delta_time: float, actions: list) -> None:
        self.prev_state.update(delta_time, actions)

    def render(self, surface: pygame.Surface):
        self.prev_state.render(surface)
