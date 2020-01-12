import pygame
from mainGameBoard import mainGameBoard


pygame.init()
NEWENEMYCREATE = pygame.USEREVENT + 1
ENEMYMOVE = pygame.USEREVENT + 2
DELHEROATTACK = pygame.USEREVENT + 3
DELENEMYATTACK = pygame.USEREVENT + 4
pygame.time.set_timer(NEWENEMYCREATE, 10000)
pygame.time.set_timer(ENEMYMOVE, 2000)
pygame.time.set_timer(DELHEROATTACK, 500)
pygame.time.set_timer(DELENEMYATTACK, 1500)
size = width, height = 1280, 720
clock = pygame.time.Clock()
fps = 60
screen = pygame.display.set_mode(size)
running = True
menu = True
game = False
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
            if event.key == pygame.K_l:
                screen = mgb.log()
            if event.key == pygame.K_i:
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
            if event.type == NEWENEMYCREATE or len(mgb.enemys) == 0:
                if len(mgb.enemys) < 10:
                    mgb.moreEnemys()
            if event.type == ENEMYMOVE:
                mgb.moveToHeroAndAttack()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT and game \
                    and mgb.attack_coords == (0, 0):
                mgb.get_click(event.pos)
            if event.type == DELHEROATTACK:
                mgb.del_attack()
            if event.type == DELENEMYATTACK:
                mgb.delEnemyAttack()
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
        screen.fill((0, 0, 0), (0, 0, width, height))
        mgb.render(screen)
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
