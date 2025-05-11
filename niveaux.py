import pygame
from niveau1 import Niveau1
from ecran_fin import fenetre_défaite
from ecran_fin import fenetre_victoire
def image(fenetre,largeur,longueur):

    # Police et assets.
    font = pygame.font.Font(None, 36)
    image_de_fond_original = pygame.image.load("image/niveaux.png").convert()
    pygame.display.set_caption("niveaux")

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
                        current_screen = "niveaux_1"
                        win=Niveau1()
                        if win==0 :
                            fenetre_défaite(fenetre, longueur, largeur)
                        else :
                            fenetre_victoire(fenetre, longueur, largeur)

                        current_screen = "menu"
                        pygame.display.set_caption("shark.io")

                    elif pygame.Rect(530, 677, 200, 59).collidepoint(pos):  # Guide
                        current_screen = "shark.io"
                        # mettre la fonction pour le premier niveau
                        print("Lancer le jeu")  # METTRE FONCTION QUI PERMET DE LANCER LE JEU
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
