from typing import Tuple, List

import pygame
from pygame import Surface

import states.game_world


class Score(pygame.sprite.Sprite):
    def __init__(self, game_world, big_pos, little_pos):
        super().__init__()
        self.game_world = game_world

        self.big_pos, self.little_pos = big_pos, little_pos

        self.little_num_images, self.big_num_images = self.load_image()
        self.little_num_rect = self.little_num_images[0].get_rect()
        self.big_num_rect = self.big_num_images[0].get_rect()

        self.big_rect = self.big_image().get_rect(center=self.big_pos)
        self.little_rect = self.little_image().get_rect(center=self.little_pos)

    def load_image(self) -> tuple[list[Surface], list[Surface]]:
        # generate the little num images
        little_num_images = []
        little_num_pos = [
            (-287, -74),    # 0
            (-288, -162),  # 1
            (-204, -245),  # 2
            (-212, -245),  # 3
            (-220, -245),  # 4
            (-228, -245),  # 5
            (-284, -197),  # 6
            (-292, -197),  # 7
            (-284, -213),  # 8
            (-292, -213),  # 9
        ]
        for pos in little_num_pos:
            image = pygame.Surface((6, 7))
            # image.fill('#FF0000')
            # image.set_colorkey('#FF0000')
            image.blit(self.game_world.game.sprites_sheet, pos)
            # image = pygame.transform.scale_by(image, 5)
            little_num_images.append(image)
        # generate the big num images
        big_num_images = []
        big_num_pos = [
            (-288, -100),  # 0
            (-289, -118),  # 1
            (-289, -134),  # 2
            (-289, -150),  # 3
            (-287, -173),  # 4
            (-287, -185),  # 5
            (-165, -245),  # 6
            (-175, -245),  # 7
            (-185, -245),  # 8
            (-195, -245),  # 9
        ]
        for pos in big_num_pos:
            image = pygame.Surface((7, 10))
            # image.fill('#FF0000')
            # image.set_colorkey('#FF0000')
            image.blit(self.game_world.game.sprites_sheet, pos)
            # image = pygame.transform.scale_by(image, 5)
            big_num_images.append(image)
        return little_num_images, big_num_images

    @property
    def current_score(self):
        return self.game_world.player.current_score

    @property
    def best_score(self):
        return self.game_world.game.best_score

    def big_image(self):
        score = self.current_score
        score_str = str(score)
        image_width = (self.big_num_rect.w + 1) * len(score_str)
        image = pygame.Surface((image_width, self.big_num_rect.h))
        image.set_colorkey('#000000')
        # generate
        for i, num in enumerate(score_str):
            num_image = self.big_num_images[int(num)]
            xpos_num = (self.big_num_rect.w + 1) * i
            image.blit(num_image, (xpos_num, 0))
        # resize image
        image = pygame.transform.scale_by(image, 5)
        return image

    def little_image(self):
        score = self.best_score
        score_str = str(score)
        image_width = (self.little_num_rect.w + 1) * len(score_str)
        image = pygame.Surface((image_width, self.little_num_rect.h))
        image.set_colorkey('#000000')
        # generate image
        for i, num in enumerate(score_str):
            num_image = self.little_num_images[int(num)]
            xpos_num = (self.little_num_rect.w + 1) * i
            image.blit(num_image, (xpos_num, 0))
        # resize
        image = pygame.transform.scale_by(image, 5)
        return image

    def update(self, *args, **kwargs):
        # update best score
        if self.current_score > self.best_score:
            self.game_world.game.best_score = self.current_score
        # update pos for the game_world
        if isinstance(self.game_world.game.current_state, states.game_world.GameWorld):
            self.big_rect = self.big_image().get_rect(center=self.big_pos)
            self.little_rect = self.little_image().get_rect(center=self.little_pos)

    def render(self, surface: pygame.Surface):
        big_image = self.big_image()
        big_rect = big_image.get_rect(center=self.big_pos)
        little_image = self.little_image()
        little_rect = little_image.get_rect(center=self.little_pos)
        surface.blit(big_image, big_rect)
        surface.blit(little_image, little_rect)
