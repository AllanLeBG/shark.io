import pygame
import sys
import math

# Initialisation de Pygame
  # Removed redundant import
import os  # Gestion des fichiers
  # Removed redundant import
pygame.init()




# Définir les dimensions de la fenêtre en plein écran
screen_width, screen_height = 1280, 720  # These dimensions are now used for background_image scaling
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Deux personnages qui marchent avec des vagues améliorées")
piece_image = None  # Placeholder for future use (if needed)
# Définir la couleur de l'eau
water_color = (0, 0, 255)  # Bleu
water_height = pygame.display.Info().current_h // 2
class Piece:
    def __init__(self, image, pos):
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)


class Surfeur:
    def __init__(self, image, pos, vitesse=1.5):  # Reduced the speed of surfers
        self.vitesse = vitesse
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
  # Removed duplicate assignment
        self.direction = 1  # Initializes direction for horizontal movement

    def deplacer(self, screen_width):
        if not hasattr(self, 'rect') or self.rect is None:
            raise AttributeError("Surfeur instance has no attribute 'rect'. Ensure it is initialized correctly.")
        self.rect.x += self.vitesse * self.direction
        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.direction *= -1  # Reverse direction on collision
class Personnage:
    def __init__(self, image, start_pos):
        self.speed = 3  # Increased readability
        self.vitesse_y = 0
        self.en_saut = False
        self.gravite = 0.1  # Adjusted gravity for smoother movement
        self.live = True

    def deplacer(self, touches, keys, screen_width, screen_height):

        #Dans l'eau
        if self.rect.top > screen_height - water_height:
            if keys[touches['left']] and self.rect.left > 0:
                self.rect.x -= self.speed
            if keys[touches['right']] and self.rect.right < screen_width * 2:
                self.rect.x += self.speed
            if keys[touches['up']]:
                self.rect.y -= self.speed
            if keys[touches['down']] and self.rect.bottom < screen_height:
                self.rect.y += self.speed


        #Sortie de l'eau 01
        elif self.rect.top <= screen_height - water_height:

            if keys[touches['left']] and self.rect.left > 0:
                self.rect.x -= self.speed
            if keys[touches['right']] and self.rect.right < screen_width * 2:  # Limite sur la droite augmentée
                self.rect.x += self.speed

            if keys[touches['down']] and self.rect.bottom < screen_height:  # Limite en hauteur augmentée
                self.rect.y += self.speed

            if keys[touches['space']] and not self.en_saut:
                self.vitesse_y = -10
                self.en_saut = True

            if self.en_saut:
                self.vitesse_y += self.gravite
                self.rect.y += self.vitesse_y


                if keys[touches['left']] and self.rect.left > 0:
                    self.rect.x -= self.speed
                if keys[touches['right']] and self.rect.right < screen_width * 2:
                    self.rect.x += self.speed

                #Fin du saut : quand on touche l'eau
                if self.rect.top >= screen_height - water_height:
                    self.rect.top = screen_height * 2 // 3
                    self.vitesse_y = 0
                    self.en_saut = False



    def dessiner(self, screen):

        screen.blit(self.image, self.rect.topleft)





class Requin:
    def __init__(self, image, pos, speed):
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)  # Fixed indentation for proper initialization
        self.speed = speed
        self.en_saut = False
        self.speed_y = 0
        self.gravite = 0.5

    def deplacer(self, keys, screen_width, screen_height, water_height):
        in_water = self.rect.top >= screen_height - water_height
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and in_water:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < screen_height and in_water:
            self.rect.y += self.speed
        if keys[pygame.K_SPACE] and not self.en_saut:
            self.en_saut = True
            self.speed_y = -12 if in_water else -8
        if self.en_saut:
            self.speed_y += self.gravite if not in_water else self.gravite / 2
            self.rect.y += self.speed_y
            if self.rect.top >= screen_height - water_height:
                self.rect.top = screen_height - water_height
                self.speed_y = 0
                self.en_saut = False






font = pygame.font.SysFont(None, 36)
score = 0
score_timer = pygame.time.get_ticks()

score_timer = pygame.time.get_ticks()
score_timer = pygame.time.get_ticks()  # Timer to track when to increase score
font = pygame.font.SysFont(None, 36)  # Font for the score counter

# Charger les images des pièces, du requin et du background
try:
    background_image = pygame.image.load('image/fondniveau2.png').convert()
    background_image = pygame.Surface.subsurface(
        background_image,
        (0, background_image.get_height() // 3, background_image.get_width(), background_image.get_height() * 2 // 3))
    background_image = pygame.transform.scale(
        background_image,
        (screen_width, screen_height))
except pygame.error as e:
    print(f"Erreur : Impossible de charger l'image background ({e})")
    pygame.quit()
    sys.exit()
try:
    coin_image = pygame.image.load('image/coin.png').convert_alpha()
    coin_image = pygame.transform.scale(coin_image, (coin_image.get_width() // 2, coin_image.get_height() // 2))
except pygame.error as e:
    print(f"Erreur : Impossible de charger l'image coin.png ({e})")
    pygame.quit()
    sys.exit()
try:
    requin_image = pygame.image.load('image/requin.png').convert_alpha()
    requin_image = pygame.transform.scale(requin_image, (requin_image.get_width() // 3, requin_image.get_height() // 3))
except pygame.error as e:
    print(f"Erreur : Impossible de charger l'image requin.png ({e})")
    pygame.quit()
    sys.exit()

# Initialiser les pièces, le requin et les surfeurs
# Charger les images des surfeurs
try:
    surfeur1_image = pygame.image.load('image/surfeur1.png').convert_alpha()
    surfeur1_image = pygame.transform.scale(surfeur1_image, (surfeur1_image.get_width() // 3, surfeur1_image.get_height() // 3))
    surfeur2_image = pygame.image.load('image/surfeur2.png').convert_alpha()
    surfeur2_image = pygame.transform.scale(surfeur2_image, (surfeur2_image.get_width() // 3, surfeur2_image.get_height() // 3))
except pygame.error as e:
    print(f"Erreur : Impossible de charger les images des surfeurs ({e})")
    pygame.quit()
    sys.exit()

surfeurs = [
    Surfeur(surfeur1_image, (screen_width // 4, screen_height - water_height - 50), 3),
    Surfeur(surfeur2_image, (3 * screen_width // 4, screen_height - water_height - 50), 3)
]
surfeurs = [
    Surfeur(surfeur1_image, (screen_width // 4, screen_height - water_height - 50), 3),
    Surfeur(surfeur2_image, (3 * screen_width // 4, screen_height - water_height - 50), 3)
]
personnages = surfeurs
pieces = [Piece(coin_image, (100 * i, 500)) for i in range(5)]
  # Removed duplicate declaration
requin = Requin(requin_image, (screen_width // 2, screen_height - water_height), 3)

# Initialisation globale Personnages + UI fixes:
camera_offset = 0
pieces = [Piece(coin_image, (100 * i, 500)) for i in range(5)]  # Initialize pieces
personnages = surfeurs  # Initialize personnage using surfeurs
personnages = surfeurs  # Initialize personnage using surfeurs, updated velocity references
camera_offset_x = 0
camera_offset_y = 0
music_playing = True

clock = pygame.time.Clock()
while True:
    clock.tick(60)
    screen.fill((0, 0, 0))
    if pygame.time.get_ticks() - score_timer >= 1000:
        score += 1
        score_timer = pygame.time.get_ticks()
    screen.blit(background_image, (0, 0))
    for piece in pieces:
        screen.blit(piece.image, piece.rect)  # Ensure correct drawing of all elements
    screen.blit(score_text_surface, (10, 10))
    for surfeur in surfeurs:
        surfeur.deplacer(screen_width)
        screen.blit(surfeur.image, surfeur.rect)
    requin.deplacer(pygame.key.get_pressed(), screen_width, screen_height, water_height)

    pygame.draw.line(screen, (0, 255, 0), (0, water_height), (screen_width, water_height), 2)  # Waterline debugging
    for surfeur in surfeurs:
        surfeur.deplacer(screen_width)
        screen.blit(surfeur.image, surfeur.rect)
    for piece in pieces:
        if piece.rect.colliderect(requin.rect):  # Combine drawing logic
            pieces.remove(piece)
            score += 1
            print(f"Score: {score}")
        else:
            screen.blit(piece.image, piece.rect)
    score_text_surface = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text_surface, (10, 10))


    for piece in pieces:
        screen.blit(piece.image, piece.rect)
    for surfeur in surfeurs:
        surfeur.deplacer(screen_width)
        screen.blit(surfeur.image, surfeur.rect)

    # Display the score counter
  # Merged score drawing block into a single section
  # Removed redundant code

# Dessiner les pièces
    for piece in pieces:  # Streamline the rendering and handling loop
        if piece.rect.colliderect(requin.rect):
            pieces.remove(piece)
            score += 1
            print(f"Score: {score}")  # Debugging score increment
        else:
            screen.blit(piece.image, piece.rect)
    pygame.draw.rect(screen, (255, 0, 0), requin.rect, 2)  # Debugging - Draw hitbox
    screen.blit(requin.image, requin.rect)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                personnage1.rect.topleft = (300, 300)
