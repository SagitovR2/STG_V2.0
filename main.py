import pygame
from mainGameBoard import mainGameBoard
from PyQt5.QtWidgets import QApplication
from Menu import FormStarting, Registration
import names
import sys
import sqlite3


pygame.init()
NEWENEMYCREATE = pygame.USEREVENT + 1
ENEMYMOVE = pygame.USEREVENT + 2
DELHEROATTACK = pygame.USEREVENT + 3
DELENEMYATTACK = pygame.USEREVENT + 4
CREATEITEM = pygame.USEREVENT + 5
pygame.time.set_timer(NEWENEMYCREATE, 10000)
pygame.time.set_timer(ENEMYMOVE, 2000)
pygame.time.set_timer(DELHEROATTACK, 500)
pygame.time.set_timer(DELENEMYATTACK, 1500)
pygame.time.set_timer(CREATEITEM, 20000)
size = width, height = 1280, 720
clock = pygame.time.Clock()
fps = 60
screen = pygame.display.set_mode(size)
running = True
screen.fill((0, 0, 0))
pygame.display.flip()
mgb = mainGameBoard(32, 18, 5, "grass_top.png", "charecter.png", "enemyImage.png", screen)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                mgb.pause = not mgb.pause
            if event.key == pygame.K_l and not mgb.hasInventory:
                screen = mgb.log()
            if event.key == pygame.K_i and not mgb.hasLog:
                screen = mgb.showInventory()
            if event.key == pygame.K_1 and mgb.hasInventory:
                mgb.showInfoAbout("head")
            if event.key == pygame.K_2 and mgb.hasInventory:
                mgb.showInfoAbout("body")
            if event.key == pygame.K_3 and mgb.hasInventory:
                mgb.showInfoAbout("arms")
            if event.key == pygame.K_4 and mgb.hasInventory:
                mgb.showInfoAbout("foot")
            if event.key == pygame.K_5 and mgb.hasInventory:
                mgb.showInfoAbout("weapon")
            if event.key == pygame.K_6 and mgb.hasInventory:
                mgb.showInfoAbout("shild")
            if event.key == pygame.K_m and mgb.hasLog:
                mgb.showInfoAbout("shild")
        if not mgb.pause:
            if event.type == CREATEITEM:
                mgb.randomItemInRandomPlace()
            if event.type == NEWENEMYCREATE or len(mgb.enemys) == 0:
                if len(mgb.enemys) < 10:
                    mgb.moreEnemys()
            if event.type == ENEMYMOVE:
                mgb.moveToHeroAndAttack()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT and names.game \
                    and mgb.attack_coords == (0, 0):
                mgb.get_click(event.pos)
            if event.type == DELHEROATTACK:
                mgb.del_attack()
            if event.type == DELENEMYATTACK:
                mgb.delEnemyAttack()
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
        screen.fill((0, 0, 0), (0, 0, width, height))
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
