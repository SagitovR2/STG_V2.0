import pygame


class Enemy:
    def __init__(self, coords, image, desc):
        self.coords = coords
        self.image = image
        self.hp = 50
        self.attackDamage = 10
        self.defense = 0

    def return_coords(self):
        return self.coords

    def return_image(self):
        return self.image

    def set_coords(self, coords):
        self.coords = coords

    def attack(self, tzel):
        tzel.hp = min(tzel.hp - self.attackDamage, tzel.hp - 1)


class EnemySprites(pygame.sprite.Sprite):
    def __init__(self, group, image, coords):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]

    def update(self, *args):
        dir = args[0]
        if dir == "up":
            self.rect.y -= 40
        elif dir == "down":
            self.rect.y += 40
        elif dir == "right":
            self.rect.x += 40
        elif dir == "left":
            self.rect.x -= 40
