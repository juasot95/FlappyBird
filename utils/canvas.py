import pygame


class Canvas(pygame.Surface):

    def __init__(self, size, pos, *args, color_reset='#000000', **kwargs):
        super().__init__(size, *args, **kwargs)
        self.pos = pos
        self.rect = self.get_rect(topleft=pos)
        self.color_reset = color_reset

    def reset(self):
        self.fill(self.color_reset)
        self.set_colorkey(self.color_reset)

    def update(self, pos=None):
        self.reset()
        if pos:
            self.pos = pos
        self.rect = self.get_rect(topleft=self.pos)

    def render(self, surface: pygame.Surface):
        surface.blit(self, self.rect)
