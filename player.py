import pygame
from pygame.locals import *

class Player:
    def __init__(self, x, y, on_die, on_exit):
        self.on_die = on_die
        self.on_exit = on_exit

        self.reset(x, y)

    def reset(self, x, y):
        self.images_right = list(map(lambda i: pygame.transform.scale(pygame.image.load(f'img/guy{i}.png'), (40, 80)), range(1, 5)))
        self.images_left = list(map(lambda r: pygame.transform.flip(r, True, False), self.images_right))
        self.death_image = pygame.image.load('img/ghost.png')

        self.index = 0
        self.counter = 0

        # Set the starting image
        self.image = self.images_right[self.index] 

        # Set the rect/bouding box
        self.rect = self.image.get_rect().move(x, y)
        self.width = self.image.get_width
        self.height = self.image.get_height

        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = False

    def update(self, tile_list, entity_list, exit_list):
        dx = 0
        dy = 0
        walk_cooldown = 5

        # input
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and not self.jumped and not self.in_air:
            self.vel_y = -15
            self.jumped = True
        if not key[pygame.K_SPACE]:
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 5
            self.counter += 1
            self.direction = -1
        if key[pygame.K_RIGHT]:
            dx += 5
            self.counter += 1
            self.direction = 1
        if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
            self.counter = 0
            self.index = 0
            self.image = self.images_right[self.index]
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]

        # animation
        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0

            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]


        # gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10

        # Apply velocity
        dy += self.vel_y

        # collsision
        self.in_air = True
        for tile in tile_list:
            x_rect = self.rect.move(dx, 0)
            if tile[1].colliderect(x_rect):
                dx = 0

            y_rect = self.rect.move(0, dy)
            if tile[1].colliderect(y_rect):
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                if self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.in_air = False
                    self.vel_y = 0

        # enemy collision if collided with an enmy return false
        if pygame.sprite.spritecollide(self, entity_list, False):
            self.on_die()

        if pygame.sprite.spritecollide(self, exit_list, False):
            self.on_exit()

        # update
        self.rect.x += dx
        self.rect.y += dy

        return True

    def update_death(self):
        self.image = self.death_image
        if self.rect.y > 200:
            self.rect.y -= 5

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
