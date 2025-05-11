import pygame
import sys
import math

# Initialisation de Pygame
pygame.init()

# Définir les dimensions de la fenêtre en plein écran
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Deux personnages qui marchent avec des vagues améliorées")

# Définir la couleur de l'eau
water_color = (0, 0, 255)  # Bleu
class Personnage:
    def __init__(self, image, start_pos):
        self.image = pygame.transform.scale(pygame.image.load(image), (150, 150))
        self.rect = self.image.get_rect()
        self.rect.topleft = start_pos
        self.speed = 1
        self.vitesse_y = 0
        self.en_saut = False
        self.gravite = 0.086
        self.live = True

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




class Piece:
    def __init__(self, position, img):
        self.pos = position
        self.img = pygame.transform.scale(pygame.image.load(img), (50, 50))

    def dessiner(self, screen):
        screen.blit(self.img, (self.pos[0], self.pos[1]))





personnage1 = Personnage('image/requin.png', (100, 100))
piece1 = Piece((100,100), "image/coin.png")



touches_personnage1 = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN, 'space': pygame.K_SPACE}

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
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    personnage1.deplacer(touches_personnage1, keys, screen_width, screen_height)


    # Mettre à jour le décalage de la caméra pour suivre le personnage
    camera_offset_x = max(0, personnage1.rect.x - screen_width // 2)
    camera_offset_y = max(0, personnage1.rect.y - screen_height // 2)

    # Remplir l'écran avec une couleur de fond
    screen.fill((0, 0, 0))

    # Dessiner l'eau sur le premier tiers en partant du bas
    water_rect = pygame.Rect(0, screen_height * 2 // 3, screen_width, screen_height // 3)
    pygame.draw.rect(screen, water_color, water_rect)

    # Dessiner les personnages sur l'écran
    personnage1.dessiner(screen, camera_offset_x)
    piece1.dessiner(screen)

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
                personnage1.rect.topleft = (300, 300)  # Réinitialise la position du personnage
