import pygame

import states.game_over
from utils.canvas import Canvas
from utils.flag import Flag
from utils.medal import Medal


class Board:
    def __init__(self, game, score):
        self.game = game
        self.score = score
        self.load_assets()

    def load_assets(self):
        # create the board
        self.board_image = pygame.Surface((113, 58))
        self.board_image.set_colorkey('#000000')
        self.board_image = self.board_image
        self.board_image.blit(self.game.sprites_sheet, (-146, -58))
        self.board_image = pygame.transform.scale_by(self.board_image, 5)
        self.board_rect = self.board_image.get_rect(center=(self.game.WIDTH/2, self.game.HEIGHT/2))
        # crete the score canvas
        self.score_canvas = Canvas(
            self.score.big_rect.size,
            pygame.Vector2(self.board_rect.topright) - pygame.Vector2(self.score.big_rect.w + 35, -85))
        # create the best score canvas
        self.best_score_canvas = Canvas(
            self.score.little_rect.size,
            pygame.Vector2(self.board_rect.topright) - pygame.Vector2(self.score.little_rect.w + 35, -190))
        # create the new flag
        self.new_flag = Flag(self.game,
                             *self.best_score_canvas.rect.midleft - pygame.Vector2(50, 0),
                             swing_amount=10,
                             swing_speed=24,
                             image='new_flag')
        # create a medal
        self.medal = Medal(self.game)

        # choose the right medal
        if isinstance(self.game.current_state, states.game_over.GameOver):
            # print('CHOOSE MEDAL', self.game.current_state)
            self.choose_medal()

    @staticmethod
    def mean(*args: int):
        return sum(args) / len(args)

    def choose_medal(self):
        if self.game.current_state.new_best_score:
            self.medal.choose('gold')
        elif self.score.current_score > self.mean(
                self.score.best_score * 0.9, self.game.current_state.mean_score) * 0.8:
            self.medal.choose('silver')
        elif self.score.current_score > self.mean(
                self.score.best_score * 0.9, self.game.current_state.mean_score) * 0.2:
            self.medal.choose('bronze')

    def update(self, delta_time):
        self.score_canvas.update()
        self.best_score_canvas.update()
        self.score_canvas.blit(self.score.big_image(), (0, 0))
        self.best_score_canvas.blit(self.score.little_image(), (0, 0))
        # update the new flag
        # if the beste score if greater than the last best score
        if isinstance(self.game.current_state, states.game_over.GameOver):
            if self.game.current_state.new_best_score:
                self.new_flag.update(delta_time=delta_time)
        # update the medal
        self.choose_medal()
        self.medal.update(delta_time)

    def render(self, surface: pygame.Surface):
        self.game.game_canvas.blit(self.board_image, self.board_rect)
        self.score_canvas.render(self.game.game_canvas)
        self.best_score_canvas.render(self.game.game_canvas)
        # render the new flag
        # if the beste score if greater than the last best score
        if isinstance(self.game.current_state, states.game_over.GameOver):
            if self.game.current_state.new_best_score:
                self.new_flag.render(surface)
        # render the medal
        self.medal.render(surface)
