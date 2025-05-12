import pygame
import sys
import classes

def Niveau2():
    pygame.init()
    screen_width, screen_height = 1280, 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Niveau 2")
    water_height = pygame.display.Info().current_h // 2
    font = pygame.font.SysFont(None, 36)
    score = 0
    score_timer = pygame.time.get_ticks()
    
    # Images
    background_image = pygame.image.load('image/fondniveau2.png').convert()
    background_image = pygame.Surface.subsurface(background_image, (0, background_image.get_height() // 3, background_image.get_width(), background_image.get_height() * 2 // 3))
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
    
    coin_image = pygame.image.load('image/coin.png').convert_alpha()
    coin_image = pygame.transform.scale(coin_image, (50, 50))
    
    requin_image = pygame.image.load('image/requin2.png').convert_alpha()
    requin_image = pygame.transform.scale(requin_image, (200, 200))
    
    tueur_image = pygame.image.load('image/bateau1.png').convert_alpha()
    tueur_image = pygame.transform.scale(tueur_image, (tueur_image.get_width() // 4, tueur_image.get_height() // 4))
    
    
    surfeur1_image = pygame.image.load('image/surfeur1.png').convert_alpha()
    surfeur1_image = pygame.transform.scale(surfeur1_image, (surfeur1_image.get_width() // 3, surfeur1_image.get_height() // 3))
    surfeur2_image = pygame.image.load('image/surfeur2.png').convert_alpha()
    surfeur2_image = pygame.transform.scale(surfeur2_image, (surfeur2_image.get_width() // 3, surfeur2_image.get_height() // 3))
    
    mouette1_image = pygame.image.load('image/mouette1.png').convert_alpha()
    mouette1_image = pygame.transform.scale(mouette1_image, (100, 100))
    mouette2_image = pygame.image.load('image/mouette2.png').convert_alpha()
    mouette2_image = pygame.transform.scale(mouette2_image, (100, 100))
    
    # Entités
    surfeurs = [
        Surfeur(surfeur1_image, (screen_width // 4, screen_height - water_height - 50), 3),
        Surfeur(surfeur2_image, (3 * screen_width // 4, screen_height - water_height - 50), 3)
    ]
    
    mouettes = [
        Surfeur(mouette1_image, (100, 250), 2),
        Surfeur(mouette2_image, (2 * screen_width // 3, screen_height // 4), 2)
    ]
    
    tueurs = [
        TueurRequin(tueur_image, (screen_width // 4, screen_height - water_height - 50), 3),
        TueurRequin(tueur_image, (3 * screen_width // 4, screen_height - water_height - 50), 3)
    ]
    
    pieces = [Piecespe(coin_image, (100 * i + (i*400), 500 - (i*230))) for i in range(2)]
    requin = Requin(requin_image, (0, screen_height - water_height + 100), 5)
    
    clock = pygame.time.Clock()
    
    # Boucle principale
    while True:
        clock.tick(60)
        screen.blit(background_image, (0, 0))
    
        if pygame.time.get_ticks() - score_timer >= 1000:
            score += 1
            score_timer = pygame.time.get_ticks()
    
        # Score
        score_text_surface = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text_surface, (10, 10))
    
        # Pièces
        for piece in pieces[:]:
            if piece.rect.colliderect(requin.rect):
                pieces.remove(piece)
                score += 1
            else:
                screen.blit(piece.image, piece.rect)
    
        # Surfeurs
        for surfeur in surfeurs[:]:
            surfeur.deplacer(screen_width)
            screen.blit(surfeur.image, surfeur.rect)
            if surfeur.rect.colliderect(requin.rect):
                surfeurs.remove(surfeur)
    
        # Mouettes
        for mouette in mouettes[:]:
            mouette.deplacer(screen_width)
            screen.blit(mouette.image, mouette.rect)
            if mouette.rect.colliderect(requin.rect):
                mouettes.remove(mouette)
    
        for tueur in tueurs[:]:
            tueur.deplacer(screen_width)
            screen.blit(tueur.image, tueur.rect)
            if tueur.rect.colliderect(requin.rect):
                return 0
        if score>= 20:
            return 1
        # Requin
        requin.deplacer(pygame.key.get_pressed(), screen_width, screen_height, water_height)
        screen.blit(requin.image, requin.rect)
    
        pygame.display.flip()
    
        # Événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    requin.rect.topleft = (300, 300)
