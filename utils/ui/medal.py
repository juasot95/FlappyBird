import pygame
from utils.ui.particle import Particle, ParticleGroup


class Medal:
    def __init__(self, game):
        self.game = game
        self._type = 'None'
        self.images: dict[str, pygame.Surface] = self.load_images()
        self.default_image = self.images[self._type]
        self.image = self.default_image
        self.rect = self.image.get_rect(center=(377, 377))

        self.particle = ParticleGroup(
            [Particle(game, (377, 377), self.rect.h / 2) for i in range(3)]
        )

    def load_images(self) -> dict[str, pygame.Surface]:
        images = {}
        xpos_images = {'None': (-220, -144), 'bronze': (-302, -137), 'silver': (-266, -229), 'gold': (-242, -229)}
        for _type, pos in xpos_images.items():
            image = pygame.Surface((22, 22))
            image.set_colorkey('#000000')
            image.blit(self.game.sprites_sheet, pos)
            image = pygame.transform.scale_by(image, 5)
            images[_type] = image
        return images

    def choose(self, _type='None'):
        if _type in self.images.keys():
            self._type = _type
            self.image = self.images[self._type]

    def update(self, delta_time):
        self.particle.update(delta_time)

    def render(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)
        if self._type in ('silver', 'gold'):
            self.particle.render(surface)

