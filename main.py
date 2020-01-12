import pygame
from mainGameBoard import mainGameBoard
from PyQt5.QtWidgets import QApplication
from Menu import FormStarting, Registration
import names
import sys
import sqlite3


pygame.init()
size = width, height = 1280, 720
clock = pygame.time.Clock()
fps = 60
screen = pygame.display.set_mode(size)
running = True
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
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT and names.game \
                and mgb.attack_coords == (0, 0):
            mgb.get_click(event.pos)
            c = 0
        if event.type == pygame.KEYDOWN and names.game:
            if event.key == pygame.K_w:
                mgb.go("up")
            if event.key == pygame.K_s:
                mgb.go("down")
            if event.key == pygame.K_d:
                mgb.go("right")
            if event.key == pygame.K_a:
                mgb.go("left")
    if names.menu:
        app = QApplication(sys.argv)
        form_menu = FormStarting()
        form_menu.show()
    if names.game:
        screen.fill((0, 0, 0))
        mgb.render(screen)
    pygame.display.flip()
    clock.tick(fps)
con = sqlite3.connect('database/database.db')
cur = con.cursor()
cur.execute(
    'UPDATE players SET position = "{cor}" WHERE login = "{log}"'.format(
        cor=str(names.player_coords[0]) + ' ' + str(names.player_coords[1]), log=names.player_login
    )
)
con.commit()
names.game = False
names.menu = True
pygame.quit()
