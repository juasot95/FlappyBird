import pygame

from states.state import State
from states.game_over import GameOver
from states.pause import Pause

from utils.game_insight.pipe import Pipe, PipeGroup
from utils.ui.score import Score
from utils.ui.button import PauseButton


class GameWorld(State):
    def __init__(self, game, speed, player, ground):
        State.__init__(self, game)
        self.GRAVITY = -15  # - 150  # 15
        self.speed = speed
        self.playing = True

        # self.player = Player(self, x=self.game.WIDTH//4, y=self.game.HEIGHT//2)
        self.player = player
        # Pipe group and the ground
        self.ground = ground
        self.pipes = PipeGroup(self, [Pipe(self, speed=self.speed)for i in range(5)])
        # Score
        self.score = Score(self, (self.game.WIDTH/2, 100), (self.game.WIDTH/2, 150))
        self.last_best_score = self.game.best_score
        # Pause button
        self.pause_button = PauseButton(game, (50, 25))

    @property
    def collision(self) -> bool:
        """return True if the player has collided with a pipe"""
        return pygame.sprite.spritecollide(self.player, self.pipes.sprite_group, False,
                                           collided=pygame.sprite.collide_mask)  # NOQA

    @property
    def on_ground(self) -> bool:
        """returns True if the players has collided with the ground"""
        beneath_the_ground: bool = self.player.pos.y > self.ground.top_left.y
        collision = pygame.sprite.spritecollide(self.player, self.ground.group, False,
                                                collided=pygame.sprite.collide_mask)  # NOQA
        return beneath_the_ground or collision

    @property
    def above_screen(self) -> bool:
        """returns True if the player is above the screen"""
        above = self.player.pos.y < 0
        return above

    @property
    def lost(self):
        return self.collision or self.on_ground or self.above_screen

    def update(self, delta_time: float, actions: list) -> None:
        ########################
        # PAUSE BUTTON__________
        ########################

        # check pause button is released
        pause_pressed_keyboard = pygame.key.get_pressed()[pygame.K_PAUSE] or pygame.key.get_pressed()[pygame.K_p]
        trigger_pause = self.pause_button.is_released() or pause_pressed_keyboard

        # trigger the Pause state
        if trigger_pause and self.pause_button.active:
            self.pause_button.change_state()
            # change state : game_world -> Pause
            if isinstance(self.game.current_state, GameWorld):
                # enter into Pause state (game_world -> Pause)
                # print('Pause state: ENTERED')
                pause_state = Pause(self.game, self.pause_button)
                pause_state.enter_state()
            # change state : Pause -> game_world
            else:
                # exit from Pause state (Pause -> game_world)
                self.game.current_state.exit_state()

        self.pause_button.update()

        # activated the pause_button if the keyboard stop being pressed
        if not pause_pressed_keyboard:
            self.pause_button.activate()
            # print(f'BUTTON ACTIVATED : {self.pause_button.active}')

        ########################
        # GAME UPDATES__________
        ########################

        # updates that are specific to the game
        if isinstance(self.game.current_state, GameWorld):
            if self.on_ground:
                self.player.pos.y = min(self.player.pos.y+self.player.rect.h//2, self.ground.top_left.y)
                # print('LOST')
                self.game.sound_handler.lose()
                # enter in game_over state (game_world -> game_over)
                game_over = GameOver(self.game, self.score, self.last_best_score)
                game_over.enter_state()
            elif self.lost or not self.playing:
                self.playing = False
                self.player.update(delta_time, dead=True)
            else:
                self.player.update(delta_time)
                self.pipes.update(delta_time)
                self.ground.update(delta_time)
                self.score.update()

    def render(self, surface: pygame.Surface) -> None:
        self.prev_state.render(self.game.game_canvas)
        self.pipes.render(self.game.game_canvas)
        self.ground.render(self.game.game_canvas)
        self.player.render(self.game.game_canvas)
        self.pause_button.render(self.game.game_canvas)
        # only render the score if we are in the playing state or pause state (game world  or  pause)
        if isinstance(self.game.current_state, GameWorld) or isinstance(self.game.current_state, Pause):
            self.score.render(self.game.game_canvas)


