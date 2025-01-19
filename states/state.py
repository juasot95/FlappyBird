import pygame
from utils.sound.sound import SoundHandler


class State:
    def __init__(self, game):
        self.game = game
        self.prev_state = None

    def update(self, delta_time: float, actions: list) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        pass

    def enter_state(self) -> None:
        if len(self.game.state_stack) >= 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)
        print(type(self), ': ENTERED')

    def exit_state(self) -> None:
        self.game.state_stack.pop()
        print(type(self), ': EXIT')
