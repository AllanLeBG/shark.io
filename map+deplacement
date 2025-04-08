import pygame
import sys
import math

# Initialisation de Pygame
pygame.init()

# Charger et jouer la musique
pygame.mixer.music.load('musique.mp3')
pygame.mixer.music.play(-1)  # -1 pour jouer en boucle

# Définir les dimensions de la fenêtre en plein écran
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Deux personnages qui marchent avec des vagues améliorées")

# Définir la couleur de l'eau
water_color = (0, 0, 255)  # Bleu

# Charger et redimensionner l'image du bouton pour couper la musique
mute_button_image = pygame.image.load('mute_button.jpg')
mute_button_image = pygame.transform.scale(mute_button_image, (30, 30))  # Redimensionner à 30x30 pixels
mute_button_rect = mute_button_image.get_rect()
mute_button_rect.topright = (screen.get_width() - 10, 10)  # Position en haut à droite avec un décalage de 10 pixels

# Classe Personnage
class Personnage:
    def __init__(self, image_path, start_pos):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = start_pos
        self.speed = 5

    def deplacer(self, touches, keys, screen_width, screen_height):
        if keys[touches['left']] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[touches['right']] and self.rect.right < screen_width * 2:  # Limite sur la droite augmentée
            self.rect.x += self.speed
        if keys[touches['up']] and self.rect.top > -100:  # Limite en hauteur augmentée
            self.rect.y -= self.speed
        if keys[touches['down']] and self.rect.bottom < screen_height + 100:  # Limite en hauteur augmentée
            self.rect.y += self.speed

    def dessiner(self, screen, camera_offset):
        screen.blit(self.image, (self.rect.x - camera_offset, self.rect.y))

# Classe Vague
class Vague:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.waves = []
        self.wave_height = 20
        self.wave_length = 100
        self.speed = 0.05
        self.offset = 0

    def update(self):
        self.offset += self.speed

    def dessiner(self, screen, camera_offset):
        for x in range(0, self.screen_width * 2, 5):  # Limite sur la droite augmentée
            y = int(self.screen_height * 2 / 3 + self.wave_height * math.sin((x * 0.02) + self.offset) + self.wave_height * 0.5 * math.sin((x * 0.04) + self.offset * 1.5))
            pygame.draw.line(screen, water_color, (x - camera_offset, y), (x - camera_offset, self.screen_height))

# Créer deux personnages
personnage1 = Personnage('image_drole.jpg', (100, 100))
personnage2 = Personnage('image_drole.jpg', (200, 200))

# Créer les vagues
vagues = Vague(screen.get_width(), screen.get_height())

# Définir les touches pour chaque personnage
touches_personnage1 = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN}
touches_personnage2 = {'left': pygame.K_q, 'right': pygame.K_d, 'up': pygame.K_z, 'down': pygame.K_s}

# Boucle principale du jeu
camera_offset_x = 0
camera_offset_y = 0
followed_character = personnage1  # Choisissez quel personnage suivre
music_playing = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if mute_button_rect.collidepoint(event.pos):
                if music_playing:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
                music_playing = not music_playing

    # Récupérer les touches pressées
    keys = pygame.key.get_pressed()

    # Déplacer les personnages
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    personnage1.deplacer(touches_personnage1, keys, screen_width, screen_height)
    personnage2.deplacer(touches_personnage2, keys, screen_width, screen_height)

    # Mettre à jour les vagues
    vagues.update()

    # Mettre à jour le décalage de la caméra pour suivre le personnage
    camera_offset_x = max(0, followed_character.rect.x - screen_width // 2)
    camera_offset_y = max(0, followed_character.rect.y - screen_height // 2)

    # Remplir l'écran avec une couleur de fond
    screen.fill((0, 0, 0))

    # Dessiner l'eau sur le premier tiers en partant du bas
    water_rect = pygame.Rect(0, screen_height * 2 // 3, screen_width, screen_height // 3)
    pygame.draw.rect(screen, water_color, water_rect)

    # Dessiner les vagues
    vagues.dessiner(screen, camera_offset_x)

    # Dessiner les personnages sur l'écran
    personnage1.dessiner(screen, camera_offset_x)
    personnage2.dessiner(screen, camera_offset_x)

    # Dessiner le bouton de coupure de la musique
    screen.blit(mute_button_image, mute_button_rect)

    # Mettre à jour l'affichage
    pygame.display.flip()
