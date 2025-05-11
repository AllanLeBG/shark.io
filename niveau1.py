import pygame
import math
import sys
from map_deplacement import Personnage

def Niveau1():
    pygame.init()
    win=0

    #gestion de musique
    pygame.mixer.music.stop()  # arrete la musique
    pygame.mixer.music.load("son/ocean.wav")
    pygame.mixer.music.play(-1)  # -1 pour jouer en boucle

    pygame.display.set_caption("Niveaux_1")
    screen = pygame.display.set_mode((1200, 800))
    image_de_fond = pygame.image.load("image/fond.png").convert()
    image_de_fond = pygame.transform.scale(image_de_fond, (2000, 1600))
    screen.blit(image_de_fond, (0, 0))

    #déclaration de l'ile
    ile_image = pygame.image.load("image/ile.png").convert_alpha()  # Utilise une image d'île avec transparence
    ile_image = pygame.transform.scale(ile_image, (400, 800))
    ile_rect = ile_image.get_rect(topleft=(1700,800))

    #declaration mut invible pour eviter de dépasser la limite
    mur_inv_image = pygame.image.load("image/mur_invisible.png").convert_alpha()  # Utilise une image d'île avec transparence
    mur_inv_image = pygame.transform.scale(mur_inv_image, (10, 1600))
    mur_inv_rect = mur_inv_image.get_rect(topleft=(2100,0))

    #declaration du mur
    mur_image = pygame.image.load("image/mur-1.png").convert_alpha()  # Utilise une image de mur avec transparence
    mur_image = pygame.transform.scale(mur_image, (400, 200))
    mur_rect = mur_image.get_rect(topleft=(800, 480))

    #declaration de l'eau
    eau_image = pygame.image.load("image/eau-1.png").convert_alpha()  # Utilise une image d eau avec transparence
    eau_image = pygame.transform.scale(eau_image, (380, 200))
    eau_rect = eau_image.get_rect(topleft=(800, 480))

    # declaration des persos
    bonhomme_image = pygame.image.load("image/perso-1.png").convert_alpha()  # Utilise une image d eau avec transparence
    bonhomme_image = pygame.transform.scale(bonhomme_image, (200, 300))
    bonhomme_rect = bonhomme_image.get_rect(topleft=(880, 290))

    #bouton couper la musique
    mute_button_image = pygame.image.load("image/mutebutton.png")#mettre image pour couper le son
    mute_button_image = pygame.transform.scale(mute_button_image, (30, 30))  # Redimensionner à 30x30 pixels
    mute_button_rect = mute_button_image.get_rect()
    mute_button_rect.topright = (screen.get_width() - 10, 10)  # Position en haut à droite avec un décalage de 10 pixels

    camera_offset_x = 0

    #création du requin
    mon_perso=Personnage("image/requin.png",(350,1208))
    # définition des touches
    touches_mon_perso = {
        'left': pygame.K_LEFT,
        'right': pygame.K_RIGHT,
        'up': pygame.K_UP,
        'down': pygame.K_DOWN,
        'space': pygame.K_SPACE
    }
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


        # Détecter les collisions entre le personnage et l'île
        if mon_perso.rect.colliderect(mur_inv_rect):
            # Si le personnage entre en collision avec l'île, empêcher le mouvement
            if keys[pygame.K_RIGHT]:  # Empêcher de se déplacer à droite si collision
                mon_perso.rect.x -= mon_perso.speed

        #detecter les collisition du mur invisible
        if mon_perso.rect.colliderect(ile_rect):
            # Si le personnage entre en collision avec l'île, empêcher le mouvement
            if keys[pygame.K_RIGHT]:  # Empêcher de se déplacer à droite si collision
                mon_perso.rect.x -= mon_perso.speed
            if keys[pygame.K_UP]:  # Empêcher de se déplacer en haut si collision
                mon_perso.rect.y += mon_perso.speed
            if keys[pygame.K_DOWN]:  # Empêcher de se déplacer en bas si collision
                mon_perso.rect.y -= mon_perso.speed

                # Détecter les collisions entre le personnage et l'île
        if mon_perso.rect.colliderect(mur_rect):
                # Si le personnage entre en collision avec l'île, empêcher le mouvement
            if keys[pygame.K_LEFT] : # perdre si touche
                return win
            if keys[pygame.K_RIGHT]:  # perdre si touche
                return win
            if keys[pygame.K_UP]:  # perdre si touche
                return win
            if keys[pygame.K_DOWN]:  # perdre si touche
                return win

        if mon_perso.rect.colliderect(bonhomme_rect):
                # Si le personnage entre en collision avec l'île, empêcher le mouvement
            if keys[pygame.K_LEFT] : # perdre si touche
                win=1
                return win
            if keys[pygame.K_RIGHT]:  # perdre si touche
                win=1
                return win
            if keys[pygame.K_UP]:  # perdre si touche
                win=1
                return win
            if keys[pygame.K_DOWN]:  # perdre si touche
                win=1
                return win

        camera_offset_x = max(0, min(followed_character.rect.x - screen_width // 2, map_width - screen_width))
        camera_offset_y = max(0, min(followed_character.rect.y - screen_height // 2, map_height - screen_height))

        # Mettre à jour le décalage de la caméra pour suivre le personnage
        screen.blit(image_de_fond, (-camera_offset_x, -camera_offset_y))

        mon_perso.dessiner(screen, camera_offset_x,camera_offset_y)
        screen.blit(eau_image, (eau_rect.x - camera_offset_x, eau_rect.y - camera_offset_y))
        screen.blit(bonhomme_image, (bonhomme_rect.x - camera_offset_x, bonhomme_rect.y - camera_offset_y))
        screen.blit(mur_image, (mur_rect.x - camera_offset_x, mur_rect.y - camera_offset_y))
        screen.blit(mute_button_image, mute_button_rect)



        # Affichage des coordonnées de la souris (utilisé pour faire les boutons)
        pos_souris = pygame.mouse.get_pos()
        pos_souris_map_x = pos_souris[0] + camera_offset_x  # Ajouter le décalage X
        pos_souris_map_y = pos_souris[1] + camera_offset_y  # Ajouter le décalage Y
        font = pygame.font.Font(None, 36)
        text_coord = font.render(f"X: {pos_souris_map_x} Y: {pos_souris_map_y}", True, (255, 255, 255))
        screen.blit(text_coord, (10, 10))  # Afficher les coordonnées en haut à gauche

        screen.blit(ile_image, (ile_rect.x - camera_offset_x, ile_rect.y - camera_offset_y))
        pygame.display.flip()




