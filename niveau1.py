import pygame
import sys
import random
from map_deplacement import Perso
from map_deplacement import Coin
from classes import Oiseau, Nageur


def Niveau1():
    pygame.init()
    win = 0

    pygame.display.set_caption("Niveaux_1")
    screen = pygame.display.set_mode((1200, 800))
    image_de_fond = pygame.image.load("image/fond.png").convert()
    image_de_fond = pygame.transform.scale(image_de_fond, (3000, 1600))
    screen.blit(image_de_fond, (0, 0))

    # Déclaration de l'île
    ile_image = pygame.image.load("image/ile.png").convert_alpha()
    ile_image = pygame.transform.scale(ile_image, (400, 800))
    ile_rect = ile_image.get_rect(topleft=(1700, 800))

    # Déclaration de pièce
    point_image = Coin((805, 1050), "image/coin.png")
    point_image.dessiner_menu(screen)

    # Mur invisible
    mur_inv_image = pygame.image.load("image/mur_invisible.png").convert_alpha()
    mur_inv_image = pygame.transform.scale(mur_inv_image, (10, 1600))
    mur_inv_rect = mur_inv_image.get_rect(topleft=(2100, 0))

    # Mur
    mur_image = pygame.image.load("image/mur-1.png").convert_alpha()
    mur_image = pygame.transform.scale(mur_image, (400, 200))
    mur_rect = mur_image.get_rect(topleft=(800, 480))

    # Eau
    eau_image = pygame.image.load("image/eau-1.png").convert_alpha()
    eau_image = pygame.transform.scale(eau_image, (380, 200))
    eau_rect = eau_image.get_rect(topleft=(800, 480))

    # Personnage
    bonhomme_image = pygame.image.load("image/perso-1.png").convert_alpha()
    bonhomme_image = pygame.transform.scale(bonhomme_image, (200, 300))
    bonhomme_rect = bonhomme_image.get_rect(topleft=(880, 290))

    # Bouton mute
    mute_button_image = pygame.image.load("image/mutebutton.png")
    mute_button_image = pygame.transform.scale(mute_button_image, (30, 30))
    mute_button_rect = mute_button_image.get_rect()
    mute_button_rect.topright = (screen.get_width() - 10, 10)

    # Pièce
    piece = Coin((1032, 1098), "image/coin.png")

    # Initialisation des bonus
    bonus_list = pygame.sprite.Group()  # Groupe spécial Pygame
    bonus_spawn_timer = 0
    bonus_spawn_interval = 120  # 2 secondes à 60 FPS

    # Requin
    mon_perso = Perso("image/requin.png", (350, 1208))
    touches_mon_perso = {
        'left': pygame.K_LEFT,
        'right': pygame.K_RIGHT,
        'up': pygame.K_UP,
        'down': pygame.K_DOWN,
        'space': pygame.K_SPACE
    }
    followed_character = mon_perso

    map_width, map_height = 2000, 1600
    camera_offset_x = 0
    camera_offset_y = 0
    music_playing = True

    clock = pygame.time.Clock()

    score=0

    while True:
        dt = clock.tick(60)  # Limite à 60 FPS

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

        for bonus in bonus_list:
            bonus.update()

        keys = pygame.key.get_pressed()
        point_image.dessiner_menu(screen)

        # Déplacement du personnage
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        mon_perso.deplacer(touches_mon_perso, keys, map_width, map_height)

        # Gestion des collisions avec l'île
        if mon_perso.rect.colliderect(mur_inv_rect):
            if keys[pygame.K_RIGHT]:
                mon_perso.rect.x -= mon_perso.speed

        if mon_perso.rect.colliderect(ile_rect):
            if keys[pygame.K_RIGHT]:
                mon_perso.rect.x -= mon_perso.speed
            if keys[pygame.K_UP]:
                mon_perso.rect.y += mon_perso.speed
            if keys[pygame.K_DOWN]:
                mon_perso.rect.y -= mon_perso.speed

        # Gestion des bonus

        if random.random() < 0.005:  # fréquence d'apparition
            if random.random() < 0.5:  # 50% mouette et 50% nageur
                # Mouette (dans les airs - entre y=100 et 400)
                bonus_list.add(Oiseau(1300, random.randint(100, 500)))
            else:
                # Nageur (dans l'eau - entre y=550 et 750)
                bonus_list.add(Nageur(1300, random.randint(900, 1100)))

        # Mise à jour et affichage des bonus
        bonus_list.update()  # Appelle auto. actualisation sur tous les sprites
        bonus_touchés = pygame.sprite.spritecollide(mon_perso, bonus_list, True, pygame.sprite.collide_mask)
        for bonus in bonus_touchés:
            score += bonus.valeur
        bonus_list.draw(screen)

        # Collision avec la pièce
        if mon_perso.rect.colliderect(pygame.Rect(piece.pos[0], piece.pos[1], 40, 40)) and not piece.ramassee:
            if any(keys[key] for key in [pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT]):
                piece.ramasser()
                score += piece.get_pieces()

        # Gestion des collisions avec le mur et le bonhomme
        if mon_perso.rect.colliderect(mur_rect):
            if any(keys[key] for key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]):
                return win

        if mon_perso.rect.colliderect(bonhomme_rect):
            if any(keys[key] for key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]):
                win = 1
                return win

        # Mise à jour de la caméra
        camera_offset_x = max(0, min(followed_character.rect.x - screen_width // 2, map_width - screen_width))
        camera_offset_y = max(0, min(followed_character.rect.y - screen_height // 2, map_height - screen_height))

        # Affichage
        screen.blit(image_de_fond, (-camera_offset_x, -camera_offset_y))

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (70, 20))

        # Affichage des bonus
        for bonus in bonus_list:
            screen.blit(bonus.image, (bonus.rect.x - camera_offset_x, bonus.rect.y - camera_offset_y))

        mon_perso.dessiner(screen, camera_offset_x, camera_offset_y)
        screen.blit(eau_image, (eau_rect.x - camera_offset_x, eau_rect.y - camera_offset_y))
        screen.blit(bonhomme_image, (bonhomme_rect.x - camera_offset_x, bonhomme_rect.y - camera_offset_y))
        screen.blit(mur_image, (mur_rect.x - camera_offset_x, mur_rect.y - camera_offset_y))
        screen.blit(mute_button_image, mute_button_rect)
        piece.dessiner(screen, camera_offset_x, camera_offset_y)

        # Affichage du score
        piece_number = Coin((10, 10), "image/coin.png")
        piece_number.dessiner_menu(screen)

        # Affichage des coordonnées
        #pos_souris = pygame.mouse.get_pos()
        #pos_souris_map_x = pos_souris[0] + camera_offset_x
        #pos_souris_map_y = pos_souris[1] + camera_offset_y
        #font = pygame.font.Font(None, 36)
        #text_coord = font.render(f"X: {pos_souris_map_x} Y: {pos_souris_map_y}", True, (255, 255, 255))
        #screen.blit(text_coord, (10, 10))

        screen.blit(ile_image, (ile_rect.x - camera_offset_x, ile_rect.y - camera_offset_y))
        pygame.display.flip()





