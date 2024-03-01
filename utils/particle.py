import pygame
from random import randint, uniform
from math import cos, sin


class Particle:
    def __init__(self, game, center: tuple, spawn_radius: float) -> None:
        self.game = game
        self.images: list[pygame.Surface] = self.load_images()
        self.center = pygame.Vector2(center)
        self.pos = self.center

        # Handle random spawn
        self.center = center
        self.spawn_radius = spawn_radius
        self.seconds_to_respawn = uniform(0.6, 1)  # 0.75
        self.current_sec_respawn = 0

        # Handle animation
        self.animation = True
        self.current_index = 0
        self.seconds_per_frame = uniform(0.1, 0.2)  # 0.15
        self.current_sec_animation = 0
        self.current_image = self.images[0]

        self.rect = self.current_image.get_rect(center=self.center)

    def load_images(self) -> list[pygame.Surface]:
        images = []
        images_pos = [(-268, -110), (-261, -110)]
        for pos in images_pos:
            image = pygame.Surface((5, 5))
            image.set_colorkey('#000000')
            image.blit(self.game.sprites_sheet, pos)
            image = pygame.transform.scale_by(image, 5)
            images.append(image)
        return images

    @property
    def random_pos(self):
        random_angle = randint(0, 360)
        random_vector = pygame.Vector2(cos(random_angle), sin(random_angle))
        random_scalar = randint(0, int(self.spawn_radius))
        return self.center + random_vector * random_scalar

    def animate(self, delta_time) -> None:
        # Handle transition between animation and respawn
        if self.current_index >= len(self.images):
            self.animation = False
            self.current_index = -1

        # animation
        if self.animation:
            self.current_sec_animation += delta_time
            # if seconds_per_frame passed
            if self.current_sec_animation > self.seconds_per_frame:
                # next frame
                self.current_image = self.images[self.current_index]
                self.current_index = self.current_index + 1
                # reset current_sec_animation
                self.current_sec_animation = 0

    def respawn(self, delta_time) -> None:
        if not self.animation:
            self.current_sec_respawn += delta_time
            # if enough time passed respawn
            if self.current_sec_respawn > self.seconds_to_respawn:
                # animation
                self.animation = True
                # reset
                self.current_sec_respawn = 0
                # set a random pos
                self.pos = self.random_pos

    def update(self, delta_time) -> None:
        self.animate(delta_time)
        self.respawn(delta_time)
        self.rect.center = self.pos

    def render(self, surface: pygame.Surface) -> None:
        if self.animation:
            surface.blit(self.current_image, self.rect)


class ParticleGroup(list):
    def __init__(self, *args):
        list.__init__(self, *args)

    def update(self, delta_time):
        for particle in self:
            particle.update(delta_time)

    def render(self, surface: pygame.Surface):
        for particle in self:
            particle.render(surface)
