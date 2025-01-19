import pygame

from states.state import State
from states.wait_to_play import WaitToPlay
from utils.ui.button import Button
from utils.ui.flag import Flag


class Menu(State):
    def __init__(self, game) -> None:
        State.__init__(self, game)
        self.start_button = Button(game, 'start', (self.game.WIDTH/2, self.game.HEIGHT/2))
        self.bg = pygame.Surface((self.game.WIDTH, self.game.HEIGHT))
        self.load_bg()
        self.flappy_flag = Flag(game, self.game.WIDTH//2, 150, swing='v')

    def load_bg(self) -> None:

        little_bg = pygame.Surface((144, 256))
        little_bg.blit(self.game.sprites_sheet, (0, 0))
        little_bg = pygame.transform.scale_by(little_bg, self.game.HEIGHT/little_bg.get_height())

        # create the bg that will fill all the screen
        for i in range(self.bg.get_width()//little_bg.get_width()+1):
            x = i * little_bg.get_width()
            self.bg.blit(little_bg, (x, 0))

    def update(self, delta_time, actions) -> None:
        self.flappy_flag.update(delta_time)
        if (self.start_button.is_released() or self.game.actions['start']) and self.start_button.active:
            # print('Start Button : CLICKED')
            # enter in wait_to_play state (menu -> wait_to_play)
            wait_to_play = WaitToPlay(self.game)
            wait_to_play.enter_state()
        self.start_button.update()
        if not self.game.actions['start']:
            self.start_button.activate()

    def render(self, surface: pygame.Surface) -> None:
        surface.fill('#000000')
        surface.set_colorkey('#000000')
        self.game.game_canvas.blit(self.bg, (0, 0))

        # If the current state is the menu
        if self.game.state_stack[-1] is self:
            # Render the Flag
            self.flappy_flag.render(self.game.game_canvas)
            # Render all buttons
            self.start_button.render(self.game.game_canvas)
