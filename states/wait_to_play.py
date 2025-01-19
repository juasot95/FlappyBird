import pygame
from states.state import State
from states.game_world import GameWorld
from utils.game_insight.player import Player
from utils.game_insight.ground import Ground
from utils.ui.flag import Flag


class WaitToPlay(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.GRAVITY = 0
        self.game_gravity = -15
        self.speed = -240
        self.player = Player(self, x=self.game.WIDTH//4, y=self.game.HEIGHT//2)
        self.ground = Ground(self, top_left=(0, 650), speed=self.speed)
        self.click_image, self.click_image_rect, self.click_image_mask = self.load_click_image()
        self.get_ready_flag = Flag(self.game,
                                   self.game.WIDTH/2,
                                   150,
                                   swing='v',
                                   swing_amount=10,
                                   swing_speed=16,
                                   image='get_ready')
        self.active = False

    def load_click_image(self):
        click_image = pygame.Surface((39, 49))
        click_image.set_colorkey('#000000')
        click_image.blit(self.game.sprites_sheet, (-172, -122))
        click_image = pygame.transform.scale_by(click_image, 5)
        return (click_image, click_image.get_rect(center=(self.game.WIDTH//3*2, self.game.HEIGHT//2)),
                pygame.mask.from_surface(click_image))

    def activate(self) -> None:
        self.active = True

    def update(self, delta_time: float, actions: list) -> None:
        # update the GET READY flag
        self.get_ready_flag.update(delta_time)
        # prevent from skipping the wait_to_play state
        if not self.game.actions['start']:
            self.activate()
        # self.player.update(delta_time)  # optional
        # self.ground.update(delta_time)  # better without
        # Change to playing state
        if (self.game.actions['start']
                or self.game.actions['up']
                or pygame.mouse.get_pressed()[0]) and self.active:
            # exit from wait_to_play state (wait_to_play -> menu)
            self.exit_state()
            # enter game_world state (menu -> game_world)
            game_world = GameWorld(self.game, self.speed, self.player, self.ground)
            game_world.enter_state()
            self.player.update_game_world(game_world)

    def render(self, surface: pygame.Surface) -> None:
        self.prev_state.render(self.game.game_canvas)
        self.ground.render(self.game.game_canvas)
        self.player.render(self.game.game_canvas)
        # render the click image
        self.game.game_canvas.blit(self.click_image, self.click_image_rect)
        # render the get ready flag
        self.get_ready_flag.render(self.game.game_canvas)

