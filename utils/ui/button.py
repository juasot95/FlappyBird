import pygame
from typing import override
from utils.sound.sound import SoundHandler


class Button(pygame.sprite.Sprite):

    type_rects = {
        # regular Buttons
        'menu': pygame.Rect(246, 118, 40, 14),
        'ok': pygame.Rect(246, 134, 40, 14),
        'rate': pygame.Rect(246, 150, 40, 14),
        'score': pygame.Rect(244, 173, 40, 14),
        'share': pygame.Rect(242, 197, 40, 14),
        'start': pygame.Rect(242, 213, 40, 14),
        # play / pause Buttons
        'play': pygame.Rect(287, 84, 13, 14),
        'pause': pygame.Rect(287, 58, 13, 14)

    }

    def __init__(self, game, _type: str, pos: tuple[int, int] = (0, 0), offset: int = 5) -> None:
        super().__init__()
        self.game = game
        self._type = _type

        self._type_rect = self.type_rects[self._type]
        self.button_image, self.rect = self.load_image(pos, self.type_rects)

        self.pressed = False
        self.default_y = pos[1]
        self.offset = offset

        self.active = False

    def load_image(self, pos, type_rects: dict) -> (pygame.Surface, pygame.rect):
        button_image = pygame.Surface(self._type_rect.size)
        button_image.set_colorkey('#000000')
        button_image.blit(self.game.sprites_sheet,
                               (-self._type_rect.x, -self._type_rect.y))
        button_image = pygame.transform.scale_by(button_image, 5)
        rect = button_image.get_rect(center=pos)
        return button_image, rect

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.button_image, self.rect)

    def update(self, *args, **kwargs) -> None:
        if self.is_pressed():
            self.pressed = True
            self.rect.y = self.default_y + self.offset
        else:
            self.rect.y = self.default_y
        # not for pause button
        if isinstance(self, Button):
            self.active = False

    def activate(self):
        self.active = True

    def is_pressed(self) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        on_button = self.rect.collidepoint(*mouse_pos)
        clicked = pygame.mouse.get_pressed()[0]
        if on_button and clicked:
            if not self.pressed:
                SoundHandler.click()
                self.pressed = True
            return True
        return False

    def is_released(self) -> bool:
        if not self.is_pressed() and self.pressed:
            self.pressed = False
            return True
        return False


class PauseButton(Button):
    def __init__(self, game, pos: tuple[int, int] = (0, 0), offset: int = 5) -> None:
        super().__init__(game, 'play', pos, offset)
        self.state_images = {
            'play': self.load_image(self.rect.center, self.type_rects)[0],
            'pause': self.load_image(self.rect.center, self.type_rects)[0]
        }
        self.update_state_images()

    def update_state_images(self):
        self._type_rect = self.type_rects['pause']
        self.state_images['pause'] = self.load_image(self.rect.center, self.type_rects)[0]
        self._type_rect = self.type_rects['play']

    def update_image(self) -> None:
        self.button_image = self.state_images[self._type]

    def change_state(self) -> None:
        self._type = ('play', 'pause')[self._type == 'play']
        self.update_image()
        self.active = False

