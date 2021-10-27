import pygame

def draw_text(screen, text, x, y):
    font = pygame.font.SysFont('FiraMono', 30)
    img = font.render(text, True, (255, 255, 255))
    screen.blit(img, (x, y))

