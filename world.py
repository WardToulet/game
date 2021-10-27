import pygame
from pygame.locals import *

from entities import Enemy, Lava

class World:
    def __init__(self, data, tile_size):
        self.tile_list = []
        self.entity_list = pygame.sprite.Group()

        # Load the images
        self.images = list(map(lambda name: pygame.image.load(f"img/{name}.png"), ["dirt", "grass"]))

        # Loop through all the datapoints on the grid and add the to the world
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                ## 1 and 2 or grass and dirt blocks
                if tile in range(1, 3):
                    self.add_tile(tile, x, y, tile_size)

                ## Blob enemies
                elif tile == 3:
                    blob = Enemy(x * tile_size, y * tile_size + 15)
                    self.entity_list.add(blob)

                ## Lava entities
                elif tile == 6:
                    lava = Lava(x * tile_size, (y + 0.5) * tile_size, tile_size)
                    self.entity_list.add(lava)

    def update(self):
        self.entity_list.update()

    def draw(self, screen):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)

        self.entity_list.draw(screen)

    def add_tile(self, kind, x, y, tile_size):
        image = pygame.transform.scale(self.images[kind - 1], (tile_size, tile_size))
        rect = image.get_rect().move(x * tile_size, y * tile_size)
        self.tile_list.append((image, rect))
