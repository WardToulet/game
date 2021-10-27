import pygame
from pygame.locals import *

from player import Player
from world import World

class Game:
    def __init__(self, width, height, tile_size, world, fps=60, name="Game"):
        pygame.init()

        self.width = width
        self.height = height

        self.fps = fps

        self.player = Player(100, self.height - 130)
        self.world = world
        self.clock = pygame.time.Clock()

        pygame.display.set_caption('Platformer')
        self.screen = pygame.display.set_mode((self.width, self.height))

    def run(self):
        img_sun = pygame.image.load('img/sun.png')
        img_bkg = pygame.image.load('img/sky.png')

        game_over = 0

        while True:
            self.screen.blit(img_bkg, (0, 0))
            self.screen.blit(img_sun, (100, 100))

            self.world.update()
            self.world.draw(self.screen)

            game_over = self.player.update(self.world.tile_list, self.world.entity_list, game_over)
            self.player.draw(self.screen, game_over)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            pygame.display.update()
            self.clock.tick(self.fps)

    def __del__(self):
        pygame.quit()
