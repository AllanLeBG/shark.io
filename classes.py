import pygame

class Bonus(pygame.sprite.Sprite):
    def __init__(self, x, y, image, valeur, vitesse, largeur, hauteur):
        super().__init__()
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (largeur, hauteur))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.valeur = valeur
        self.vitesse = vitesse
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= self.vitesse
        if self.rect.right < 0:
            self.kill()

class Oiseau(Bonus):
    def __init__(self, x, y, vitesse=3):
        super().__init__(
            x, y, "image/pelican.png",
            10, vitesse, 80, 80
        )

class Nageur(Bonus):
    def __init__(self, x, y, vitesse=1):
        super().__init__(
            x, y, "image/plongeur1.png",
            20, vitesse, 100, 100
        )

class MurInvisible:
    def __init__(self, left, right, top, bottom):
        self.rect = pygame.Rect(left, top, right - left, bottom - top)

    def verifier_collision(self, personnage):
        if self.rect.colliderect(personnage.rect):
            if personnage.rect.left < self.rect.left:
                personnage.rect.left = self.rect.left
            if personnage.rect.right > self.rect.right:
                personnage.rect.right = self.rect.right
            if personnage.rect.top < self.rect.top:
                personnage.rect.top = self.rect.top
            if personnage.rect.bottom > self.rect.bottom:
                personnage.rect.bottom = self.rect.bottom
