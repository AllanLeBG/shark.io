import pygame
import random

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, width, height):
        super().__init__()   #classe parente
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)  # Pour collisions précises

    def update(self, *args):
        pass  # À surcharger pour les objets mobiles

    def draw(self, screen, camera_offset=0):
        screen.blit(self.image, (self.rect.x - camera_offset, self.rect.y))

class Roche(Obstacle):
    def __init__(self, x, screen_height):
        super().__init__(
            x, screen_height * 2 // 3 + 20, 
            "assets/rock.png", 60, 60
        )

class Avion(Obstacle):
    def __init__(self, x, screen_height, speed=3):
        super().__init__(x, screen_height // 4, "assets/plane.png", 80, 40)
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.left = pygame.display.get_surface().get_width()

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, points, speed, width, height):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.points = points
        self.speed = speed
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()  # Supprime l'objet s'il sort de l'écran

class Mouette(Collectible):
    def __init__(self, x, y, speed=2):
        super().__init__(
            x, y, "assets/seagull.png", 
            10, speed, 40, 40
        )

class Humain(Collectible):
    def __init__(self, x, y, speed=1):
        super().__init__(
            x, y, "assets/human.png", 
            20, speed, 50, 50
        )