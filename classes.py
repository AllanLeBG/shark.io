class Bonus(pygame.sprite.Sprite):
    def __init__(self, x, y, image, valeur, vitesse, largeur, hauteur):
        super().__init__()
        self.apparence = pygame.image.load(image)
        self.apparence = pygame.transform.scale(self.apparence, (largeur, hauteur))
        self.position = self.apparence.get_rect(topleft=(x, y))
        self.valeur = valeur
        self.vitesse = vitesse
        self.masque = pygame.mask.from_surface(self.apparence)

    def actualiser(self):
        self.position.x -= self.vitesse
        if self.position.right < 0:
            self.kill()  # Supprime l'objet s'il sort de l'écran

class Oiseau(Bonus):
    def __init__(self, x, y, vitesse=2):
        super().__init__(
            x, y, "assets/seagull.png",
            10, vitesse, 40, 40
        )

class Nageur(Bonus):
    def __init__(self, x, y, vitesse=1):
        super().__init__(
            x, y, "assets/human.png",
            20, vitesse, 50, 50
        )
