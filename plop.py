import pygame
import sys
import math

# Initialisation de Pygame
pygame.init()
background_image = pygame.image.load('image/fondniveau2.png')
background_image = pygame.Surface.subsurface(background_image, (0, background_image.get_height() // 3, background_image.get_width(), background_image.get_height() * 2 // 3))
background_image = pygame.transform.scale(background_image, (pygame.display.Info().current_w, pygame.display.Info().current_h))

# Définir les dimensions de la fenêtre en plein écran
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width = pygame.display.Info().current_w
screen_height = pygame.display.Info().current_h
pygame.display.set_caption("Deux personnages qui marchent avec des vagues améliorées")

# Définir la couleur de l'eau
water_color = (0, 0, 255)  # Bleu
water_height = pygame.display.Info().current_h // 2
class Piece:
    def __init__(self, image, pos):
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
class Personnage:
    def __init__(self, image, start_pos):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = start_pos
        self.speed = 1
        self.vitesse_y = 0
        self.en_saut = False
        self.gravite = 0.086
        self.live = True
        self.comp = 0

    def deplacer(self, touches, keys, screen_width, screen_height):


        #Dans l'eau
        if self.rect.top > screen_height * 2 // 3:
            if keys[touches['left']] and self.rect.left > 0:
                self.rect.x -= self.speed
            if keys[touches['right']] and self.rect.right < screen_width * 2:
                self.rect.x += self.speed
            if keys[touches['up']]:
                self.rect.y -= self.speed
            if keys[touches['down']] and self.rect.bottom < screen_height:
                self.rect.y += self.speed


        #Sortie de l'eau 01
        elif self.rect.top <= screen_height * 2 // 3:

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
                if self.rect.top >= screen_height * 2 // 3:
                    self.rect.top = screen_height * 2 // 3
                    self.vitesse_y = 0
                    self.en_saut = False



    def dessiner(self, screen, camera_offset):
        screen.blit(self.image, (self.rect.x - camera_offset, self.rect.y))















font = pygame.font.SysFont(None, 36)  # Font for the score counter
score = 0  # Initialize score counter
font = pygame.font.SysFont(None, 36)  # Font for the score counter

# Charger les images des pièces et du requin
piece_image = pygame.image.load('image/coin.png')
requin_image = pygame.image.load('image/requin.png')
requin_image = pygame.transform.scale(requin_image, (requin_image.get_width() // 3, requin_image.get_height() // 3))
# Initialiser les pièces et le requin
pieces = [Piece(pygame.transform.scale(piece_image, (125,125)), (100 * i, 500)) for i in range(5)]
requin = Personnage(requin_image, (400, 400))
# Boucle principale du jeu
camera_offset_x = 0
camera_offset_y = 0
music_playing = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Récupérer les touches pressées
    keys = pygame.key.get_pressed()

    # Déplacer les personnages
    # Déplacer le requin
    if keys[pygame.K_LEFT] and requin.rect.left > 0:
        requin.rect.x -= requin.speed
    if keys[pygame.K_RIGHT] and requin.rect.right < screen_width:
        requin.rect.x += requin.speed
    if keys[pygame.K_UP] and requin.rect.top > screen_height - water_height and not requin.en_saut:
        if requin.rect.top > 0:
            requin.rect.y -= requin.speed
    if keys[pygame.K_DOWN] and requin.rect.bottom < screen_height:
        if requin.rect.bottom < screen_height:
            requin.rect.y += requin.speed

    # Handle requin jumping behavior
    if requin.en_saut:
        requin.speed_y += requin.gravite
        requin.rect.y += requin.speed_y

        # End jump when it re-enters the water
        if requin.rect.top >= screen_height - water_height:
            requin.rect.top = screen_height - water_height
            requin.speed_y = 0
            requin.en_saut = False
    elif keys[pygame.K_SPACE] and not requin.en_saut:
        requin.en_saut = True
        requin.speed_y = -15
        requin.speed_y = -requin.speed  # Reflect trajectory
        requin.rect.y -= 5  # Ensure slight movement for realism

    # Mettre à jour le décalage de la caméra pour suivre le personnage


    # Dessiner les pièces
    for piece in pieces:
        screen.blit(piece.image, piece.rect)
        score_text_surface = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text_surface, (10, 10))  # Render the score at the top-left corner
    # Dessiner le requin
    screen.blit(requin.image, requin.rect)
    score_text_surface = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text_surface, (10, 10))
# Dessiner l'image de fond
    screen.blit(background_image, (0, 0))
    # Dessiner les pièces
    for piece in pieces:
        if piece.rect.colliderect(requin.rect):
            pieces.remove(piece)
            score += 1
        else:
            screen.blit(piece.image, piece.rect)
    # Dessiner le requin
    screen.blit(requin.image, requin.rect)

    # Mettre à jour l'affichage
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                afficher_mur = not afficher_mur  # Toggle affichage du mur
            elif event.key == pygame.K_r:
                requin.rect.topleft = (300, 300)  # Réinitialise la position du personnage
