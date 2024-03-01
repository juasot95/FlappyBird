import pygame


class Ground(pygame.sprite.Sprite):
    def __init__(self, game_world, top_left: tuple = (0, 600), speed=240):
        super().__init__()
        self.game_world = game_world
        self.speed = speed
        self.top_left = pygame.Vector2(top_left)
        self.image, self.rect, self.mask = self.load_image()

        self.group = pygame.sprite.GroupSingle(self)

    def load_image(self) -> (pygame.Surface, pygame.Rect, pygame.mask):
        ground_image = pygame.Surface((154, 56))
        ground_image.set_colorkey('#000000')
        ground_image.blit(self.game_world.game.sprites_sheet, (-146, 0))
        ground_image = pygame.transform.scale_by(ground_image, 5)

        image = pygame.Surface((ground_image.get_width()*2, ground_image.get_height()))
        image.set_colorkey('#000000')
        image.blit(ground_image, (0, 0))
        image.blit(ground_image, (ground_image.get_width(), 0))

        return image, image.get_rect(topleft=self.top_left), pygame.mask.from_surface(image)

    def update(self, delta_time):
        self.move(delta_time)

    def move(self, delta_time):
        self.top_left.x += self.speed * delta_time
        if self.top_left.x < -(7 * self.image.get_width()) // 154:
            self.top_left.x = 0
        # update the rect pos
        self.rect.topleft = self.top_left

    def render(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)
