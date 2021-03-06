import pygame
from pygame.locals import *

from pygame import mixer

from enum import Enum

from player import Player
from world import World
from button import Button
from util import draw_text

class GameState(Enum):
    GAME_OVER = 0
    START = 1
    PLAYING = 2
    EXIT = 3

class Game:
    def __init__(self, width, height, tile_size, levels, fps=60, name="Game"):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        mixer.init()
        pygame.init()

        self.width = width
        self.height = height

        self.tile_size = tile_size

        self.fps = fps

        self.levels = levels
        self.current_level = 0

        self.score = 0

        self.game_state = GameState.START

        self.player = Player(100, self.height - 130, self.on_die, self.next_level, self.add_to_score)
        self.world = levels[self.current_level].load_world(tile_size)
        self.clock = pygame.time.Clock()

        # FIXME: move to proper location
        # ===================================================================================================== 
        image_restart = pygame.image.load('img/restart_btn.png')
        self.restart_button = Button(self.width // 2 - 50, self.height // 2 + 100, image_restart, self.reset)

        image_start = pygame.image.load('img/start_btn.png')
        self.start_button = Button(self.width // 2 - 350, self.height // 2, image_start, self.start)

        image_exit = pygame.image.load('img/exit_btn.png')
        self.exit_button = Button(self.width // 2 + 150, self.height // 2 , image_exit, self.exit)
        # ===================================================================================================== 

        pygame.display.set_caption('Platformer')
        self.screen = pygame.display.set_mode((self.width, self.height))

    def run(self):
        img_sun = pygame.image.load('img/sun.png')
        img_bkg = pygame.image.load('img/sky.png')

        while self.game_state != GameState.EXIT:
            # Maintain a constant FPS
            self.clock.tick(self.fps)

            # Draw background
            self.screen.blit(img_bkg, (0, 0))
            self.screen.blit(img_sun, (100, 100))

            # Run the code
            if self.game_state == GameState.PLAYING:
                self.world.update()

                is_alive = self.player.update(self.world.tile_list, self.world.enemies_list, self.world.exit_list, self.world.coin_list)
                if not is_alive:
                    self.game_state = GameState.GAME_OVER

                self.world.draw(self.screen)
                self.player.draw(self.screen)

            # Show the restart menu
            elif self.game_state == GameState.GAME_OVER:
                self.world.draw(self.screen)
                self.player.draw(self.screen)

                self.player.update_death()
                self.restart_button.update()
                self.restart_button.draw(self.screen)

                draw_text(self.screen, f"Score: {self.score}", 0, 0)

            elif self.game_state == GameState.START:
                self.start_button.update()
                self.start_button.draw(self.screen)

                self.exit_button.update()
                self.exit_button.draw(self.screen)

            # Habdle quit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # Update the display
            pygame.display.update()

    def on_die(self):
        self.game_state = GameState.GAME_OVER

    def reset(self):
        self.game_state = GameState.PLAYING
        self.score = 0

        self.world = self.levels[self.current_level].load_world(self.tile_size)
        self.player.reset(100, self.height - 130)

        self.player.reset(100, self.height - 130)
    
    def start(self):
        self.game_state = GameState.PLAYING

    def exit(self):
        self.game_state = GameState.EXIT

    def next_level(self):
        # TODO: check if the last level has been reached

        self.current_level += 1
        self.world = self.levels[self.current_level].load_world(self.tile_size)
        self.player.reset(100, self.height - 130)

    def add_to_score(self, amount):
        self.score += amount

    def __del__(self):
        pygame.quit()
