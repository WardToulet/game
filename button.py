import pygame
from pygame.locals import *

class Button():
    def __init__(self, x, y, image, on_click):
        self.image = image
        self.rect = self.image.get_rect().move(x, y)
        self.on_click = on_click

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.on_click()
