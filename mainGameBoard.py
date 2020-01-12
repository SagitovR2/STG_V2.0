import pygame
from Board import Board
from LoadImage import load_image
from backImageSprites import BackImage
import random
from Player import Player, PlayerSprites
from Enemys import Enemy, EnemySprites
import names
import sqlite3


class mainGameBoard(Board):
    def __init__(self, width, height, enemyCount, backImage, playerImage, enemyImage):
        super().__init__(width, height)
        self.attack_coords = (0, 0)
        self.enemyCount = enemyCount
        self.backImage = load_image(backImage, -1)
        playerImage = load_image(playerImage, -1)
        self.backSprites = pygame.sprite.Group()
        self.playerSprites = pygame.sprite.Group()
        self.EnemySprites = pygame.sprite.Group()
        self.EnemyImage = load_image(enemyImage)
        self.enemys = []
        self.attack_dir = ""
        self.con = sqlite3.connect('database/database.db')
        self.cur = self.con.cursor()
        self.player_coords = list(self.cur.execute(
            "SELECT position FROM players WHERE login = '{log}'".format(log=names.player_login)
        ))[0][0].split()
        self.player = Player((int(self.player_coords[0]), int(self.player_coords[1])), playerImage, "")
        self.board[self.player.return_coords()[0]][self.player.return_coords()[1]] = 1
        self.EnemySpr = []
        for i in range(enemyCount):
            x = random.randint(0, 31)
            y = random.randint(0, 17)
            while self.board[x][y] != -1:
                x = random.randint(0, 31)
                y = random.randint(0, 17)
            enemy = Enemy((x, y), self.EnemyImage, "")
            self.enemys.append(enemy)
            self.EnemySpr.append(EnemySprites(self.EnemySprites, enemy.return_image(),
                                           (enemy.coords[0] * 40, enemy.coords[1] * 40)))
            self.board[x][y] = 2
        self.playerSpr = PlayerSprites(self.playerSprites, self.player.return_image(),
                                       (self.player.coords[0] * 40, self.player.coords[1] * 40))
        self.blade_left = load_image("blade_left.png", -1)
        self.blade_right = load_image("blade_right.png", -1)
        self.blade_down = load_image("blade_down.png", -1)
        self.blade_up = load_image("blade_up.png", -1)
        for row in range(self.height):
            for col in range(self.width):
                rect = pygame.Rect(
                    self.left + self.cell_size * col,
                    self.top + self.cell_size * row,
                    self.cell_size, self.cell_size
                )
                BackImage(self.backSprites, self.backImage, rect)

    def updateEnemys(self):
        for i in self.enemys:
            if i.hp <= 0:
                for j in self.EnemySprites:
                    if i.coords[0] * 40 == j.rect.x and i.coords[1] * 40 == j.rect.y:
                        self.EnemySprites.remove(j)
                        break
                self.enemys.remove(i)
                self.board[i.coords[0]][i.coords[1]] = -1

    def render(self, screen):
        self.backSprites.draw(screen)
        self.playerSprites.draw(screen)
        self.EnemySprites.draw(screen)
        for row in range(self.height):
            for col in range(self.width):
                rect = pygame.Rect(
                    self.left + self.cell_size * col,
                    self.top + self.cell_size * row,
                    self.cell_size, self.cell_size
                )
                pygame.draw.rect(screen, self.color, rect, 1)
                if self.board[col][row] == -5 or self.board[col][row] == 10:
                    screen.blit(self.blade_left, (col * 40, row * 40))
                if self.board[col][row] == -6 or self.board[col][row] == 12:
                    screen.blit(self.blade_down, (col * 40, row * 40))
                if self.board[col][row] == -7 or self.board[col][row] == 14:
                    screen.blit(self.blade_right, (col * 40, row * 40))
                if self.board[col][row] == -8 or self.board[col][row] == 16:
                    screen.blit(self.blade_up, (col * 40, row * 40))

    def on_click(self, cell_coords):
        if cell_coords[0] == self.player.coords[0] - 1 and cell_coords[1] == self.player.coords[1]:
            if self.board[self.player.coords[0] - 1][self.player.coords[1]] == -1 or\
                    self.board[self.player.coords[0] - 1][self.player.coords[1]] == 2:
                self.board[self.player.coords[0] - 1][self.player.coords[1]] *= 5
                self.attack_coords = (self.player.coords[0] - 1, self.player.coords[1])
                self.attack_dir = "left"
        elif cell_coords[0] == self.player.coords[0] + 1 and cell_coords[1] == self.player.coords[1]:
            if self.board[self.player.coords[0] + 1][self.player.coords[1]] == -1 or\
                    self.board[self.player.coords[0] + 1][self.player.coords[1]] == 2:
                self.board[self.player.coords[0] + 1][self.player.coords[1]] *= 7
                self.attack_coords = (self.player.coords[0] + 1, self.player.coords[1])
                self.attack_dir = "right"
        elif - 1 <= self.player.coords[0] - cell_coords[0] <= 1:
            if self.player.coords[1] > cell_coords[1]:
                if self.board[self.player.coords[0]][self.player.coords[1] - 1] == -1 or \
                        self.board[self.player.coords[0]][self.player.coords[1] - 1] == 2:
                    self.board[self.player.coords[0]][self.player.coords[1] - 1] *= 8
                    self.attack_coords = (self.player.coords[0], self.player.coords[1] - 1)
                    self.attack_dir = "up"
            if self.player.coords[1] < cell_coords[1]:
                if self.board[self.player.coords[0]][self.player.coords[1] + 1] == -1 or \
                        self.board[self.player.coords[0]][self.player.coords[1] + 1] == 2:
                    self.board[self.player.coords[0]][self.player.coords[1] + 1] *= 6
                    self.attack_coords = (self.player.coords[0], self.player.coords[1] + 1)
                    self.attack_dir = "down"
        elif - 1 <= self.player.coords[1] - cell_coords[1] <= 1:
            if self.player.coords[0] > cell_coords[0]:
                if self.board[self.player.coords[0] - 1][self.player.coords[1]] == -1 or \
                        self.board[self.player.coords[0] - 1][self.player.coords[1]] == 2:
                    self.board[self.player.coords[0] - 1][self.player.coords[1]] *= 5
                    self.attack_coords = (self.player.coords[0] - 1, self.player.coords[1])
                    self.attack_dir = "left"
            if self.player.coords[0] < cell_coords[0]:
                if self.board[self.player.coords[0] + 1][self.player.coords[1]] == -1 or \
                        self.board[self.player.coords[0] + 1][self.player.coords[1]] == 2:
                    self.board[self.player.coords[0] + 1][self.player.coords[1]] *= 7
                    self.attack_coords = (self.player.coords[0] + 1, self.player.coords[1])
                    self.attack_dir = "right"
        if self.board[self.attack_coords[0]][self.attack_coords[1]] > 0:
            for i in self.enemys:
                if i .coords == self.attack_coords:
                    self.player.attack(i)
            self.updateEnemys()

    def del_attack(self):
        if self.board[self.attack_coords[0]][self.attack_coords[1]] < 0:
            self.board[self.attack_coords[0]][self.attack_coords[1]] = -1
        else:
            if self.attack_dir == "left":
                self.board[self.attack_coords[0]][self.attack_coords[1]] /= 5
            if self.attack_dir == "right":
                self.board[self.attack_coords[0]][self.attack_coords[1]] /= 7
            if self.attack_dir == "down":
                self.board[self.attack_coords[0]][self.attack_coords[1]] /= 6
            if self.attack_dir == "up":
                self.board[self.attack_coords[0]][self.attack_coords[1]] /= 8
        self.attack_dir = ""
        self.attack_coords = (0, 0)

    def go(self, dir):
        if dir == "up":
            if self.player.coords[1] != 0:
                if self.board[self.player.coords[0]][self.player.coords[1] - 1] == -1:
                    self.board[self.player.coords[0]][self.player.coords[1] - 1] = 1
                    self.board[self.player.coords[0]][self.player.coords[1]] = -1
                    self.player.coords = (self.player.coords[0], self.player.coords[1] - 1)
                    self.playerSpr.update("up")
        if dir == "down":
            if self.player.coords[1] + 1 != self.height:
                if self.board[self.player.coords[0]][self.player.coords[1] + 1] == -1:
                    self.board[self.player.coords[0]][self.player.coords[1] + 1] = 1
                    self.board[self.player.coords[0]][self.player.coords[1]] = -1
                    self.player.coords = (self.player.coords[0], self.player.coords[1] + 1)
                    self.playerSpr.update("down")
        if dir == "right":
            if self.player.coords[0] + 1 != self.width:
                if self.board[self.player.coords[0] + 1][self.player.coords[1]] == -1:
                    self.board[self.player.coords[0] + 1][self.player.coords[1]] = 1
                    self.board[self.player.coords[0]][self.player.coords[1]] = -1
                    self.player.coords = (self.player.coords[0] + 1, self.player.coords[1])
                    self.playerSpr.update("right")
        if dir == "left":
            if self.player.coords[0] != 0:
                if self.board[self.player.coords[0] - 1][self.player.coords[1]] == -1:
                    self.board[self.player.coords[0] - 1][self.player.coords[1]] = 1
                    self.board[self.player.coords[0]][self.player.coords[1]] = -1
                    self.player.coords = (self.player.coords[0] - 1, self.player.coords[1])
                    self.playerSpr.update("left")
        names.player_coords = self.player.return_coords()
