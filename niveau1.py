import pygame
import math
import sys
from map_deplacement import Personnage

class Personnage:
    def __init__(self, image_path, start_pos): # permet de créer un personnage
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (300, 200))
        self.rect = self.image.get_rect()
        self.rect.topleft = start_pos
        self.speed = 5

    def deplacer(self, touches,keys, map_width, map_height): # fonction qui gere le deplacement des personnage elle prend en compte le perso (self) les touches du clavier  les largeur (1200) et longueur(800) de l ecran
        if keys[touches['left']] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[touches['right']] and self.rect.right < map_width * 2:  # Limite sur la droite augmentée
            self.rect.x += self.speed
        if keys[touches['up']] and self.rect.top > -100:  # Limite en hauteur augmentée
            self.rect.y -= self.speed
        if keys[touches['down']] and self.rect.bottom < map_height + 100:  # Limite en hauteur augmentée
            self.rect.y += self.speed

    def dessiner(self, screen, camera_offset_x,camera_offset_y): # permet de suivre le personnage ( avec la caméra )
        screen.blit(self.image, (self.rect.x - camera_offset_x, self.rect.y - camera_offset_y))

def niveau1():
    pygame.init()

    #gestion de musique
    pygame.mixer.music.stop()  # arrete la musique
    pygame.mixer.music.load("son/ocean.wav")
    pygame.mixer.music.play(-1)  # -1 pour jouer en boucle

    pygame.display.set_caption("Niveaux_1")
    screen = pygame.display.set_mode((1200, 800))
    image_de_fond = pygame.image.load("image/fond.png").convert()
    image_de_fond = pygame.transform.scale(image_de_fond, (2000, 1600))
    screen.blit(image_de_fond, (0, 0))

    #bouton couper la musique
    mute_button_image = pygame.image.load("image/coin.png")#mettre image pour couper le son
    mute_button_image = pygame.transform.scale(mute_button_image, (30, 30))  # Redimensionner à 30x30 pixels
    mute_button_rect = mute_button_image.get_rect()
    mute_button_rect.topright = (screen.get_width() - 10, 10)  # Position en haut à droite avec un décalage de 10 pixels

    camera_offset_x = 0

    #création du requin
    mon_perso=Personnage("image/requin.png",(350,1208))
    touches_mon_perso = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN}
    followed_character = mon_perso  # Choisissez quel personnage suivre

    map_width, map_height = 2000, 1600  # Taille de la carte plus grande
    camera_offset_x = 0
    camera_offset_y = 0

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
        mon_perso.deplacer(touches_mon_perso, keys, map_width, map_height)

        camera_offset_x = max(0, min(followed_character.rect.x - screen_width // 2, map_width - screen_width))
        camera_offset_y = max(0, min(followed_character.rect.y - screen_height // 2, map_height - screen_height))

        # Mettre à jour le décalage de la caméra pour suivre le personnage
        screen.blit(image_de_fond, (-camera_offset_x, -camera_offset_y))
        mon_perso.dessiner(screen, camera_offset_x,camera_offset_y)
        screen.blit(mute_button_image, mute_button_rect)


        # Affichage des coordonnées de la souris (utilisé pour faire les boutons)
        pos_souris = pygame.mouse.get_pos()
        pos_souris_map_x = pos_souris[0] + camera_offset_x  # Ajouter le décalage X
        pos_souris_map_y = pos_souris[1] + camera_offset_y  # Ajouter le décalage Y
        font = pygame.font.Font(None, 36)
        text_coord = font.render(f"X: {pos_souris_map_x} Y: {pos_souris_map_y}", True, (255, 255, 255))
        screen.blit(text_coord, (10, 10))  # Afficher les coordonnées en haut à gauche

        pygame.display.flip()



if __name__ == "__main__":
    niveau1()
