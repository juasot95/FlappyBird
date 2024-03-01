import pygame
from math import atan2, degrees

import states.game_world


class Player(pygame.sprite.Sprite):
    def __init__(self, game_world, x, y) -> None:
        super().__init__()
        self.game_world = game_world
        self.images = self.load_images()
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

        # Motion
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.jump_vector = pygame.Vector2(0, -2.5)  # pygame.Vector2(0, -25)  # pygame.Vector2(0, -2.5)

        # Animation
        self.current_frame = 0
        self.second_per_frame = 0.3
        self.current_time_on_frame = 0

        # Score
        self.current_score = 0

    def load_images(self) -> list[pygame.Surface]:
        image_rects = [(264, 90, 17, 12), (223, 124, 17, 12), (264, 64, 17, 12)]
        images = []
        for rect in image_rects:
            image = pygame.Surface((rect[2], rect[3]))
            image.set_colorkey('#000000')
            image.blit(self.game_world.game.sprites_sheet, (-rect[0], -rect[1]))
            image = pygame.transform.scale_by(image, 5)
            images.append(image)
        return images

    def move(self, delta_time):
        # gravity and jump

        if isinstance(self.game_world, states.game_world.GameWorld):
            self.apply_gravity(delta_time)
            if pygame.mouse.get_pressed()[0]\
                    or self.game_world.game.actions['start']:
                self.jump()
            '''
            speed = 2
            # left and right
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.pos.x += speed * 160 * delta_time
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                self.pos.x -= speed * 160 * delta_time
            # up and down
            if pygame.key.get_pressed()[pygame.K_UP]:
                self.pos.y -= speed * 160 * delta_time
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                self.pos.y += speed * 160 * delta_time
            '''
        self.pos += self.velocity
        self.rect.center = self.pos

    def apply_gravity(self, delta_time) -> None:
        self.velocity.y -= self.game_world.GRAVITY * delta_time

    def jump(self) -> None:
        self.velocity.y = self.jump_vector.y

    @property
    def current_image(self):
        return self.images[self.current_frame]

    def animate(self, delta_time):
        ####################
        # ANIMATION ________
        ####################
        self.current_time_on_frame += delta_time
        if self.current_time_on_frame >= self.second_per_frame:
            self.current_time_on_frame -= self.second_per_frame
            self.current_frame = (self.current_frame + 1) % len(self.images)
            # update image
            self.image = self.images[self.current_frame]
            self.rect = self.image.get_rect(center=self.rect.center)
            self.mask = pygame.mask.from_surface(self.image)
            # update the mask
            self.update_mask()
        ###################
        # INCLINATION _____
        ###################
        dir_vector = pygame.Vector2(-self.game_world.pipes[0].speed, -self.game_world.player.velocity.y)
        angle = degrees(atan2(dir_vector.y, dir_vector.x))
        angle *= 24

        self.image = pygame.transform.rotate(self.current_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def update_game_world(self, game_world):
        self.game_world = game_world

    def update_mask(self):
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, delta_time) -> None:
        self.move(delta_time)
        self.animate(delta_time)

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)



