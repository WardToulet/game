import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 1000
tile_size = 50

game_over = 0

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Platformer')

# Load images
img_sun = pygame.image.load('img/sun.png')
img_bkg = pygame.image.load('img/sky.png')

class World:
    def __init__(self, data):
        self.tile_list = []

        # load images
        img_dirt = pygame.image.load('img/dirt.png')
        img_grass = pygame.image.load('img/grass.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(img_dirt, (tile_size, tile_size))
                    rect = img.get_rect()
                    rect.x = col_count * tile_size
                    rect.y = row_count * tile_size
                    tile = (img, rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(img_grass, (tile_size, tile_size))
                    rect = img.get_rect()
                    rect.x = col_count * tile_size
                    rect.y = row_count * tile_size
                    tile = (img, rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    blob = Enemy(col_count * tile_size, row_count * tile_size + 15)
                    blob_group.add(blob)
                if tile == 6:
                    lava = Lava(col_count * tile_size, (row_count + 0.5) * tile_size)
                    lava_group.add(lava)


                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/blob.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('img/lava.png')
        self.image = pygame.transform.scale(image, (tile_size, tile_size/2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player:
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0

        for num in range(1, 5):
            img_right = pygame.image.load(f'img/guy{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False) 
            self.images_right.append(img_right)
            self.images_left.append(img_left)

        self.death_image = pygame.image.load('img/ghost.png')

        self.image = self.images_right[self.index] 
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width
        self.height = self.image.get_height
        self.vel_y = 0
        self.jumped = False
        self.direction = 0

    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 5

        if game_over == 0:
            # input
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and not self.jumped:
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
            for tile in world.tile_list:
                x_rect = self.rect.move(dx, 0)
                if tile[1].colliderect(x_rect):
                    dx = 0

                y_rect = self.rect.move(0, dy)
                if tile[1].colliderect(y_rect):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                    if self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0

            # enemy collision
            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1

            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1

            # update
            self.rect.x += dx
            self.rect.y += dy
        elif game_over == -1:
            if self.rect.y > 200:
                self.rect.y -= 5
        return game_over

    def draw(self, game_over):
        if game_over == 0:
            screen.blit(self.image, self.rect)
        else:
            screen.blit(self.death_image, self.rect)

        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)


world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1], 
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1], 
[1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1], 
[1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

player = Player(100, screen_height - 130)

blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()

world = World(world_data)

run = True
while run:
    clock.tick(fps)

    screen.blit(img_bkg, (0, 0))
    screen.blit(img_sun, (100, 100))

    world.draw()

    if game_over == 0:
        blob_group.update()

    blob_group.draw(screen)
    lava_group.draw(screen)

    game_over = player.update(game_over)
    player.draw(game_over)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
