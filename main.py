import pygame
from Board import Board

pygame.init()
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()