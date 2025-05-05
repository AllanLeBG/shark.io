import pygame
from Tuto import tuto

def main():
    pygame.init()
    pygame.font.init()

    largeur, longueur = 1200, 800  # Dimensions de la fenêtre

    fenetre = pygame.display.set_mode((largeur, longueur))
    pygame.display.set_caption("shark.io")

    # Police et assets.
    font = pygame.font.Font(None, 36)
    image_de_fond_original = pygame.image.load("menu.png").convert()

    clock = pygame.time.Clock()
    running = True
    current_screen = "menu"

    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if current_screen == "menu":
                    if pygame.Rect(530, 588, 200, 55).collidepoint(pos):  # Start
                        #current_screen = "shark.io"
                        print("Lancer le jeu")#METTRE FONCTION QUI PERMET DE LANCER LE JEU
                    elif pygame.Rect(530, 677, 200, 59).collidepoint(pos):  # Guide
                        current_screen = "tuto"
                        tuto(fenetre,largeur,longueur)
                        current_screen = "menu"

        pos_souris = pygame.mouse.get_pos()

        # Redimensionner l'image de fond pour s'adapter à la taille de la fenêtre
        image_de_fond_redimensionnee = pygame.transform.scale(image_de_fond_original, (largeur, longueur))

        # Affichage du fond redimensionné
        fenetre.blit(image_de_fond_redimensionnee, (0, 0))

        # Affichage des coordonnées de la souris
        text_coord = font.render(f"X:{pos_souris[0]} Y:{pos_souris[1]}", True, (255, 255, 255))
        fenetre.blit(text_coord, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
