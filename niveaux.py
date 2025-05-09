import pygame
def image(fenetre,largeur,longueur):
    pygame.display.set_caption("niveaux")

    # Police et assets.
    font = pygame.font.Font(None, 36)
    image_de_fond_original = pygame.image.load("image/niveaux.png").convert()

    clock = pygame.time.Clock()
    running = True
    current_screen = "niveaux"

    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if current_screen == "niveaux":
                    if pygame.Rect(530, 588, 200, 55).collidepoint(pos):  # Start
                        current_screen = "shark.io"
                        #mettre la fonction pour le premier niveau
                        print("Lancer le jeu")#METTRE FONCTION QUI PERMET DE LANCER LE JEU

                    elif pygame.Rect(530, 677, 200, 59).collidepoint(pos):  # Guide
                        current_screen = "tuto"
                        #tuto(fenetre,largeur,longueur)
                        current_screen = "menu"
                    elif pygame.Rect(224, 74, 817, 155).collidepoint(pos):  # Start
                        while running:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()
                                elif event.type == pygame.MOUSEBUTTONDOWN:
                                    return


        pos_souris = pygame.mouse.get_pos()

        # Redimensionner l'image
        image_de_fond_redimensionnee = pygame.transform.scale(image_de_fond_original, (largeur, longueur))
        #Affichage
        fenetre.blit(image_de_fond_redimensionnee, (0, 0))

        # Affichage des coordonnées de la souris
        #text_coord = font.render(f"X:{pos_souris[0]} Y:{pos_souris[1]}", True, (255, 255, 255))
        #fenetre.blit(text_coord, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
