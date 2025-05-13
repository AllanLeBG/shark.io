import pygame
pygame.init()

class Piece:
    def __init__(self, image, pos):
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)


class TueurRequin:
    def __init__(self, image, pos, vitesse=3):
        self.vitesse = vitesse
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = 1

    def deplacer(self, screen_width):
        self.rect.x += self.vitesse * self.direction
        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.direction *= -1




class Surfeur:
    def __init__(self, image, pos, vitesse=5):
        self.vitesse = vitesse
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = 1

    def deplacer(self, screen_width):
        self.rect.x += self.vitesse * self.direction
        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.direction *= -1

class Requin:
    def __init__(self, image, pos, speed):
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = speed
        self.en_saut = False
        self.speed_y = 0
        self.gravite = 0.4

    def deplacer(self, keys, screen_width, screen_height, water_height):
        in_water = self.rect.top >= screen_height - water_height
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.image = pygame.transform.scale(pygame.image.load('image/requin2gauche.png').convert_alpha(), (200, 200))

        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
            self.image = pygame.transform.scale(pygame.image.load('image/requin2.png').convert_alpha(), (200, 200))
        if keys[pygame.K_UP] and in_water:
            self.rect.y -= self.speed
            self.image = pygame.transform.scale(pygame.image.load('image/requin2haut.png').convert_alpha(),(200, 200))
        if keys[pygame.K_DOWN] and self.rect.bottom < screen_height and in_water:
            self.rect.y += self.speed
            self.image = pygame.transform.scale(pygame.image.load('image/requin2bas.png').convert_alpha(),(200, 200))
        if keys[pygame.K_SPACE] and not self.en_saut:
            self.en_saut = True
            self.image = pygame.transform.scale(pygame.image.load('image/requin2haut.png').convert_alpha(),(200, 200))
            self.speed_y = -12 if in_water else -8

        if self.en_saut:
            self.speed_y += self.gravite if not in_water else self.gravite / 2
            self.rect.y += self.speed_y
            if self.rect.top >= screen_height - water_height:
                self.rect.top = screen_height - water_height
                self.speed_y = 0
                self.en_saut = False
