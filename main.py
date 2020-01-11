import pygame
from mainGameBoard import mainGameBoard


pygame.init()
size = width, height = 1280, 720
clock = pygame.time.Clock()
fps = 60
screen = pygame.display.set_mode(size)
running = True
menu = True
game = False
screen.fill((0, 0, 0))
pygame.display.flip()
mgb = mainGameBoard(32, 18, 5, "grass_top.png", "charecter.png", "enemyImage.png")
c = 0
while running:
    c += 1
    if c == 3:
        mgb.del_attack()
        c = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT and game \
                and mgb.attack_coords == (0, 0):
            mgb.get_click(event.pos)
            c = 0
        if event.type == pygame.KEYDOWN and game:
            if event.key == pygame.K_w:
                mgb.go("up")
            if event.key == pygame.K_s:
                mgb.go("down")
            if event.key == pygame.K_d:
                mgb.go("right")
            if event.key == pygame.K_a:
                mgb.go("left")
    if menu:
        menu = False
        game = True
    if game:
        screen.fill((0, 0, 0))
        mgb.render(screen)
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
