import pygame

# Classe obstacles
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()  # à custom
        self.rect.topleft = (x, y)

    def dessiner(self, screen, camera_offset_x):
        #Dessiner l'obstacle ?
        screen.blit(self.image, (self.rect.x - camera_offset_x, self.rect.y))

# Classe Rochers (statique, bloquent le joueur)
class Roche(Obstacle):
    def __init__(self, x, screen_height):
        super().__init__(x, screen_height * 2 // 3 + 30, 50, 50, "rock.png")  # Position dans l'eau

# Classe Avions (mobiles et font dégâts)
class Avion(Obstacle):
    def __init__(self, x, screen_height, speed):
        super().__init__(x, screen_height // 3 - 50, 80, 40, "plane.png")  # Position dans l'air
        self.speed = speed  

    def update(self):
        self.rect.x += self.speed  
        if self.rect.right < 0:  # S'il sort de l'écran à gauche, il réapparaît à droite?? possible changement
            self.rect.left = 800  


# mettre dans un file logique mouvement du requin pour le bloquage :
def check_collisions(shark, obstacles, score):
    for obstacle in obstacles:

        # Collision avec un rocher
        if isinstance(obstacle, Roche):  
            if shark.rect.colliderect(obstacle.rect):
                # Empêcher de traverser
                if shark.rect.right > obstacle.rect.left:
                    shark.rect.right = obstacle.rect.left
                if shark.rect.left < obstacle.rect.right:
                    shark.rect.left = obstacle.rect.right

        # Collision avec un avion
        elif isinstance(obstacle, Avion):  
            if shark.rect.colliderect(obstacle.rect):
                score -= 1  # VERIFIER SCORE
                shark.rect.y = 300  # Le requin redescend??
    return score
