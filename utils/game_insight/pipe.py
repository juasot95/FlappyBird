import pygame
import random
from typing import override


class Pipe(pygame.sprite.Sprite):
    def __init__(self, game_world, speed=-240,  x=0, y=0):
        super().__init__()
        self.game_world = game_world
        self.pos = pygame.Vector2(x, y)
        self.image, self.rect, self.mask = self.load_image()

        # x, y are initialize in the PipeGroup
        self.pipe_group = None

        self.speed = speed

        # Reward
        self.default_reward = 1
        self.reward = self.default_reward

    def load_image(self) -> (pygame.Surface, pygame.Rect, pygame.mask):
        top_pipe = pygame.Surface((26, 135))
        top_pipe.set_colorkey('#000000')
        top_pipe.blit(self.game_world.game.sprites_sheet, (-302, 0))
        bottom_pipe = pygame.Surface((26, 121))
        bottom_pipe.set_colorkey('#000000')
        bottom_pipe.blit(self.game_world.game.sprites_sheet, (-330, 0))

        both_pipes = pygame.Surface((26, 250))
        both_pipes.set_colorkey('#000000')
        space_between_pipes = 50
        both_pipes.blit(top_pipe, top_pipe.get_rect(bottom=both_pipes.get_height()/2-space_between_pipes/2))
        both_pipes.blit(bottom_pipe, both_pipes.get_rect(top=both_pipes.get_height()/2+space_between_pipes//2))
        both_pipes = pygame.transform.scale_by(both_pipes, 5)

        return both_pipes, both_pipes.get_rect(center=self.pos), pygame.mask.from_surface(both_pipes)

    def update(self, delta_time):
        self.move(delta_time)

    def render(self, surface: pygame.Surface):
        # pygame.draw.rect(surface, '#993333', self.rect, 3, 5)
        surface.blit(self.image, self.rect)

    def move(self, delta_time):
        # move
        self.pos.x += self.speed * delta_time
        # update rect pos
        self.rect.center = self.pos
        # respawn to the left
        if self.rect.right < 0:
            self.rect.left = self.game_world.game.WIDTH
            self.pos = pygame.Vector2(self.rect.center)
            self.reset()

    def get_random_y(self) -> int:
        window_height = self.game_world.game.HEIGHT
        return random.randint(window_height//4, -window_height//4 + self.game_world.ground.rect.y)

    def reset(self):
        # reset pos of the pipe
        if self.pipe_group:
            self.pos.x = self.pipe_group.furthest_pipe.pos.x + self.pipe_group.sep_x
            self.pos.y = self.get_random_y()
            self.rect.center = self.pos
        else:
            self.pos.y = self.get_random_y()
            self.rect.center = self.pos
        # reset reward
        self.reward = self.default_reward


class PipeGroup(list):
    def __init__(self, game_world, *args) -> None:
        list.__init__(self, *args)
        # print('PipeGroup __init__()')
        # print(*args)
        self.game_world = game_world
        self.sep_x = self.game_world.game.WIDTH/3
        self.__init_the_pipes__()
        self.sprite_group = pygame.sprite.Group(*args)

    @property
    def furthest_pipe(self) -> Pipe:
        return max(self, key=lambda pipe: pipe.pos.x)

    @property
    def reward_pipes(self):
        return filter(lambda pipe: pipe.reward > 0, self)

    def nearest_pipe(self, group=None) -> Pipe:
        if group:
            return min(group, key=lambda pipe: pipe.pos.x)
        return min(self, key=lambda pipe: pipe.pos.x)

    def __init_the_pipes__(self) -> None:
        for i, pipe in enumerate(self):
            pipe.pipe_group = self
            pipe.rect.midleft = pygame.Vector2(
                pipe.game_world.game.WIDTH * 1 + i * self.sep_x,
                pipe.get_random_y())
            pipe.pos = pygame.Vector2(pipe.rect.center)

    def update(self, *args, **kwargs) -> None:
        # update pipes
        for pipe in self:
            pipe.update(*args, **kwargs)
        # Handle player score
        if (nearest_pipe := self.nearest_pipe(self.reward_pipes)).rect.left < self.game_world.player.rect.centerx:
            # Play the sound effect
            self.game_world.game.sound_handler.increment_score()
            # Modify the score
            self.game_world.player.current_score += nearest_pipe.reward
            nearest_pipe.reward = 0
            # print(self.game_world.player.current_score)

    def render(self, surface: pygame.Surface) -> None:
        for pipe in self:
            pipe.render(surface)


