import pygame


class Player:
    def __init__(self, coords, image, desc):
        self.coords = coords
        self.image = image
        self.attackDamage = 10
        self.strength = 0
        self.agility = 0
        self.intelligent = 0
        self.defense = 0
        self.hp = 100 + self.strength * 10
        self.mana = self.intelligent * 10

    def return_coords(self):
        return self.coords

    def return_image(self):
        return self.image

    def set_coords(self, coords):
        self.coords = coords

    def attack(self, tzel):
        tzel.hp -= self.attackDamage

    def updateAtributs(self, strength, agility, intelligent, defense, attack):
        self.hp += strength * 10 - self.strength * 10
        self.strength = strength
        self.agility = agility
        self.mana += intelligent * 10 - self.intelligent * 10
        self.intelligent = intelligent
        self.attackDamage = 10 + attack
        self.defense = defense


class PlayerSprites(pygame.sprite.Sprite):
    def __init__(self, group, image, coords):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]

    def update(self, dir):
        if dir == "up":
            self.rect.y -= 40
        if dir == "down":
            self.rect.y += 40
        if dir == "right":
            self.rect.x += 40
        if dir == "left":
            self.rect.x -= 40
