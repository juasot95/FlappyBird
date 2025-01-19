import pygame
import os
import time
import json

from utils.sound.sound import SoundHandler

import states.state
from states.menu import Menu
from states.game_world import GameWorld
from states.game_over import GameOver


class Game:

    def __init__(self, width: int = 1080, height: int = 720) -> None:
        # Initialize the window
        pygame.init()
        self.WIDTH, self.HEIGHT = width, height
        pygame.display.set_caption('Flappy Bird')
        self.screen = pygame.display.set_mode((width, height))
        self.game_canvas = pygame.Surface((width, height))

        # Instantiate the SoundHandler
        self.sound_handler = SoundHandler()

        # Set running to True for the game loop
        self.running = True
        self.actions = {'left': False, 'right': False, 'up': False, 'down': False, 'start': False, 'pause': False}

        # Handle FPS and delta time
        self.FPS = 160
        self.clock = pygame.time.Clock()
        self.dt, self.prev_time = 0, time.perf_counter()

        # Create a stack to handle game states
        self.state_stack = []

        # Load some basic stuff
        self.new_data = True
        self.data = self.load_data()
        self.load_assets()
        self.load_states()

        # Store best score
        self.best_score = self.data['best_score']

    @property
    def current_state(self) -> states.state.State:
        return self.state_stack[-1]

    @staticmethod
    def quit():
        pygame.quit()
        quit()

    def game_loop(self) -> None:
        """
        run the game
        :return:
        """
        while self.running:
            self.update_delta_time()
            self.get_events()
            self.update()
            self.render()
            self.clock.tick(self.FPS)
        self.quit()

    def get_events(self) -> None:
        """
        updates self.actions
        :return:
        """
        for event in pygame.event.get():
            # stop the game
            if event.type == pygame.QUIT:
                self.save_data()
                self.running = False
            # True if the key is key pressed else false
            pressed = ((event.type == pygame.KEYDOWN) and (event.type != pygame.KEYUP))
            # set the actions
            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                if event.unicode == 'z': self.actions['up'] = pressed
                if event.unicode == 's': self.actions['down'] = pressed
                if event.unicode == 'q': self.actions['left'] = pressed
                if event.unicode == 'd': self.actions['right'] = pressed
                if event.key == pygame.K_RETURN: self.actions['start'] = pressed
                if event.key == pygame.K_KP_ENTER: self.actions['start'] = pressed
                if event.key == pygame.K_SPACE: self.actions['start'] = pressed

    def update(self) -> None:
        """
        updates the current state
        :return:
        """
        self.current_state.update(self.dt, self.actions)
        self.update_data()

    def render(self) -> None:
        """
        renders the current states
        :return:
        """
        self.current_state.render(self.game_canvas)
        self.screen.blit(self.game_canvas, (0, 0))
        pygame.display.flip()

    def update_delta_time(self) -> None:
        """
        updates self.dt
        :return:
        """
        now = time.perf_counter()
        self.dt = now - self.prev_time
        self.prev_time = now

    def draw_text(self, surface, text, color, x, y, _type: str = None) -> None:
        """
        draws some text on a surface
        :param surface: pygame.Surface
        :param text: str
        :param color: str | tuple[int, int, int]
        :param x: int
        :param y: int
        :param _type: None | str
        :return:
        """
        if _type is None:
            font = self.font
        elif isinstance(_type, str):
            if _type.lower() == 'title':
                font = self.title_font
            else:
                font = self.font
        else:
            font = self.font

        text_surface = font.render(text, True, color)
        text_surface.set_colorkey((0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = x, y
        surface.blit(text_surface, text_rect)

    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False

    def load_data(self) -> dict:
        # if file exists load the data
        if os.path.isfile(os.path.join('data', 'data.json')):
            with open(os.path.join('data', 'data.json')) as file:
                self.new_data = False
                return json.load(file)

        # else create default data
        else:
            return {'best_score': 0, 'all_scores': [0]}

    def load_assets(self) -> None:
        """
        load the fonts and the sprites_sheet
        :return:
        """
        self.title_font = pygame.font.Font(None, 52)
        self.font = pygame.font.Font(None, 20)
        self.sprites_dir = os.path.join('assets', 'spritesheet', 'flappy_sprites.png')
        self.sprites_sheet = pygame.image.load(self.sprites_dir).convert_alpha()
        self.icon = pygame.Surface((17, 17))
        self.icon.set_colorkey('#000000')
        self.icon.blit(self.sprites_sheet, (-264, -87))

        pygame.display.set_icon(self.icon)

    def load_states(self) -> None:
        """
        load the starting state
        :return:
        """
        self.menu_screen = Menu(self)
        self.menu_screen.enter_state()

    def save_data(self):
        # update data
        self.data['best_score'] = self.best_score
        # save data
        data_directory = os.path.join('data', 'data.json')
        # if file exists write data in file
        if os.path.exists(data_directory):
            with open(data_directory, 'w') as file:
                json.dump(self.data, file)
        # create a file
        else:
            with open(data_directory, 'w') as file:
                json.dump(self.data, file)
        print('DATA SAVED')

    def update_data(self):
        self.data['best_score'] = self.best_score
        if isinstance(self.current_state, GameOver):
            # if data not updated add a new
            if not self.current_state.score_updated:
                print('Add New Score to DATA')
                if 'all_scores' in self.data.keys():
                    # if it is a new data then remove the first 0
                    # which has been set at the creation of the new data (self.load_data())
                    if self.new_data and len(self.data['all_scores']) > 1:
                        self.data['all_scores'].pop(0)
                        self.new_data = False
                        print(self.data)
                    self.data['all_scores'].append(self.current_state.score.current_score)
                    self.current_state.score_updated = True
                else:
                    self.data['all_scores'] = [self.current_state.score.current_score]
        else:
            if not isinstance(self.current_state, GameWorld):
                self.current_state.score_updated = False


if __name__ == '__main__':
    g = Game()
    g.game_loop()
