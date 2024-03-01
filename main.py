from game import Game


if __name__ == '__main__':
    game = Game(1080, 720)
    game.game_loop()
    '''
    while game.running:
        game.update_delta_time()
        game.get_events()
        game.update()
        game.render()
        game.clock.tick(game.FPS)
    game.quit()
    '''
