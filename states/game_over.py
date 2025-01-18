import pygame

from states.state import State
from utils.board import Board
from utils.ui.button import Button
from utils.ui.flag import Flag


class GameOver(State):
    def __init__(self, game, score, last_best_score):
        State.__init__(self, game)
        self.score = score
        self.last_best_score = last_best_score
        self.new_best_score: bool = self.game.best_score > last_best_score
        # use to add the current score to data at the end of a game
        self.score_updated = False
        self.mean_score = round(self.mean(*self.game.data['all_scores']), 2)
        self.board = Board(self.game, self.score)
        self.button_ok = Button(
            self.game,
            'ok',
            (self.game.WIDTH/2, self.board.board_rect.bottom + 10))
        # Game over flag
        self.game_over_flag = Flag(self.game, self.game.WIDTH/2, 150,
                                   swing='v', swing_amount=10, swing_speed=16, image='game_over')

    @staticmethod
    def mean(*args: int):
        return sum(args) / len(args)

    def update(self, delta_time: float, actions: list) -> None:
        self.board.update(delta_time=delta_time)
        self.game_over_flag.update(delta_time)

        if (self.button_ok.is_released() or self.game.actions['start']) and self.button_ok.active:
            # exit from game over state -> playing state
            self.exit_state()
            # exit from playing state -> menu state
            self.prev_state.exit_state()
        self.button_ok.update()
        if not self.game.actions['start']:
            self.button_ok.activate()

    def render(self, surface: pygame.Surface):
        self.prev_state.render(surface)
        self.board.render(surface)
        self.game_over_flag.render(surface)
        self.button_ok.render(surface)
