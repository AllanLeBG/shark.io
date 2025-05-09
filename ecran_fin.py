import pygame

def fenetre_victoire(fenetre,longueur,largeur):
    from niveaux import image
    pygame.mixer.music.stop()#arrete la musique
    son_victoire= pygame.mixer.Sound("son/win.wav")
    son_victoire.play()
    pygame.display.set_caption("Winner")
    image_de_fond = pygame.image.load("image/Win.png").convert()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                image(fenetre, largeur, longueur)
                return

        image_de_fond_redimensionnee = pygame.transform.scale(image_de_fond, (largeur, longueur))
        fenetre.blit(image_de_fond_redimensionnee, (0, 0))
        pygame.display.flip()
        clock.tick(60)

def fenetre_défaite(fenetre,longueur,largeur):
    from niveaux import image
    pygame.mixer.music.stop()#arrete la musique
    son_victoire= pygame.mixer.Sound("son/loose.wav")
    son_victoire.play()#activer le nouveau son

    pygame.display.set_caption("you loose")
    image_de_fond = pygame.image.load("image/game_over.png").convert()

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                image(fenetre, largeur, longueur)
                return

        image_de_fond_redimensionnee = pygame.transform.scale(image_de_fond, (largeur, longueur))
        fenetre.blit(image_de_fond_redimensionnee, (0, 0))
        pygame.display.flip()
        clock.tick(60)
