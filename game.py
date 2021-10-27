import pygame
from pygame.locals import *

from enum import Enum

from player import Player
from world import World
from button import Button

class GameState(Enum):
    PLAYING = 1
    GAME_OVER = 0

class Game:
    def __init__(self, width, height, tile_size, world, fps=60, name="Game"):
        pygame.init()

        self.width = width
        self.height = height

        self.fps = fps

        self.game_state = GameState.PLAYING

        self.player = Player(100, self.height - 130)
        self.world = world
        self.clock = pygame.time.Clock()

        # FIXME: move to proper location
        image_restart = pygame.image.load('img/restart_btn.png')
        self.restart_button = Button(self.width // 2 - 50, self.height // 2 + 100, image_restart, self.reset)

        pygame.display.set_caption('Platformer')
        self.screen = pygame.display.set_mode((self.width, self.height))

    def run(self):
        img_sun = pygame.image.load('img/sun.png')
        img_bkg = pygame.image.load('img/sky.png')

        while True:
            # Maintain a constant FPS
            self.clock.tick(self.fps)

            # Run the code
            if self.game_state == GameState.PLAYING:
                self.world.update()

                is_alive = self.player.update(self.world.tile_list, self.world.entity_list)
                if not is_alive:
                    self.game_state = GameState.GAME_OVER

            # Habdle quit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # Draw background
            self.screen.blit(img_bkg, (0, 0))
            self.screen.blit(img_sun, (100, 100))

            # Draw the world and the player
            self.world.draw(self.screen)
            self.player.draw(self.screen)

            # Show the restart menu
            if self.game_state == GameState.GAME_OVER:
                self.player.update_death()
                self.restart_button.update()
                self.restart_button.draw(self.screen)

            # Update the display
            pygame.display.update()

    def reset(self):
        self.game_state = GameState.PLAYING
        self.player.reset(100, self.height - 130)

    def __del__(self):
        pygame.quit()
