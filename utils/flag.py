import pygame


class Flag(pygame.sprite.Sprite):
    def __init__(self, game, x, y, swing='vertical', swing_amount=20, swing_speed=32, image='flappy bird') -> None:
        super().__init__()
        self.game = game
        self.image, self.rect = self.load_image(image, x, y)
        self.pos = pygame.Vector2(x, y)

        self.default_x = x
        self.default_y = y
        self.swing = swing
        self.swing_amount = swing_amount
        self.swing_speed = swing_speed
        self._dir = 0

    def load_image(self, image, x=0, y=0) -> (pygame.Surface, pygame.Rect):
        if image == 'flappy bird':
            flag_image = pygame.Surface((96, 22))
            flag_image.set_colorkey('#000000')
            flag_image.blit(self.game.sprites_sheet, (-146, -173))
            flag_image = pygame.transform.scale_by(flag_image, 5)
            return flag_image, flag_image.get_rect()
        elif image == 'game_over':
            flag_image = pygame.Surface((94, 19))
            flag_image.set_colorkey('#000000')
            flag_image.blit(self.game.sprites_sheet, (-146, -199))
            flag_image = pygame.transform.scale_by(flag_image, 5)
            return flag_image, flag_image.get_rect()
        elif image == 'get_ready':
            flag_image = pygame.Surface((87, 22))
            flag_image.set_colorkey('#000000')
            flag_image.blit(self.game.sprites_sheet, (-146, -221))
            flag_image = pygame.transform.scale_by(flag_image, 5)
            return flag_image, flag_image.get_rect()
        elif image == 'new_flag':
            flag_image = pygame.Surface((16, 7))
            flag_image.set_colorkey('#000000')
            flag_image.blit(self.game.sprites_sheet, (-146, -245))
            flag_image = pygame.transform.scale_by(flag_image, 5)
            return flag_image, flag_image.get_rect()
        else:
            # FLAPPY BIRD flag by defaul
            flag_image = pygame.Surface((96, 22))
            flag_image.set_colorkey('#000000')
            flag_image.blit(self.game.sprites_sheet, (-146, -173))
            flag_image = pygame.transform.scale_by(flag_image, 5)
            return flag_image, flag_image.get_rect(center=self.pos)

    def update(self, delta_time) -> None:
        self.move(delta_time)
        self.rect.center = self.pos

    def move(self, delta_time) -> None:
        # vertical movement
        if 'v' in self.swing:
            current_y = self.pos.y
            default_y = self.default_y

            # if going up
            if self._dir:
                # if going to high go down
                if current_y < default_y - self.swing_amount:
                    # print('up -> down')
                    self._dir = False
                    self.pos.y += self.swing_speed * delta_time
                # else go up
                else:
                    # print('up')
                    self.pos.y -= self.swing_speed * delta_time
            # going down
            else:
                # if going too low go up
                if current_y > default_y + self.swing_amount:
                    # print('down -> up')
                    self._dir = True
                    self.pos.y -= self.swing_speed * delta_time
                # else go down
                else:
                    # print('down')
                    self.pos.y += self.swing_speed * delta_time
        # horizontal movement
        if 'h' in self.swing:
            current_x = self.pos.x
            default_x = self.default_x

            # if going up
            if self._dir:
                # if going too to the right go left
                if current_x < default_x - self.swing_amount:
                    # print('right -> left')
                    self._dir = False
                    self.pos.x += self.swing_speed * delta_time
                # else go right
                else:
                    # print('right')
                    self.pos.x -= self.swing_speed * delta_time
            # going down
            else:
                # if going too to the left go right
                if current_x > default_x + self.swing_amount:
                    # print('left -> right')
                    self._dir = True
                    self.pos.x -= self.swing_speed * delta_time
                # else go left
                else:
                    # print('left')
                    self.pos.x += self.swing_speed * delta_time

    def render(self, surface):
        surface.blit(self.image, self.rect)
